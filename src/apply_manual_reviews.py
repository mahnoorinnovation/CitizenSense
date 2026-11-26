
import pandas as pd
import sys

REVIEW_FILE = "data/manual_review.csv"
MASTER_FILE = "data/labels.csv"
BATCH_SIZE = 10

review = pd.read_csv(REVIEW_FILE)
master = pd.read_csv(MASTER_FILE)

# Ensure review columns support text values
for col in [
    "reviewed_category",
    "reviewed_sentiment",
    "reviewed_priority",
    "review_status"
]:
    review[col] = review[col].astype("object")

# Display next pending batch
if len(sys.argv) < 2 or sys.argv[1].lower() == "show":
    pending = review[review["review_status"] != "Reviewed"].head(BATCH_SIZE)

    if pending.empty:
        print("All review samples completed!")
    else:
        print("\nNEXT 10 SAMPLES FOR REVIEW\n")
        print(pending[
            ["sample_id", "text", "original_category",
             "original_sentiment", "original_priority"]
        ].to_string(index=False))

    sys.exit()

# Apply the next batch after confirmation
if sys.argv[1].lower() == "apply":

    pending = review[review["review_status"] != "Reviewed"].head(BATCH_SIZE)

    if pending.empty:
        print("No pending samples.")
        sys.exit()

    ids = pending["sample_id"].tolist()

    for _, row in pending.iterrows():
        sid = row["sample_id"]

        category = row["original_category"]
        sentiment = row["original_sentiment"]
        priority = row["original_priority"]

        review.loc[review["sample_id"] == sid, [
            "reviewed_category",
            "reviewed_sentiment",
            "reviewed_priority"
        ]] = [category, sentiment, priority]

        review.loc[review["sample_id"] == sid, "review_status"] = "Reviewed"

        master.loc[master["sample_id"] == sid, [
            "category", "sentiment", "priority"
        ]] = [category, sentiment, priority]

        master.loc[master["sample_id"] == sid, "manual_reviewed"] = True

    review.to_csv(REVIEW_FILE, index=False, encoding="utf-8-sig")
    master.to_csv(MASTER_FILE, index=False, encoding="utf-8-sig")

    total = (
        master["manual_reviewed"].astype(str).str.lower() == "true"
    ).sum()

    print(f"\nSuccessfully reviewed {len(ids)} confirmed samples.")
    print(f"Total manually reviewed: {total}")
    print(f"Remaining: {len(review) - (review['review_status'] == 'Reviewed').sum()}")

else:
    print("Use: python src/apply_manual_reviews.py show")
    print("Or:  python src/apply_manual_reviews.py apply")
