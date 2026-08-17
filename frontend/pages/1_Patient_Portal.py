import streamlit as st

from api_client import (
    APIClientError,
    check_backend_health,
    create_case,
    get_case,
    update_case_status,
    upload_xray,
)
from config import APP_NAME, SAFETY_NOTICE


st.set_page_config(
    page_title=f"Patient Portal | {APP_NAME}",
    page_icon="👤",
    layout="wide",
)

st.title("👤 Patient Portal")
st.caption(
    "Create a case, upload a chest X-ray and track doctor-review status."
)

st.warning(SAFETY_NOTICE, icon="⚠️")
st.info(
    "Use sample or de-identified information during development. "
    "Do not upload real patient data.",
    icon="🔒",
)

try:
    health = check_backend_health()
    st.success(
        f"Backend connected: {health.get('message', 'Service is running')}",
        icon="✅",
    )
except APIClientError as exc:
    st.error(str(exc), icon="🚨")

create_tab, upload_tab, status_tab = st.tabs(
    [
        "Create case",
        "Upload X-ray",
        "Track case",
    ]
)

with create_tab:
    st.subheader("Create a new case")

    with st.form("create_case_form"):
        patient_name = st.text_input(
            "Patient name",
            placeholder="Use a sample name during development",
        )

        patient_age = st.number_input(
            "Patient age",
            min_value=18,
            max_value=120,
            value=18,
            step=1,
        )

        description = st.text_area(
            "Symptoms or case description",
            placeholder="Enter a short description",
            max_chars=500,
        )

        consent = st.checkbox(
            "I confirm that this is sample or de-identified data."
        )

        create_submitted = st.form_submit_button(
            "Create case",
            use_container_width=True,
        )

    if create_submitted:
        if not patient_name.strip():
            st.error("Patient name is required.")

        elif not description.strip():
            st.error("Case description is required.")

        elif not consent:
            st.error("You must confirm the development-data notice.")

        else:
            try:
                created_case = create_case(
                    patient_name=patient_name.strip(),
                    patient_age=int(patient_age),
                    description=description.strip(),
                )

                st.session_state["current_case_id"] = created_case["id"]

                st.success(
                    f"Case #{created_case['id']} created successfully."
                )
                st.json(created_case)

            except APIClientError as exc:
                st.error(str(exc))

with upload_tab:
    st.subheader("Upload chest X-ray")

    default_case_id = int(
        st.session_state.get("current_case_id", 1)
    )

    upload_case_id = st.number_input(
        "Case ID",
        min_value=1,
        value=default_case_id,
        step=1,
        key="upload_case_id",
    )

    uploaded_file = st.file_uploader(
        "Choose an X-ray image",
        type=["png", "jpg", "jpeg"],
        accept_multiple_files=False,
    )

    if uploaded_file is not None:
        st.image(
            uploaded_file,
            caption=uploaded_file.name,
            width=450,
        )

        if st.button(
            "Upload X-ray",
            type="primary",
            use_container_width=True,
        ):
            try:
                upload_result = upload_xray(
                    case_id=int(upload_case_id),
                    filename=uploaded_file.name,
                    content=uploaded_file.getvalue(),
                    content_type=(
                        uploaded_file.type or "application/octet-stream"
                    ),
                )

                update_case_status(
                    case_id=int(upload_case_id),
                    new_status="uploaded",
                )

                st.session_state["current_case_id"] = int(
                    upload_case_id
                )

                st.success("X-ray uploaded successfully.")
                st.json(upload_result)

            except APIClientError as exc:
                st.error(str(exc))

with status_tab:
    st.subheader("Track case status")

    status_case_id = st.number_input(
        "Enter case ID",
        min_value=1,
        value=int(st.session_state.get("current_case_id", 1)),
        step=1,
        key="status_case_id",
    )

    if st.button(
        "Check status",
        use_container_width=True,
    ):
        try:
            case = get_case(int(status_case_id))

            status_labels = {
                "created": "Case created",
                "uploaded": "X-ray uploaded",
                "analyzing": "Analysis in progress",
                "awaiting_review": "Waiting for doctor review",
                "approved": "Approved by doctor",
                "rejected": "Doctor requested changes",
            }

            st.success(
                status_labels.get(
                    case["status"],
                    case["status"].replace("_", " ").title(),
                )
            )

            first_column, second_column = st.columns(2)

            with first_column:
                st.metric("Case ID", case["id"])
                st.write("**Patient:**", case["patient_name"])

            with second_column:
                st.metric(
                    "Status",
                    case["status"].replace("_", " ").title(),
                )
                st.write("**Age:**", case["patient_age"])

            st.write("**Description:**")
            st.write(case["description"])

        except APIClientError as exc:
            st.error(str(exc))

st.divider()

st.page_link(
    "app.py",
    label="Return to home",
    icon="🏠",
)