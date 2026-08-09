# Chest X-ray Assist

An educational research prototype that helps qualified doctors review adult
chest X-rays for signs associated with pneumonia.

## Important safety boundary

- This project does not diagnose patients.
- AI output is a draft for doctor review.
- No result is released to a patient before doctor approval.
- Do not use real patient data during development.

## Technology

- FastAPI backend
- Streamlit patient and doctor interfaces (added in later steps)
- MySQL database (connected in Step 2)
- Local image-processing/model service (added in later steps)

## Step 1: run the backend

```bash
cd chest_xray_assist
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn backend.app.main:app --reload
```

Open:

- API status: http://127.0.0.1:8000/
- Interactive API docs: http://127.0.0.1:8000/docs

Run the first test:

```bash
pytest
```


# AI-Medical-Image-Analyzer
