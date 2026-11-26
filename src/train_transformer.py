import pandas as pd
from pathlib import Path
from transformers import pipeline
from sklearn.metrics import accuracy_score, classification_report

DATA_DIR = Path("data/processed")
OUTPUT_DIR = Path("outputs")

print("Loading Hugging Face Transformer model...")

classifier = pipeline(
    "sentiment-analysis",
    model="cardiffnlp/twitter-roberta-base-sentiment-latest",
    device=-1
)

test_df = pd.read_csv(DATA_DIR / "test_cleaned.csv")

texts = test_df["text"].astype(str).tolist()
actual = test_df["sentiment"].str.lower().tolist()

print("Predicting sentiment on test data...")

results = classifier(texts, batch_size=16, truncation=True)

predicted = []

for result in results:
    label = result["label"].lower()

    if label.startswith("label_"):
        label_id = int(label.split("_")[1])
        label = classifier.model.config.id2label[label_id].lower()

    predicted.append(label)

print("\nTRANSFORMER TEST RESULTS")
print("------------------------")

print("Test Accuracy:",
      round(accuracy_score(actual, predicted), 4))

print("\nClassification Report:")
report = classification_report(
    actual,
    predicted,
    labels=["negative", "neutral", "positive"],
    zero_division=0
)

print(report)

with open(
    OUTPUT_DIR / "transformer_classification_report.txt",
    "w",
    encoding="utf-8"
) as file:
    file.write(report)

output = test_df[["sample_id", "text", "sentiment"]].copy()
output["transformer_prediction"] = predicted

output.to_csv(
    OUTPUT_DIR / "transformer_predictions.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nTransformer evaluation files saved!")