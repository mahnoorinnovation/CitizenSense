
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split

# Project paths
DATA_FILE = Path("data/labels.csv")
OUTPUT_DIR = Path("data/processed")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Load dataset
df = pd.read_csv(DATA_FILE)

# Basic quality checks
assert len(df) == 500, "Dataset must contain 500 records."
assert df["sample_id"].nunique() == 500, "Duplicate IDs found."

reviewed_count = (
    df["manual_reviewed"].astype(str).str.lower() == "true"
).sum()

assert reviewed_count >= 200, "At least 200 reviewed samples required."
assert df["category"].nunique() >= 4, "At least 4 categories required."

# 70% training and 30% temporary data
train_df, temp_df = train_test_split(
    df,
    test_size=0.30,
    random_state=42,
    stratify=df["category"]
)

# Split remaining 30% equally into validation and test
validation_df, test_df = train_test_split(
    temp_df,
    test_size=0.50,
    random_state=42,
    stratify=temp_df["category"]
)

# Assign split names
train_df = train_df.copy()
validation_df = validation_df.copy()
test_df = test_df.copy()

train_df["split"] = "train"
validation_df["split"] = "validation"
test_df["split"] = "test"

# Combine and save
final_df = pd.concat(
    [train_df, validation_df, test_df]
).sort_values("sample_id")

train_df.to_csv(OUTPUT_DIR / "train.csv", index=False, encoding="utf-8-sig")
validation_df.to_csv(OUTPUT_DIR / "validation.csv", index=False, encoding="utf-8-sig")
test_df.to_csv(OUTPUT_DIR / "test.csv", index=False, encoding="utf-8-sig")
final_df.to_csv(OUTPUT_DIR / "labels_with_splits.csv", index=False, encoding="utf-8-sig")

# Update master dataset with split assignments
df["split"] = df["sample_id"].map(
    final_df.set_index("sample_id")["split"]
)
df.to_csv(DATA_FILE, index=False, encoding="utf-8-sig")

# Display results
print("\nDATASET SPLITTING COMPLETED")
print("--------------------------------")
print("Training samples:", len(train_df))
print("Validation samples:", len(validation_df))
print("Testing samples:", len(test_df))
print("Total samples:", len(final_df))
print("\nCategory distribution:")
print(pd.crosstab(final_df["category"], final_df["split"]))
print("\nFiles saved in:", OUTPUT_DIR)
