import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPORT = ROOT / "report"
OUTPUT = REPORT / "CitizenSense_Final_Report_Complete.md"

original = REPORT / "CitizenSense_Final_Report.md"
content = original.read_text(encoding="utf-8")
content = content.replace("â€”", "—")

csv_path = ROOT / "outputs" / "error_analysis_reviewed.csv"

def clean(value):
    return str(value or "").replace("|", "\\|").replace("\n", " ").strip()

with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
    cases = list(csv.DictReader(f))

rows = []
for item in cases:
    rows.append(
        "| " + " | ".join([
            clean(item.get("sample_id")),
            clean(item.get("text")),
            clean(item.get("actual_category")),
            clean(item.get("predicted_category")),
            clean(item.get("confidence")),
            clean(item.get("prediction_status")),
            clean(item.get("review_reason")),
        ]) + " |"
    )

appendix = r"""

---

# Final Report Addendum

## 14. Detailed Per-Class Evaluation

The following results are taken from the saved baseline classification report.

| Category | Precision | Recall | F1-score | Support |
|---|---:|---:|---:|---:|
| Education | 1.00 | 1.00 | 1.00 | 9 |
| Electricity | 0.90 | 1.00 | 0.95 | 9 |
| General | 1.00 | 1.00 | 1.00 | 9 |
| Health | 1.00 | 1.00 | 1.00 | 10 |
| Roads / Infrastructure | 1.00 | 1.00 | 1.00 | 10 |
| Sanitation | 1.00 | 1.00 | 1.00 | 10 |
| Traffic | 1.00 | 1.00 | 1.00 | 9 |
| Water Supply | 1.00 | 0.89 | 0.94 | 9 |

The baseline model achieved 98.67% accuracy on 75 test samples. Electricity has a precision of 0.90, while Water Supply has a recall of 0.89. These results indicate a small number of category-confusion errors.

## 15. Confusion Matrix Evidence

### Baseline Category Classifier

![Baseline category confusion matrix](../outputs/confusion_matrix.png)

### Sentiment Classifier

![Sentiment confusion matrix](../outputs/sentiment_confusion_matrix.png)

### Priority Classifier

![Priority confusion matrix](../outputs/priority_confusion_matrix.png)

These figures provide visual evidence of the saved evaluation results.

## 16. Detailed Preliminary Error Analysis

The following 15 records were selected from the saved error-analysis output. They consist of one misclassification and fourteen correct predictions with low confidence.

**Review status:** This is an AI-assisted preliminary text review. The records have not yet been independently verified by a human reviewer. The explanations are plausible text-based observations, not confirmed explanations of the model's internal behaviour.

| Sample ID | Complaint Text | Actual Category | Predicted Category | Confidence | Status | Preliminary Review Reason |
|---|---|---|---|---:|---| 
""" + "\n".join(rows) + r"""

### Error Analysis Interpretation

- One sample, CS-0131, was misclassified: a Water Supply complaint was predicted as Electricity.
- Fourteen other samples were correctly classified but had relatively low prediction confidence.
- Some complaint texts contain generic wording and limited supporting context.
- Streetlight complaints may contain overlapping infrastructure and electricity-related terms.
- These observations suggest that more varied and independently labelled examples may improve category separation.

### Recommended Improvements

1. Collect real civic complaints from appropriate sources, remove personal information, and obtain independent human annotations.
2. Add more diverse examples for categories with overlapping vocabulary, especially Water Supply, Electricity, and Roads / Infrastructure.
3. Review low-confidence predictions with a human-in-the-loop process and use verified corrections to improve future training data.

## 17. Dashboard Screenshots

### System Overview

![System Overview](../screenshots/01_system_overview.png)

### Complaint Intelligence

![Complaint Intelligence](../screenshots/02_complaint_intelligence.png)

### Model Performance

![Model Performance](../screenshots/03_model_performance.png)

### Dataset Insights

![Dataset Insights](../screenshots/04_dataset_insights.png)

### About CitizenSense

![About CitizenSense](../screenshots/05_about_citizensense.png)

## 18. Project Links

- **GitHub Repository:** https://github.com/mahnoorinnovation/CitizenSense
- **Live Streamlit Dashboard:** https://citizensense-hae5xfzbtnar2wq9tka4x2.streamlit.app/

## 19. LinkedIn-Ready Project Summary

**CitizenSense — NLP-Based Public Feedback Classification and Insight System**

Developed an end-to-end NLP project as part of the AIRI Team PITB AI Internship. The system analyzes synthetic civic feedback using TF-IDF and Logistic Regression for complaint-category classification, classification models for sentiment and priority, and a pretrained Hugging Face transformer pipeline for sentiment analysis.

Implemented text preprocessing, model evaluation, confusion matrices, preliminary error analysis, keyword extraction, complaint summaries, and an interactive Streamlit dashboard.

**Technologies:** Python, Pandas, Scikit-learn, TF-IDF, Logistic Regression, Hugging Face Transformers, Streamlit.

**Key evaluation result:** The baseline category classifier achieved 98.67% accuracy on a held-out test set of 75 synthetic samples. Results require further validation on independently labelled real-world data.

## 20. Final Evaluation and Limitations

The category baseline achieved 98.67% accuracy. The sentiment and priority classifiers each achieved 100% accuracy on the available synthetic test set. The pretrained transformer sentiment pipeline achieved 52% accuracy, with a weighted F1-score of 0.48.

Perfect sentiment and priority scores on synthetic data should be interpreted cautiously. They do not establish real-world generalization. Independent human annotation evidence for the 200 records marked as reviewed has not been established. The 15 preliminary error-analysis records also remain pending human verification.

The suggested department is informational guidance only. Predictions and priority estimates should be reviewed by people before any real public-service decision.

## 21. Final Conclusion

CitizenSense demonstrates a practical NLP workflow that combines text processing, machine learning, transformer-based sentiment analysis, evaluation, preliminary error analysis, keyword extraction, summarization, and an interactive dashboard.

The project provides a working prototype and a foundation for further development. The next important steps are independent human annotation, testing on real-world civic feedback, reviewing low-confidence predictions, and validating the system with broader data.

---

**Project:** CitizenSense  
**Internship:** AIRI Team — PITB  
**Task:** Task 4 — Final Project
"""

OUTPUT.write_text(content + appendix, encoding="utf-8")

print("Complete report created:", OUTPUT)
print("Error-analysis records included:", len(cases))
print("Original report preserved:", original.exists())
