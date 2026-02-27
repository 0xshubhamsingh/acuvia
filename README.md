# Acuvia — Precision Triage. Powered by AI.

An AI-driven symptom triage and risk prioritization system. This is a **clinical decision-support triage tool**, not a diagnosis system.

Live Prototype: https://acuvia-triage.web.app

---

## Architecture

```
┌────────────────────────────────────────────────────────────┐
│                        Frontend                            │
│               React + Vite (port 5173)                     │
│   ┌──────────┐  ┌──────────────┐  ┌──────────────┐        │
│   │   Home   │→ │  Assessment  │→ │   Results    │        │
│   └──────────┘  └──────┬───────┘  └──────────────┘        │
│                        │  POST /assess                     │
└────────────────────────┼───────────────────────────────────┘
                         │
┌────────────────────────┼───────────────────────────────────┐
│                  Backend (FastAPI, port 8000)               │
│                        ▼                                   │
│   ┌─────────────────────────────────────┐                  │
│   │         /assess  Endpoint           │                  │
│   │  1. Extract symptoms from text      │                  │
│   │  2. TF-IDF → ML prediction          │                  │
│   │  3. Compute risk score              │                  │
│   │  4. Critical symptom override       │                  │
│   │  5. Generate explanation            │                  │
│   └─────────────────┬───────────────────┘                  │
│                     │                                      │
│   ┌─────────────────▼───────────────────┐                  │
│   │  ML Model (Logistic Regression)     │                  │
│   │  TF-IDF Vectorizer (scikit-learn)   │                  │
│   └─────────────────────────────────────┘                  │
│                                                            │
│   ┌─────────────────────────────────────┐                  │
│   │  JSON Assessment Logs               │                  │
│   │  logs/assessments.json              │                  │
│   └─────────────────────────────────────┘                  │
└────────────────────────────────────────────────────────────┘
```

## Risk Scoring Formula

```
risk_score = (model_probability × 5) + age_factor + comorbidity_factor
```

| Factor           | Value |
|------------------|-------|
| Age > 60         | +2    |
| Age 40–60        | +1    |
| Each comorbidity | +1    |

**Critical Overrides** → Automatically classified as **High Risk**:
- Chest pain + sweating
- Severe breathlessness
- Unconsciousness / loss of consciousness

---

## Setup

### Prerequisites

- Python 3.10+
- Node.js 18+

### Backend

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8000
```

The ML model trains automatically on first startup. Swagger docs available at `http://localhost:8000/docs`.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173` in your browser.

---

## Project Structure

```
acuvia/
├── backend/
│   ├── main.py                 # FastAPI app & /assess endpoint
│   ├── requirements.txt        # Python dependencies
│   ├── model/
│   │   ├── __init__.py
│   │   ├── train.py            # ML training pipeline
│   │   ├── vectorizer.joblib   # (generated) TF-IDF model
│   │   └── classifier.joblib   # (generated) LR classifier
│   └── logs/
│       └── assessments.json    # (generated) assessment log
├── frontend/
│   ├── package.json
│   ├── vite.config.js
│   ├── index.html
│   └── src/
│       ├── main.jsx
│       ├── App.jsx
│       ├── index.css
│       └── pages/
│           ├── Home.jsx
│           ├── Assessment.jsx
│           └── Results.jsx
└── README.md
```

---

## Disclaimer

> Acuvia is a triage support tool and not a medical diagnosis system. Always consult a licensed medical professional.
