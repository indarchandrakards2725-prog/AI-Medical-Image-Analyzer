import streamlit as st

from api_client import (
    APIClientError,
    analyze_case,
    check_backend_health,
    get_case,
    get_cases,
)
from config import APP_NAME, SAFETY_NOTICE


st.set_page_config(
    page_title=f"Doctor Dashboard | {APP_NAME}",
    page_icon="🩺",
    layout="wide",
)

st.title("🩺 Doctor Dashboard")
st.caption(
    "Review the case queue and run the current image-preprocessing pipeline."
)

st.warning(SAFETY_NOTICE, icon="⚠️")

try:
    health = check_backend_health()
    st.success(
        f"Backend connected: {health.get('message', 'Service is running')}",
        icon="✅",
    )
except APIClientError as exc:
    st.error(str(exc), icon="🚨")

header_column, refresh_column = st.columns([4, 1])

with header_column:
    st.subheader("Patient case queue")

with refresh_column:
    if st.button(
        "Refresh",
        use_container_width=True,
    ):
        st.rerun()

try:
    cases = get_cases()
except APIClientError as exc:
    st.error(str(exc))
    cases = []

if not cases:
    st.info("No patient cases have been created yet.")

else:
    available_statuses = sorted(
        {case["status"] for case in cases}
    )

    selected_status = st.selectbox(
        "Filter by status",
        options=["All"] + available_statuses,
        format_func=lambda value: value.replace("_", " ").title(),
    )

    if selected_status == "All":
        filtered_cases = cases
    else:
        filtered_cases = [
            case
            for case in cases
            if case["status"] == selected_status
        ]

    table_rows = [
        {
            "Case ID": case["id"],
            "Patient": case["patient_name"],
            "Age": case["patient_age"],
            "Status": case["status"].replace("_", " ").title(),
            "Description": case["description"],
        }
        for case in filtered_cases
    ]

    st.dataframe(
        table_rows,
        use_container_width=True,
        hide_index=True,
    )

    if filtered_cases:
        case_options = {
            (
                f"Case #{case['id']} — "
                f"{case['patient_name']} — "
                f"{case['status'].replace('_', ' ').title()}"
            ): case["id"]
            for case in filtered_cases
        }

        selected_case_label = st.selectbox(
            "Select a case to inspect",
            options=list(case_options.keys()),
        )

        selected_case_id = case_options[selected_case_label]

        try:
            selected_case = get_case(selected_case_id)

            st.subheader(f"Case #{selected_case['id']}")

            detail_column, status_column = st.columns(2)

            with detail_column:
                with st.container(border=True):
                    st.write(
                        "**Patient:**",
                        selected_case["patient_name"],
                    )
                    st.write(
                        "**Age:**",
                        selected_case["patient_age"],
                    )
                    st.write(
                        "**Description:**",
                        selected_case["description"],
                    )

            with status_column:
                with st.container(border=True):
                    st.metric(
                        "Current status",
                        selected_case["status"]
                        .replace("_", " ")
                        .title(),
                    )

            st.subheader("Analysis controls")

            if selected_case["status"] == "uploaded":
                st.info(
                    "The current analysis service only preprocesses the "
                    "image. It does not produce a pneumonia diagnosis."
                )

                if st.button(
                    "Run image preprocessing",
                    type="primary",
                    use_container_width=True,
                ):
                    try:
                        result = analyze_case(selected_case_id)

                        st.success(
                            "Image preprocessing completed. "
                            "Case moved to doctor review."
                        )
                        st.json(result)
                        st.rerun()

                    except APIClientError as exc:
                        st.error(str(exc))

            elif selected_case["status"] == "created":
                st.info(
                    "The patient must upload an X-ray before analysis."
                )

            else:
                st.info(
                    "No preprocessing action is available for this "
                    "case status."
                )

            st.subheader("Doctor decision")

            st.warning(
                "Approval is disabled because the backend does not yet "
                "provide the original X-ray image or a structured report "
                "for doctor review."
            )

            st.button(
                "Approve report",
                disabled=True,
                use_container_width=True,
            )

        except APIClientError as exc:
            st.error(str(exc))

st.divider()

st.page_link(
    "app.py",
    label="Return to home",
    icon="🏠",
)