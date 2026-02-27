"""
Acuvia ML Training Module
Generates synthetic training data, trains a TF-IDF + Logistic Regression model,
and saves the model artifacts for use by the FastAPI backend.
"""

import os
import random
import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

# ---------------------------------------------------------------------------
# Symptom vocabulary, grouped by typical severity
# ---------------------------------------------------------------------------

LOW_SYMPTOMS = [
    "mild headache",
    "runny nose",
    "sneezing",
    "sore throat",
    "mild cough",
    "slight fatigue",
    "muscle soreness after exercise",
    "itchy eyes",
    "minor stomach upset",
    "occasional dizziness",
    "mild back pain",
    "dry skin",
    "minor joint stiffness",
    "mild nausea",
    "cold symptoms",
    "slight congestion",
    "scratchy throat",
    "watery eyes",
    "mild earache",
    "minor bruise",
]

MODERATE_SYMPTOMS = [
    "persistent cough with phlegm",
    "fever of 101",
    "moderate headache and nausea",
    "vomiting and diarrhea",
    "sharp abdominal pain",
    "wheezing and difficulty breathing",
    "high fever and chills",
    "joint pain and swelling",
    "persistent fatigue and weakness",
    "shortness of breath on exertion",
    "chest tightness",
    "blood in urine",
    "severe back pain",
    "recurrent dizziness",
    "persistent vomiting",
    "moderate dehydration",
    "swollen lymph nodes and fever",
    "painful urination with fever",
    "skin rash with fever",
    "numbness in extremities",
]

HIGH_SYMPTOMS = [
    "chest pain and sweating",
    "severe breathlessness at rest",
    "unconsciousness",
    "sudden severe headache and vision loss",
    "chest pain radiating to arm",
    "difficulty breathing and bluish lips",
    "sudden paralysis on one side",
    "uncontrolled bleeding",
    "severe allergic reaction with throat swelling",
    "seizures and loss of consciousness",
    "coughing up blood",
    "sudden confusion and slurred speech",
    "severe abdominal pain and vomiting blood",
    "high fever with stiff neck and confusion",
    "chest pain and shortness of breath",
    "crushing chest pressure",
    "sudden vision loss",
    "severe burns covering large area",
    "trauma with heavy blood loss",
    "diabetic emergency with confusion",
]


def _make_sample(symptom_pool: list[str], label: str, n_combos: int = 1) -> tuple[str, str]:
    """Create a single (symptom_text, label) sample."""
    chosen = random.sample(symptom_pool, min(n_combos, len(symptom_pool)))
    return ", ".join(chosen), label


def generate_dataset(n_per_class: int = 120) -> tuple[list[str], list[str]]:
    """Generate a balanced synthetic dataset."""
    texts: list[str] = []
    labels: list[str] = []

    for _ in range(n_per_class):
        # Low
        t, l = _make_sample(LOW_SYMPTOMS, "Low", random.randint(1, 3))
        texts.append(t)
        labels.append(l)

        # Moderate
        t, l = _make_sample(MODERATE_SYMPTOMS, "Moderate", random.randint(1, 3))
        texts.append(t)
        labels.append(l)

        # High
        t, l = _make_sample(HIGH_SYMPTOMS, "High", random.randint(1, 3))
        texts.append(t)
        labels.append(l)

    return texts, labels


def train_and_save(model_dir: str | None = None) -> tuple:
    """Train the model, print metrics, save artifacts, return (vectorizer, model)."""
    if model_dir is None:
        model_dir = os.path.dirname(os.path.abspath(__file__))

    random.seed(42)
    np.random.seed(42)

    print("=" * 60)
    print("  Acuvia ML — Training Pipeline")
    print("=" * 60)

    # 1. Generate data
    texts, labels = generate_dataset(n_per_class=150)
    print(f"\n[OK] Generated {len(texts)} training samples ({len(texts)//3} per class)")

    # 2. TF-IDF Vectorization
    vectorizer = TfidfVectorizer(max_features=500, ngram_range=(1, 2))
    X = vectorizer.fit_transform(texts)
    print(f"[OK] TF-IDF matrix shape: {X.shape}")

    # 3. Train / Test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, labels, test_size=0.2, random_state=42, stratify=labels
    )

    # 4. Logistic Regression
    model = LogisticRegression(max_iter=1000, random_state=42, multi_class="multinomial")
    model.fit(X_train, y_train)

    # 5. Evaluation
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"\n[OK] Accuracy: {acc:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    # 6. Save artifacts
    vectorizer_path = os.path.join(model_dir, "vectorizer.joblib")
    model_path = os.path.join(model_dir, "classifier.joblib")
    joblib.dump(vectorizer, vectorizer_path)
    joblib.dump(model, model_path)
    print(f"[OK] Saved vectorizer -> {vectorizer_path}")
    print(f"[OK] Saved classifier -> {model_path}")
    print("=" * 60)

    return vectorizer, model


if __name__ == "__main__":
    train_and_save()
