# CitizenSense
## NLP-Based Public Feedback Classification and Insight System

**Project:** AIRI Team — PITB AI Internship, Task 4  
**Project Type:** Natural Language Processing (NLP)  
**Interface:** Streamlit Dashboard

---

## 1. Introduction

CitizenSense is an NLP-based system designed to analyze public feedback and civic complaints. It helps classify submitted complaints into relevant categories and identify their sentiment and priority.

The system provides an interactive dashboard where users can submit complaint text and view the predicted category, sentiment, priority, confidence score, keywords, and suggested department.

## 2. Project Objectives

- Classify public complaints into relevant civic categories.
- Identify sentiment as Positive, Negative, or Neutral.
- Estimate complaint priority as High, Medium, or Low.
- Extract important keywords from complaint text.
- Evaluate machine learning and transformer-based approaches.
- Present predictions and evaluation results through a Streamlit dashboard.

## 3. Dataset Description

The project dataset contains **500 synthetic civic feedback samples**.

It includes eight complaint categories:

1. Education
2. General
3. Water Supply
4. Electricity
5. Roads / Infrastructure
6. Sanitation
7. Health
8. Traffic

The dataset was divided into:

| Dataset | Samples | Percentage |
|---|---:|---:|
| Training | 350 | 70% |
| Validation | 75 | 15% |
| Testing | 75 | 15% |
| **Total** | **500** | **100%** |

The project contains 200 records marked as manually reviewed. However, independent human annotation evidence is not yet established, so these records should not be presented as independently verified manual labels.

## 4. Data Preprocessing

The project includes a preprocessing workflow to prepare complaint text for machine learning.

The workflow includes:
- Text cleaning and normalization.
- Preparing processed complaint data.
- Creating training, validation, and testing datasets.
- Preparing text features for classification.

TF-IDF vectorization is used to convert text into numerical features for the baseline classification model.

## 5. Models Implemented

### 5.1 Baseline Machine Learning Model

The baseline category classifier uses:

- TF-IDF Vectorizer
- Logistic Regression

It predicts one of the eight complaint categories.

### 5.2 Sentiment and Priority Models

Additional classification models predict:

- Sentiment: Positive, Negative, Neutral.
- Priority: High, Medium, Low.

### 5.3 Transformer-Based Model

The project also uses the Hugging Face model:

`cardiffnlp/twitter-roberta-base-sentiment-latest`

It is used as a pretrained transformer sentiment-analysis pipeline.

## 6. Model Evaluation

Models were evaluated using accuracy, precision, recall, F1-score, and confusion matrices.

### 6.1 Baseline Category Classification

| Metric | Result |
|---|---:|
| Accuracy | 98.67% |
| Macro F1-score | 98.67% |
| Weighted F1-score | 98.67% |

The model correctly classified most test samples. Some confusion was observed between Water Supply and other categories, particularly Electricity.

### 6.2 Sentiment Classification

| Metric | Result |
|---|---:|
| Test Accuracy | 100% |
| Macro F1-score | 100% |
| Weighted F1-score | 100% |

### 6.3 Priority Classification

| Metric | Result |
|---|---:|
| Test Accuracy | 100% |
| Macro F1-score | 100% |
| Weighted F1-score | 100% |

### 6.4 Transformer Sentiment Classification

| Metric | Result |
|---|---:|
| Accuracy | 52% |
| Macro F1-score | 0.49 |
| Weighted F1-score | 0.48 |

The transformer pipeline performed less effectively on this dataset than the sentiment classification model.

**Evaluation note:** The perfect sentiment and priority scores require further independent validation. Since the dataset is synthetic, these results should not be interpreted as proof of equivalent real-world performance.

## 7. Error Analysis

The error analysis output contains 15 samples selected for review:

- 1 incorrectly classified sample.
- 14 correctly classified samples with low model confidence.

One identified classification error involved a Water Supply complaint being predicted as Electricity.

The analysis highlights the importance of reviewing ambiguous complaints and low-confidence predictions.

### Suggested Improvements

1. Collect and independently annotate real civic feedback.
2. Add more diverse examples for confusing complaint categories.
3. Review low-confidence predictions and improve the training data.

## 8. Keyword Extraction and Complaint Summary

CitizenSense extracts important keywords from submitted complaint text to help users understand the main issue.

The dashboard also displays a short text summary based on the complaint input.

Keyword extraction provides an additional way to inspect the key information in each complaint.

## 9. Streamlit Dashboard

The project includes an interactive Streamlit dashboard with five main sections:

1. **System Overview:** Introduction and system information.
2. **Complaint Intelligence:** Complaint input and prediction results.
3. **Model Performance:** Model evaluation metrics and charts.
4. **Dataset Insights:** Dataset information and category distribution.
5. **About CitizenSense:** Project information and limitations.

The Complaint Intelligence section displays category, sentiment, priority, confidence, keywords, summary, and suggested department.

The suggested department is an informational recommendation, not an official government routing decision.

## 10. Project Structure

The project is organized into the following main folders:

- `app/` — Streamlit application and demo files.
- `data/` — Dataset, annotation guidelines, and processed data.
- `models/` — Saved machine learning models and vectorizers.
- `notebooks/` — Notebook workspace.
- `outputs/` — Evaluation reports, predictions, and charts.
- `report/` — Final project documentation.
- `screenshots/` — Dashboard screenshots.
- `src/` — Data processing, training, and evaluation scripts.

## 11. Limitations

- The dataset consists of synthetic civic feedback rather than real public complaints.
- Independent human verification of the 200 records marked as reviewed has not been established.
- High scores on synthetic data may not represent performance on real-world complaints.
- The transformer sentiment pipeline achieved 52% accuracy on the available test set.
- Model confidence is an estimate and should not be treated as certainty.
- Suggested departments are informational and require human review.

## 12. Learning Outcomes

Through this project, the following practical concepts were applied:

- Text preprocessing and dataset preparation.
- TF-IDF feature extraction.
- Machine learning classification.
- Transformer-based sentiment analysis using Hugging Face.
- Model evaluation using classification metrics.
- Confusion matrix and error analysis.
- Streamlit dashboard development.
- Organizing a modular Python project.

## 13. Conclusion

CitizenSense demonstrates an end-to-end NLP workflow for analyzing civic feedback. It combines machine learning classification, transformer-based sentiment analysis, keyword extraction, model evaluation, and an interactive dashboard.

The project provides a foundation for a public feedback analysis system. Further work should focus on independently annotated real-world data, improved generalization, and additional evaluation before deployment in a real civic environment.

---

**Project:** CitizenSense  
**Internship:** AIRI Team — PITB  
**Task:** Task 4 — Final Project
