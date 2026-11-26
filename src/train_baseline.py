
import pandas as pd
import joblib
import matplotlib.pyplot as plt

from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay
)

# Project paths
DATA_DIR = Path("data/processed")
MODEL_DIR = Path("models")
OUTPUT_DIR = Path("outputs")

MODEL_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# Load datasets
train_df = pd.read_csv(DATA_DIR / "train_cleaned.csv")
val_df = pd.read_csv(DATA_DIR / "validation_cleaned.csv")
test_df = pd.read_csv(DATA_DIR / "test_cleaned.csv")

# Category classification
X_train = train_df["cleaned_text"]
y_train = train_df["category"]

X_val = val_df["cleaned_text"]
y_val = val_df["category"]

X_test = test_df["cleaned_text"]
y_test = test_df["category"]

# TF-IDF vectorization
vectorizer = TfidfVectorizer(
    max_features=5000,
    ngram_range=(1, 2),
    sublinear_tf=True
)

X_train_vec = vectorizer.fit_transform(X_train)
X_val_vec = vectorizer.transform(X_val)
X_test_vec = vectorizer.transform(X_test)

# Train Logistic Regression
model = LogisticRegression(
    max_iter=1000,
    class_weight="balanced",
    random_state=42
)

model.fit(X_train_vec, y_train)

# Validation evaluation
val_predictions = model.predict(X_val_vec)
print("\nVALIDATION RESULTS")
print("Accuracy:", round(accuracy_score(y_val, val_predictions), 4))

# Final test evaluation
test_predictions = model.predict(X_test_vec)

accuracy = accuracy_score(y_test, test_predictions)

report = classification_report(
    y_test,
    test_predictions,
    zero_division=0
)

print("\nTEST RESULTS")
print("Accuracy:", round(accuracy, 4))
print("\nClassification Report:")
print(report)

# Save classification report
with open(OUTPUT_DIR / "classification_report.txt", "w") as file:
    file.write("BASELINE MODEL: TF-IDF + LOGISTIC REGRESSION\n\n")
    file.write(f"Test Accuracy: {accuracy:.4f}\n\n")
    file.write(report)

# Confusion matrix
labels = sorted(y_test.unique())

cm = confusion_matrix(
    y_test,
    test_predictions,
    labels=labels
)

display = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=labels
)

fig, ax = plt.subplots(figsize=(11, 8))
display.plot(ax=ax, xticks_rotation=45, cmap="Blues")
plt.title("Baseline Model - Confusion Matrix")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "confusion_matrix.png", dpi=300)
plt.close()

# Save sample predictions
results = test_df[["sample_id", "text", "category"]].copy()
results["predicted_category"] = test_predictions
results["correct_prediction"] = (
    results["category"] == results["predicted_category"]
)

results.to_csv(
    OUTPUT_DIR / "sample_predictions.csv",
    index=False,
    encoding="utf-8-sig"
)

# Save model and vectorizer
joblib.dump(model, MODEL_DIR / "baseline_model.pkl")
joblib.dump(vectorizer, MODEL_DIR / "tfidf_vectorizer.pkl")

print("\nBASELINE TRAINING COMPLETED!")
print("Model saved:", MODEL_DIR / "baseline_model.pkl")
print("Vectorizer saved:", MODEL_DIR / "tfidf_vectorizer.pkl")
print("Evaluation files saved in:", OUTPUT_DIR)
