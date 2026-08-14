import os


APP_NAME = "Chest X-ray Assist"

API_BASE_URL = os.getenv(
    "API_BASE_URL",
    "http://127.0.0.1:8000",
)

REQUEST_TIMEOUT_SECONDS = 15.0

SAFETY_NOTICE = (
    "Research prototype only. AI output must be reviewed and approved "
    "by a qualified doctor before it is shown to a patient."
)