import streamlit as st

from config import API_BASE_URL, APP_NAME, SAFETY_NOTICE


st.set_page_config(
    page_title=APP_NAME,
    page_icon="🩻",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
        .stApp {
            background-color: #f4f7fb;
        }

        .hero {
            padding: 2.5rem;
            border-radius: 20px;
            color: white;
            background: linear-gradient(135deg, #123a63, #1f78a8);
            margin-bottom: 1.5rem;
        }

        .hero h1 {
            margin: 0;
            font-size: 2.5rem;
        }

        .hero p {
            margin-top: 0.75rem;
            font-size: 1.05rem;
            color: #e3f2fd;
        }

        .feature-title {
            color: #123a63;
            font-weight: 700;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("Chest X-ray Assist")
    st.caption("Research prototype v0.1")

    st.divider()

    st.write("Backend API")
    st.code(API_BASE_URL, language=None)

    st.info(
        "Use the navigation links to open the patient or doctor interface."
    )

st.markdown(
    """
    <div class="hero">
        <h1>Chest X-ray Assist</h1>
        <p>
            A doctor-reviewed research platform for managing adult chest
            X-ray cases and pneumonia-analysis workflows.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.warning(SAFETY_NOTICE, icon="⚠️")

st.subheader("Select your workspace")

patient_column, doctor_column = st.columns(2)

with patient_column:
    with st.container(border=True):
        st.markdown(
            '<h3 class="feature-title">👤 Patient Portal</h3>',
            unsafe_allow_html=True,
        )
        st.write(
            "Create a case, upload a chest X-ray and check the "
            "doctor-review status."
        )
        st.page_link(
            "pages/1_Patient_Portal.py",
            label="Open Patient Portal",
            icon="➡️",
            use_container_width=True,
        )

with doctor_column:
    with st.container(border=True):
        st.markdown(
            '<h3 class="feature-title">🩺 Doctor Dashboard</h3>',
            unsafe_allow_html=True,
        )
        st.write(
            "Review submitted cases, inspect AI-assisted findings and "
            "approve or reject reports."
        )
        st.page_link(
            "pages/2_Doctor_Dashboard.py",
            label="Open Doctor Dashboard",
            icon="➡️",
            use_container_width=True,
        )

st.divider()

st.subheader("Prototype workflow")

workflow_columns = st.columns(4)

workflow_steps = [
    ("1", "Create case"),
    ("2", "Upload X-ray"),
    ("3", "AI preprocessing"),
    ("4", "Doctor review"),
]

for column, (number, label) in zip(workflow_columns, workflow_steps):
    with column:
        with st.container(border=True):
            st.metric(label=label, value=number)