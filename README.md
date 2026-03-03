# Acuvia – Precision Triage Powered by AI

An AI-driven clinical decision-support triage system that prioritizes patient risk based on symptoms, age, and comorbidities.

> ⚠️ **Acuvia is a triage support tool and not a medical diagnosis system.**

**Live Prototype:** https://acuvia-triage.web.app

---

## Project Overview

Acuvia analyzes user-reported symptoms (free-text) using an interpretable ML model and rule-based critical overrides to produce a risk score and risk-level suggestion for triage prioritization.

The system:

- Extracts symptoms from free-text input  
- Predicts risk probability using a trained ML model  
- Adjusts risk using demographic and health factors  
- Applies critical symptom overrides for emergency cases  
- Generates interpretable explanations for transparency  

Designed for clinical decision-support in triage and telehealth workflows.

---

## Tech Stack & Tools

### Frontend
- React (Vite)
- JavaScript (ES6+)
- CSS
- Fetch API

### Backend
- FastAPI
- Python 3.10+
- Uvicorn

### Machine Learning
- scikit-learn
- TF-IDF Vectorizer
- Logistic Regression
- joblib (model persistence)

### Other
- JSON-based logging
- Swagger (FastAPI docs)
- Node.js 18+

---

## Features

- Free-text symptom input  
- ML-based risk probability prediction  
- Risk score calculation using demographic modifiers  
- Critical symptom override logic  
- Explainable AI output  
- Assessment logging system  
- RESTful API architecture  
- Interactive Swagger documentation  

---

## Risk Scoring Formula

```
risk_score = (model_probability × 5) + age_factor + comorbidity_factor
```

### Risk Modifiers

| Factor           | Value |
|------------------|-------|
| Age > 60         | +2    |
| Age 40–60        | +1    |
| Each comorbidity | +1    |

### Critical Overrides (Automatic High Risk)

- Chest pain + sweating  
- Severe breathlessness  
- Unconsciousness / loss of consciousness  

---

## System Architecture

```
Frontend (React + Vite)
        │
        │ POST /assess
        ▼
Backend (FastAPI)
        │
        ├── Symptom Extraction
        ├── TF-IDF Vectorization
        ├── Logistic Regression Prediction
        ├── Risk Score Computation
        ├── Critical Override Check
        └── Explanation Generation
        │
        ▼
Response Returned to Frontend
```

---

## Backend Processing Flow

1. User submits symptoms via frontend.  
2. Backend extracts and preprocesses symptom text.  
3. TF-IDF vectorizer transforms text into feature vectors.  
4. Logistic Regression predicts probability of high risk.  
5. Risk score is computed using formula.  
6. Critical override logic checks emergency patterns.  
7. Explanation is generated.  
8. Assessment is logged in JSON file.  
9. Structured response returned to frontend.  

---

## Installation & Setup

### Prerequisites

- Python 3.10+  
- Node.js 18+  
- npm  

---

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8000
```

- API: http://localhost:8000  
- Swagger docs: http://localhost:8000/docs  
- ML model auto-trains on first startup  

---

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Open in browser:

```
http://localhost:5173
```

---

## API Endpoint

### POST `/assess`

#### Request Example

```json
{
  "age": 65,
  "symptoms": "chest pain with sweating and shortness of breath",
  "comorbidities": ["diabetes", "hypertension"]
}
```

#### Response Example

```json
{
  "risk_score": 8.2,
  "risk_level": "High",
  "probability": 0.84,
  "explanation": "High-risk symptoms detected with age and comorbidity factors applied."
}
```

---

## Project Structure

```
acuvia/
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── model/
│   │   ├── train.py
│   │   ├── vectorizer.joblib
│   │   └── classifier.joblib
│   └── logs/
│       └── assessments.json
├── frontend/
│   ├── package.json
│   ├── vite.config.js
│   ├── index.html
│   └── src/
│       ├── App.jsx
│       ├── pages/
│       │   ├── Home.jsx
│       │   ├── Assessment.jsx
│       │   └── Results.jsx
└── README.md
```

---

## Future Improvements

- Transformer-based NLP model  
- EHR integration  
- Cloud deployment with CI/CD  
- HIPAA-compliant logging and encryption  
- Multilingual symptom support  

---

## Disclaimer

Acuvia is a clinical decision-support triage tool and does not provide medical diagnoses. Always consult a licensed medical professional.
