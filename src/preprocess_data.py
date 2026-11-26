
import re
import pandas as pd
from pathlib import Path

INPUT_DIR = Path("data/processed")
OUTPUT_DIR = Path("data/processed")

def clean_text(text):
    """Clean citizen feedback while preserving meaningful words."""
    text = str(text).lower()
    text = re.sub(r"http\S+|www\.\S+", "", text)
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

files = ["train.csv", "validation.csv", "test.csv"]

for filename in files:
    input_path = INPUT_DIR / filename
    df = pd.read_csv(input_path)

    # Preserve original text and create cleaned text
    df["cleaned_text"] = df["text"].apply(clean_text)

    output_path = OUTPUT_DIR / filename.replace(".csv", "_cleaned.csv")
    df.to_csv(output_path, index=False, encoding="utf-8-sig")

    print(f"\n{filename}")
    print("Records:", len(df))
    print("Empty cleaned texts:", df["cleaned_text"].eq("").sum())
    print("Saved:", output_path)

print("\nTEXT PREPROCESSING COMPLETED!")
