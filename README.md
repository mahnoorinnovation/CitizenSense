# CitizenSense
### NLP-Based Public Feedback Classification and Insight System

CitizenSense is an NLP-based application designed to analyze public feedback and extract meaningful insights from citizens' complaints. It helps identify complaint categories, sentiment, priority levels, important keywords, and suggested departments through an interactive Streamlit dashboard.

---

## 1. Project Overview

Public feedback often contains useful information about problems related to civic services, infrastructure, education, healthcare, and other public facilities. Manually analyzing large amounts of feedback can be time-consuming.

CitizenSense uses Natural Language Processing and Machine Learning techniques to organize and analyze this feedback.

The system provides predictions and insights to support better understanding of public complaints. It is an internship project developed as part of the AIRI Team PITB AI Internship.

## 2. Key Features

- **Complaint Classification:** Categorizes feedback into eight complaint categories.
- **Sentiment Analysis:** Identifies positive, negative, and neutral sentiment.
- **Priority Prediction:** Predicts the priority level of a complaint.
- **Keyword Extraction:** Extracts important words from submitted feedback.
- **Short Summary:** Provides a concise text summary.
- **Department Suggestions:** Displays a suggested department or action area.
- **Interactive Dashboard:** Allows users to submit feedback and view predictions.
- **Model Evaluation:** Includes classification reports, confusion matrices, and error analysis.

## 3. Complaint Categories

The dataset contains eight categories:

1. Education
2. General
3. Water Supply
4. Electricity
5. Roads / Infrastructure
6. Sanitation
7. Health
8. Traffic

## 4. Dataset Information

| Dataset property | Current details |
|---|---:|
| Total samples | 500 |
| Complaint categories | 8 |
| Training samples | 350 (70%) |
| Validation samples | 75 (15%) |
| Testing samples | 75 (15%) |
| Duplicate feedback texts | 0 |
| Missing values | 0 |

**Dataset note:** The current dataset contains synthetic public-feedback examples. The 200-sample human annotation requirement is not yet independently verified and remains pending. Automatically generated labels should not be presented as manually verified labels.

Additional documentation is available in:

- `data/DATASET_NOTES.md`
- `data/ANNOTATION_GUIDELINES.md`

## 5. Models and Techniques

CitizenSense uses the following technologies and approaches:

- **TF-IDF Vectorization:** Converts text into numerical features.
- **Scikit-learn Baseline:** Used for complaint-category classification.
- **Attribute Models:** Used for sentiment and priority prediction.
- **Hugging Face Transformer Pipeline:** Uses a pre-trained RoBERTa-based sentiment pipeline.
- **Error Analysis:** Identifies incorrect and low-confidence predictions.

The transformer pipeline uses `cardiffnlp/twitter-roberta-base-sentiment-latest`.

## 6. Model Evaluation

The project includes evaluation reports for category classification, sentiment analysis, priority prediction, and transformer-based sentiment analysis.

| Model / Task | Accuracy |
|---|---:|
| Category baseline | 98.67% |
| Sentiment baseline | 100% |
| Priority baseline | 100% |
| RoBERTa sentiment pipeline | 52% |

**Important evaluation note:** The high baseline scores should be interpreted cautiously because the dataset is synthetic. Further testing on independently collected and manually labeled feedback is needed to establish real-world performance.

Evaluation outputs are stored in the `outputs/` directory, including:

- Classification reports
- Confusion matrices
- Transformer predictions
- Sample predictions
- Error analysis results

## 7. Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- Hugging Face Transformers
- PyTorch
- Streamlit
- Matplotlib
- Seaborn
- NLTK
- Joblib

## 8. Project Structure

```text
citizensense_nlp_task4/
│
├── app/
│   ├── api.py
│   ├── demo.py
│   ├── streamlit_app.py
│   └── utils.py
│
├── data/
│   ├── labels.csv
│   ├── manual_review.csv
│   ├── ANNOTATION_GUIDELINES.md
│   ├── DATASET_NOTES.md
│   └── processed/
│
├── models/
│   ├── baseline_model.pkl
│   ├── tfidf_vectorizer.pkl
│   ├── attribute_vectorizer.pkl
│   ├── sentiment_model.pkl
│   └── priority_model.pkl
│
├── notebooks/
├── outputs/
├── report/
├── screenshots/
│
├── src/
│   ├── generate_dataset.py
│   ├── preprocess_data.py
│   ├── split_dataset.py
│   ├── apply_manual_reviews.py
│   ├── train_baseline.py
│   ├── train_attribute_models.py
│   ├── train_transformer.py
│   └── error_analysis.py
│
├── main.py
├── requirements.txt
└── README.md
```

## 9. Installation and Execution

### Step 1: Clone the repository

```bash
git clone YOUR_REPOSITORY_URL
cd citizensense_nlp_task4
```

Replace `YOUR_REPOSITORY_URL` with the actual repository URL.

### Step 2: Create a virtual environment

```bash
python -m venv .venv
```

### Step 3: Activate the environment

**Windows PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

### Step 4: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Run the Streamlit dashboard

```bash
streamlit run app/streamlit_app.py
```

The application will open in your browser.

## 10. Limitations

- The current dataset consists of synthetic feedback examples.
- Independent human verification of at least 200 samples remains pending.
- High baseline scores may reflect patterns in the generated dataset and should not be treated as proof of real-world accuracy.
- Transformer sentiment predictions require further evaluation.
- Department suggestions are informational and are not official government decisions.
- Model predictions are suggestions and should be reviewed by humans before any action is taken.

## 11. Future Improvements

- Collect real-world public feedback data.
- Complete independent human annotation.
- Fine-tune transformer models on a verified dataset.
- Improve model generalization and error handling.
- Expand evaluation using diverse real-world feedback.
- Improve deployment and monitoring capabilities.

## 12. Project Purpose

CitizenSense demonstrates how Natural Language Processing and Machine Learning can be applied to public feedback analysis. It provides an interactive way to organize complaints and generate useful insights while highlighting the importance of reliable data, model evaluation, and human oversight.

---

**Project:** CitizenSense — NLP-Based Public Feedback Classification and Insight System  
**Internship:** AIRI Team PITB AI Internship  
**Status:** Development and evaluation stage
