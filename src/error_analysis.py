
import pandas as pd
import joblib

from pathlib import Path

DATA_DIR = Path("data/processed")
MODEL_DIR = Path("models")
OUTPUT_DIR = Path("outputs")

# Load model, vectorizer and test dataset
model = joblib.load(MODEL_DIR / "baseline_model.pkl")
vectorizer = joblib.load(MODEL_DIR / "tfidf_vectorizer.pkl")

test_df = pd.read_csv(DATA_DIR / "test_cleaned.csv")

# Generate predictions and confidence scores
X_test = vectorizer.transform(test_df["cleaned_text"])

predictions = model.predict(X_test)
probabilities = model.predict_proba(X_test)
confidence = probabilities.max(axis=1)

# Create analysis dataframe
analysis = test_df[
    ["sample_id", "text", "category"]
].copy()

analysis["predicted_category"] = predictions
analysis["confidence"] = confidence.round(4)
analysis["correct_prediction"] = (
    analysis["category"] == analysis["predicted_category"]
)

analysis["analysis_type"] = analysis["correct_prediction"].map(
    {False: "Misclassified", True: "Low-confidence review"}
)

# Select all incorrect predictions first,
# then the lowest-confidence correct predictions
errors = analysis[~analysis["correct_prediction"]]
uncertain = analysis[analysis["correct_prediction"]].sort_values(
    "confidence"
)

selected = pd.concat(
    [errors, uncertain.head(max(0, 15 - len(errors)))]
).head(15)

# Save results
selected.to_csv(
    OUTPUT_DIR / "error_analysis.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nERROR ANALYSIS COMPLETED")
print("------------------------")
print("Total test samples:", len(analysis))
print("Incorrect predictions:", len(errors))
print("Correct predictions:", len(analysis) - len(errors))
print("Samples selected for analysis:", len(selected))

print("\nSelected samples:")
print(
    selected[
        ["sample_id", "category", "predicted_category",
         "confidence", "analysis_type"]
    ].to_string(index=False)
)

print("\nSaved: outputs/error_analysis.csv")
