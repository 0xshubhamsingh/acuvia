"""
Acuvia — FastAPI Backend
AI-powered symptom triage and risk prioritization API.
"""

import os
import re
import json
import datetime
from contextlib import asynccontextmanager

import joblib
import numpy as np
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "model")
LOG_DIR = os.path.join(BASE_DIR, "logs")
LOG_FILE = os.path.join(LOG_DIR, "assessments.json")

# ---------------------------------------------------------------------------
# Globals (populated on startup)
# ---------------------------------------------------------------------------
vectorizer = None
classifier = None

# ---------------------------------------------------------------------------
# Lifespan — load / train model on startup
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    global vectorizer, classifier

    vec_path = os.path.join(MODEL_DIR, "vectorizer.joblib")
    clf_path = os.path.join(MODEL_DIR, "classifier.joblib")

    if os.path.exists(vec_path) and os.path.exists(clf_path):
        vectorizer = joblib.load(vec_path)
        classifier = joblib.load(clf_path)
        print("[OK] Loaded existing model artifacts.")
    else:
        print("[*] No saved model found -- training now...")
        from model.train import train_and_save
        vectorizer, classifier = train_and_save(MODEL_DIR)

    os.makedirs(LOG_DIR, exist_ok=True)
    yield

# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------
app = FastAPI(
    title="Acuvia API",
    description="AI-powered symptom triage and risk prioritization.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------

class AssessmentRequest(BaseModel):
    age: int
    gender: str
    comorbidities: list[str] = []
    symptoms: str

class AssessmentResponse(BaseModel):
    risk_level: str
    risk_score: float
    explanation: str
    detected_symptoms: list[str]
    recommended_action: str

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

CRITICAL_PATTERNS: list[tuple[str, ...]] = [
    ("chest pain", "sweating"),
    ("severe breathlessness",),
    ("unconsciousness",),
    ("unconscious",),
    ("loss of consciousness",),
]

COMORBIDITY_ALIASES: dict[str, str] = {
    "diabetes": "diabetes",
    "hypertension": "hypertension",
    "heart disease": "heart disease",
    "asthma": "asthma",
    "copd": "COPD",
    "chronic kidney disease": "chronic kidney disease",
    "cancer": "cancer",
    "obesity": "obesity",
    "liver disease": "liver disease",
    "immunodeficiency": "immunodeficiency",
}

KNOWN_SYMPTOMS = [
    "headache", "fever", "cough", "sore throat", "nausea", "vomiting",
    "diarrhea", "fatigue", "weakness", "dizziness", "chest pain",
    "shortness of breath", "breathlessness", "sweating", "chills",
    "abdominal pain", "back pain", "joint pain", "muscle pain",
    "rash", "itching", "swelling", "numbness", "tingling",
    "blurred vision", "confusion", "seizure", "unconsciousness",
    "bleeding", "bruising", "painful urination", "blood in urine",
    "wheezing", "congestion", "runny nose", "sneezing",
    "chest tightness", "palpitations", "difficulty breathing",
    "loss of appetite", "weight loss", "night sweats",
    "stiff neck", "earache", "eye pain", "throat swelling",
]


def extract_symptoms(text: str) -> list[str]:
    """Extract recognisable symptom phrases from free-text."""
    text_lower = text.lower()
    found: list[str] = []
    for symptom in KNOWN_SYMPTOMS:
        if symptom in text_lower:
            found.append(symptom)
    # Also capture multi-word critical phrases
    for pattern_group in CRITICAL_PATTERNS:
        for p in pattern_group:
            if p in text_lower and p not in found:
                found.append(p)
    return list(dict.fromkeys(found))  # preserve order, dedupe


def check_critical_override(text: str) -> bool:
    """Return True if any critical symptom pattern is present."""
    text_lower = text.lower()
    for pattern_group in CRITICAL_PATTERNS:
        if all(p in text_lower for p in pattern_group):
            return True
    return False


def compute_age_factor(age: int) -> tuple[float, str]:
    if age > 60:
        return 2.0, f"Age {age} (above 60) increased risk by +2."
    elif age >= 40:
        return 1.0, f"Age {age} (40–60) increased risk by +1."
    else:
        return 0.0, f"Age {age} is within low-risk range."


def compute_comorbidity_factor(comorbidities: list[str]) -> tuple[float, str]:
    count = len(comorbidities)
    if count == 0:
        return 0.0, "No known comorbidities."
    names = ", ".join(comorbidities)
    return float(count), f"Presence of {names} contributed +{count} to severity."


def classify_risk(score: float, critical: bool) -> str:
    if critical:
        return "High"
    if score >= 7:
        return "High"
    elif score >= 4:
        return "Moderate"
    return "Low"


def recommended_action(level: str) -> str:
    actions = {
        "Low": "Self-care and monitoring recommended. Visit a healthcare provider if symptoms persist beyond 48 hours.",
        "Moderate": "Schedule an appointment with your healthcare provider within 24 hours. Monitor symptoms closely.",
        "High": "Seek immediate medical attention. Visit the nearest emergency department or call emergency services.",
    }
    return actions.get(level, actions["Moderate"])


def build_explanation(
    detected: list[str],
    age_info: str,
    comorbidity_info: str,
    risk_level: str,
    critical: bool,
) -> str:
    parts: list[str] = []

    if critical:
        parts.append(f"[!] Critical symptom pattern detected -- automatically classified as High Risk.")

    if detected:
        parts.append(f"{risk_level} risk due to detected symptoms: {', '.join(detected)}.")
    else:
        parts.append(f"{risk_level} risk based on symptom analysis.")

    parts.append(age_info)
    parts.append(comorbidity_info)
    return " ".join(parts)


def log_assessment(request_data: dict, response_data: dict) -> None:
    """Append assessment to JSON log file."""
    entry = {
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "request": request_data,
        "response": response_data,
    }
    try:
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                logs = json.load(f)
        else:
            logs = []
        logs.append(entry)
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            json.dump(logs, f, indent=2)
    except Exception as exc:
        print(f"[!] Logging failed: {exc}")

# ---------------------------------------------------------------------------
# Endpoint
# ---------------------------------------------------------------------------

@app.post("/assess", response_model=AssessmentResponse)
async def assess(req: AssessmentRequest):
    """Run triage assessment on patient input."""

    # 1. Extract symptoms from free-text
    detected = extract_symptoms(req.symptoms)

    # 2. Predict with ML model
    X = vectorizer.transform([req.symptoms])
    probas = classifier.predict_proba(X)[0]
    class_labels = list(classifier.classes_)

    # Get the max probability (used for risk score)
    high_idx = class_labels.index("High") if "High" in class_labels else -1
    model_prob = float(probas[high_idx]) if high_idx >= 0 else float(max(probas))

    # 3. Risk scoring factors
    age_factor, age_info = compute_age_factor(req.age)
    comorbidity_factor, comorbidity_info = compute_comorbidity_factor(req.comorbidities)

    # 4. Composite risk score
    risk_score = round((model_prob * 5) + age_factor + comorbidity_factor, 2)

    # 5. Critical override check
    critical = check_critical_override(req.symptoms)

    # 6. Classification
    risk_level = classify_risk(risk_score, critical)

    # 7. Explanation
    explanation = build_explanation(detected, age_info, comorbidity_info, risk_level, critical)

    # 8. Build response
    response = AssessmentResponse(
        risk_level=risk_level,
        risk_score=risk_score,
        explanation=explanation,
        detected_symptoms=detected,
        recommended_action=recommended_action(risk_level),
    )

    # 9. Log
    log_assessment(req.model_dump(), response.model_dump())

    return response


@app.get("/")
async def root():
    return {"service": "Acuvia API", "status": "running"}
