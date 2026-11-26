import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

DATA_DIR = Path("data/processed")
MODEL_DIR = Path("models")
OUTPUT_DIR = Path("outputs")

train_df = pd.read_csv(DATA_DIR / "train_cleaned.csv")
val_df = pd.read_csv(DATA_DIR / "validation_cleaned.csv")
test_df = pd.read_csv(DATA_DIR / "test_cleaned.csv")

# Fit vectorizer only on training text
vectorizer = TfidfVectorizer(
    max_features=5000,
    ngram_range=(1, 2),
    sublinear_tf=True
)

X_train = vectorizer.fit_transform(train_df["cleaned_text"])
X_val = vectorizer.transform(val_df["cleaned_text"])
X_test = vectorizer.transform(test_df["cleaned_text"])

joblib.dump(vectorizer, MODEL_DIR / "attribute_vectorizer.pkl")

targets = ["sentiment", "priority"]

for target in targets:
    print(f"\n{'=' * 45}")
    print(f"TRAINING {target.upper()} MODEL")
    print("=" * 45)

    y_train = train_df[target].astype(str)
    y_val = val_df[target].astype(str)
    y_test = test_df[target].astype(str)

    model = LogisticRegression(
        max_iter=1000,
        class_weight="balanced",
        random_state=42
    )

    model.fit(X_train, y_train)

    val_predictions = model.predict(X_val)
    test_predictions = model.predict(X_test)

    print("\nValidation Accuracy:",
          round(accuracy_score(y_val, val_predictions), 4))

    print("\nTest Accuracy:",
          round(accuracy_score(y_test, test_predictions), 4))

    print("\nTest Classification Report:")
    report = classification_report(
        y_test,
        test_predictions,
        zero_division=0
    )

    print(report)

    # Save model
    joblib.dump(model, MODEL_DIR / f"{target}_model.pkl")

    # Save report
    with open(
        OUTPUT_DIR / f"{target}_classification_report.txt",
        "w",
        encoding="utf-8"
    ) as file:
        file.write(report)

    # Save confusion matrix
    labels = sorted(y_test.unique())
    matrix = confusion_matrix(
        y_test,
        test_predictions,
        labels=labels
    )

    plt.figure(figsize=(7, 5))
    sns.heatmap(
        matrix,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=labels,
        yticklabels=labels
    )
    plt.title(f"{target.title()} Confusion Matrix")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / f"{target}_confusion_matrix.png"
    )
    plt.close()

    print(f"\nSaved {target} model and evaluation files.")

print("\nSENTIMENT AND PRIORITY TRAINING COMPLETED!")