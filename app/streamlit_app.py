
import re
import html
from pathlib import Path
from collections import Counter

import joblib
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="CitizenSense | Public Feedback Intelligence",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "labels.csv"
MODEL_PATH = ROOT / "models"


# =========================================================
# THEME
# =========================================================

ORANGE = "#0F5B5A"
GOLD = "#D6B56D"
CREAM = "#F7F6F0"
CHARCOAL = "#263735"
MUTED = "#71817D"
PALETTE = [ORANGE, GOLD, "#4F8580", "#E5D8BD",
           "#78685B", "#C88B5A", "#B9A18A", "#5C5149"]

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background: #F7F6F0;
    color: #263735;
}

[data-testid="stSidebar"] {
    background: #263735;
    border-right: 1px solid #514D45;
}

[data-testid="stSidebar"] * {
    color: #F7F6F0 !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label {
    background: #344B48;
    border: 1px solid #514D45;
    padding: 12px 15px;
    border-radius: 10px;
    margin: 5px 0;
    transition: 0.2s;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) {
    background: #0F5B5A;
    border-color: #0F5B5A;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label p {
    font-weight: 600;
}

.main-title {
    font-size: 34px;
    font-weight: 800;
    color: #263735;
    margin-bottom: 2px;
}

.subtitle {
    color: #71817D;
    font-size: 14px;
    margin-bottom: 25px;
}

.section-title {
    font-size: 21px;
    font-weight: 800;
    color: #263735;
    margin-top: 20px;
    margin-bottom: 12px;
}

.metric-card {
    background: #FFFFFF;
    border: 1px solid #E3E0D4;
    border-radius: 15px;
    padding: 20px;
    min-height: 115px;
    box-shadow: 0 3px 12px rgba(41,39,37,0.04);
}

.metric-label {
    font-size: 13px;
    color: #71817D;
    font-weight: 600;
}

.metric-value {
    font-size: 30px;
    font-weight: 800;
    color: #263735;
    margin-top: 7px;
}

.metric-note {
    color: #4F8580;
    font-size: 12px;
    margin-top: 3px;
}

.info-card {
    background: #FFFFFF;
    border: 1px solid #E3E0D4;
    border-radius: 14px;
    padding: 18px;
    margin-bottom: 12px;
}

.small-heading {
    color: #4F8580;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 1px;
    text-transform: uppercase;
}

.stButton > button {
    background: #0F5B5A;
    color: white;
    border: none;
    border-radius: 9px;
    font-weight: 700;
    padding: 10px 22px;
}

.stButton > button:hover {
    background: #104746;
    color: white;
    border: none;
}

div[data-testid="stTextArea"] textarea {
    background: #FFFFFF;
    border: 1px solid #DED2C3;
    border-radius: 10px;
    color: #263735;
}

hr {
    border-color: #E3E0D4;
}

/* OCEAN BLUE GRADIENT THEME */
.main-title {
    background: linear-gradient(110deg, #263735, #0F5B5A, #D6B56D);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.metric-card {
    background: linear-gradient(135deg, #FFFFFF 65%, #F7F6F0 100%);
    border: 1px solid #E3E0D4;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #263735 0%, #344F61 100%);
}

[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) {
    background: linear-gradient(110deg, #0F5B5A, #66899C);
    border-color: #D6B56D;
}

.stButton > button {
    background: linear-gradient(110deg, #0F5B5A, #66899C);
    color: #FFFFFF;
    border: none;
}

.stButton > button:hover {
    background: linear-gradient(110deg, #104746, #0F5B5A);
    color: #FFFFFF;
    border: none;
}

/* OPTION 05 DEEP TEAL GRADIENT THEME */
.main-title {
    background: linear-gradient(110deg, #263735, #0F5B5A, #D6B56D);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.metric-card {
    background: linear-gradient(135deg, #FFFFFF 65%, #F7F6F0 100%);
    border: 1px solid #E3E0D4;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #263735 0%, #104746 100%);
}

[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) {
    background: linear-gradient(110deg, #0F5B5A, #4F8580);
    border-color: #D6B56D;
}

.stButton > button {
    background: linear-gradient(110deg, #0F5B5A, #4F8580);
    color: #FFFFFF;
    border: none;
}

.stButton > button:hover {
    background: linear-gradient(110deg, #104746, #0F5B5A);
    color: #FFFFFF;
    border: none;
}

/* DEEP TEAL + SOFT GOLD: INPUT, TABLES AND DOWNLOAD */

/* Section headings */
.section-title {
    color: #0F5B5A !important;
}

/* Complaint input label */
div[data-testid="stTextArea"] label,
div[data-testid="stTextArea"] label p {
    color: #0F5B5A !important;
    font-weight: 700 !important;
}

/* Evaluation Summary and Dataset Preview tables */
[data-testid="stDataFrame"] {
    background: #F7F6F0 !important;
    border: 1px solid #D6B56D !important;
    border-radius: 10px !important;
    overflow: hidden;
    color-scheme: light !important;

    --gdg-bg-cell: #F7F6F0;
    --gdg-text-dark: #263735;
    --gdg-text-medium: #344B48;
    --gdg-text-light: #4F8580;
    --gdg-bg-header: #0F5B5A;
    --gdg-text-header: #FFFFFF;
    --gdg-bg-header-hovered: #104746;
    --gdg-border-color: #D6B56D;
}

/* Download button */
[data-testid="stDownloadButton"] button {
    background: linear-gradient(110deg, #0F5B5A, #4F8580) !important;
    color: #FFFFFF !important;
    border: 1px solid #0F5B5A !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
}

[data-testid="stDownloadButton"] button p,
[data-testid="stDownloadButton"] button span {
    color: #FFFFFF !important;
}

[data-testid="stDownloadButton"] button:hover {
    background: #104746 !important;
    color: #FFFFFF !important;
}

/* Citizen feedback example text visibility */
div[data-testid="stTextArea"] textarea::placeholder {
    color: #263735 !important;
    opacity: 1 !important;
}
</style>
""", unsafe_allow_html=True)


# =========================================================
# DATA LOADING
# =========================================================

@st.cache_data
def load_dataset():
    if DATA_PATH.exists():
        return pd.read_csv(DATA_PATH)
    return pd.DataFrame()


@st.cache_resource
def load_models():
    files = {
        "category_model": MODEL_PATH / "baseline_model.pkl",
        "category_vectorizer": MODEL_PATH / "tfidf_vectorizer.pkl",
        "attribute_vectorizer": MODEL_PATH / "attribute_vectorizer.pkl",
        "sentiment_model": MODEL_PATH / "sentiment_model.pkl",
        "priority_model": MODEL_PATH / "priority_model.pkl"
    }

    loaded = {}
    for key, path in files.items():
        if path.exists():
            try:
                loaded[key] = joblib.load(path)
            except Exception:
                loaded[key] = None
        else:
            loaded[key] = None

    return loaded


df = load_dataset()
models = load_models()


# =========================================================
# TEXT UTILITIES
# =========================================================

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"http\S+|www\S+", " ", text)
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def extract_keywords(text, count=5):
    stopwords = {
        "the", "is", "are", "was", "were", "a", "an", "and",
        "or", "to", "of", "in", "on", "for", "with", "this",
        "that", "it", "my", "our", "i", "we", "please", "would",
        "like", "have", "has", "been", "be", "at", "as", "by",
        "from", "due", "its", "their", "they", "me", "there"
    }

    words = re.findall(r"\b[a-zA-Z]{3,}\b", str(text).lower())
    words = [word for word in words if word not in stopwords]

    counts = Counter(words)
    return [word for word, _ in counts.most_common(count)]


def make_summary(text):
    text = str(text).strip()
    if not text:
        return "No complaint text provided."

    sentences = re.split(r"(?<=[.!?])\s+", text)
    summary = sentences[0].strip()

    if len(summary) > 180:
        summary = summary[:177].rstrip() + "..."

    return summary


def predict_complaint(text):
    cleaned = clean_text(text)

    results = {
        "category": "Unavailable",
        "sentiment": "Unavailable",
        "priority": "Unavailable",
        "confidence": None,
        "keywords": extract_keywords(text),
        "summary": make_summary(text)
    }

    if models["category_model"] is not None and models["category_vectorizer"] is not None:
        vector = models["category_vectorizer"].transform([cleaned])
        category_model = models["category_model"]

        results["category"] = str(category_model.predict(vector)[0])

        if hasattr(category_model, "predict_proba"):
            probabilities = category_model.predict_proba(vector)[0]
            results["confidence"] = float(np.max(probabilities))

    if models["sentiment_model"] is not None and models["attribute_vectorizer"] is not None:
        vector = models["attribute_vectorizer"].transform([cleaned])
        results["sentiment"] = str(
            models["sentiment_model"].predict(vector)[0]
        )

    if models["priority_model"] is not None and models["attribute_vectorizer"] is not None:
        vector = models["attribute_vectorizer"].transform([cleaned])
        results["priority"] = str(
            models["priority_model"].predict(vector)[0]
        )

    return results


# =========================================================
# CHART UTILITIES
# =========================================================

def chart_theme(ax):
    ax.set_facecolor("#FFFFFF")
    ax.figure.set_facecolor("#FFFFFF")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_color("#E3E0D4")
    ax.tick_params(axis="both", colors=MUTED, labelsize=9)
    ax.grid(axis="x", alpha=0.15, linestyle="--")
    ax.set_axisbelow(True)


def show_category_chart(data):
    counts = data["category"].value_counts().sort_values()

    fig, ax = plt.subplots(figsize=(9, 4.5))
    bars = ax.barh(
        counts.index.astype(str),
        counts.values,
        color=[ORANGE if i == len(counts)-1 else GOLD
               for i in range(len(counts))],
        height=0.62
    )

    chart_theme(ax)
    ax.set_title("Complaints by Category", loc="left",
                 fontsize=15, fontweight="bold", color=CHARCOAL, pad=18)
    ax.set_xlabel("Number of samples", color=MUTED)

    for bar in bars:
        width = bar.get_width()
        ax.text(width + 0.5, bar.get_y() + bar.get_height()/2,
                str(int(width)), va="center", fontsize=9, color=CHARCOAL)

    ax.set_xlim(0, max(counts.values) * 1.16)
    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)


def show_donut_chart(data, column, title, color_map):
    counts = data[column].fillna("Unknown").value_counts()

    fig, ax = plt.subplots(figsize=(5, 4))
    colors = [color_map.get(str(label), GOLD) for label in counts.index]

    wedges, _ = ax.pie(
        counts.values,
        startangle=90,
        colors=colors,
        wedgeprops={"width": 0.38, "edgecolor": "white", "linewidth": 3}
    )

    total = int(counts.sum())
    ax.text(0, 0.08, str(total), ha="center", va="center",
            fontsize=23, fontweight="bold", color=CHARCOAL)
    ax.text(0, -0.17, "Samples", ha="center", va="center",
            fontsize=9, color=MUTED)

    ax.set_title(title, fontsize=14, fontweight="bold",
                 color=CHARCOAL, pad=14)

    legend_labels = [
        f"{label}: {value} ({value/total:.0%})"
        for label, value in counts.items()
    ]

    ax.legend(
        wedges, legend_labels,
        loc="lower center",
        bbox_to_anchor=(0.5, -0.15),
        frameon=False,
        fontsize=9
    )

    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)


def show_performance_chart():
    names = ["Category\nBaseline", "Sentiment\nBaseline",
             "Priority\nBaseline", "RoBERTa\nSentiment"]
    scores = [98.67, 100, 100, 52]

    fig, ax = plt.subplots(figsize=(9, 4.5))
    colors = [ORANGE, GOLD, GOLD, "#4F8580"]

    bars = ax.bar(names, scores, color=colors, width=0.58)

    chart_theme(ax)
    ax.set_title("Test Accuracy by Model", loc="left",
                 fontsize=15, fontweight="bold", color=CHARCOAL, pad=18)
    ax.set_ylabel("Accuracy (%)", color=MUTED)
    ax.set_ylim(0, 115)
    ax.set_yticks([0, 20, 40, 60, 80, 100])

    for bar, score in zip(bars, scores):
        ax.text(bar.get_x() + bar.get_width()/2, score + 2,
                f"{score:.2f}%", ha="center", fontsize=10,
                fontweight="bold", color=CHARCOAL)

    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:
    st.markdown(
        "<h1 style='font-size:27px;margin-bottom:0;'>🌐 CitizenSense</h1>",
        unsafe_allow_html=True
    )
    st.caption("PUBLIC FEEDBACK INTELLIGENCE")
    st.markdown("---")

    selected_page = st.radio(
        "NAVIGATION",
        [
            "System Overview",
            "Complaint Intelligence",
            "Model Performance",
            "Dataset Insights",
            "About CitizenSense"
        ],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("**PROJECT STATUS**")
    st.markdown("🟢 Models loaded" if models["category_model"] is not None
                else "🌐 Model files not found")
    st.caption("AIRI Team | PITB AI Internship")


# =========================================================
# PAGE HEADER
# =========================================================

def page_header(title, subtitle):
    st.markdown(f"<div class='main-title'>{title}</div>",
                unsafe_allow_html=True)
    st.markdown(f"<div class='subtitle'>{subtitle}</div>",
                unsafe_allow_html=True)


def metric_card(label, value, note=""):
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{html.escape(str(label))}</div>
        <div class="metric-value">{html.escape(str(value))}</div>
        <div class="metric-note">{html.escape(str(note))}</div>
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# SYSTEM OVERVIEW
# =========================================================

if selected_page == "System Overview":

    page_header(
        "System Overview",
        "A unified view of public feedback, complaint patterns and model performance."
    )

    if df.empty:
        st.error("Dataset not found. Please check data/labels.csv.")
        st.stop()

    total = len(df)
    categories = df["category"].nunique() if "category" in df else 0
    reviewed = (
        df["manual_reviewed"].astype(str).str.lower()
        .isin(["true", "1", "yes", "reviewed"]).sum()
        if "manual_reviewed" in df else 0
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        metric_card("Total Samples", f"{total:,}", "Dataset records")
    with c2:
        metric_card("Categories", categories, "Complaint categories")
    with c3:
        metric_card("Reviewed Samples", f"{reviewed:,}", "Manually reviewed")
    with c4:
        metric_card("Category Accuracy", "98.67%", "Baseline test accuracy")

    st.markdown("<div class='section-title'>Complaint Distribution</div>",
                unsafe_allow_html=True)

    if "category" in df:
        show_category_chart(df)

    st.markdown("<div class='section-title'>Public Feedback Overview</div>",
                unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        if "sentiment" in df:
            show_donut_chart(
                df, "sentiment", "Sentiment Distribution",
                {
                    "Positive": "#D6B56D",
                    "Negative": "#4F8580",
                    "Neutral": "#E5D8BD"
                }
            )

    with col2:
        if "priority" in df:
            show_donut_chart(
                df, "priority", "Priority Distribution",
                {
                    "High": "#4F8580",
                    "Medium": "#0F5B5A",
                    "Low": "#D6B56D"
                }
            )

    st.info(
        "Dataset note: This project uses synthetic civic-feedback samples. "
        "Model results should be validated on real-world citizen feedback "
        "before operational use."
    )


# =========================================================
# COMPLAINT INTELLIGENCE
# =========================================================

elif selected_page == "Complaint Intelligence":

    page_header(
        "Complaint Intelligence",
        "Enter public feedback to generate an AI-assisted classification."
    )

    st.markdown("<div class='info-card'>"
                "<div class='small-heading'>How it works</div>"
                "Enter a complaint and select Analyze Complaint. "
                "CitizenSense processes the text and predicts its category, "
                "sentiment and priority."
                "</div>", unsafe_allow_html=True)

    complaint = st.text_area(
        "Citizen feedback",
        placeholder="Example: There is no clean drinking water in our area...",
        height=150
    )

    if st.button("Analyze Complaint", use_container_width=True):

        if not complaint.strip():
            st.warning("Please enter a complaint first.")

        elif models["category_model"] is None:
            st.error("Category model not found. Please check the models folder.")

        else:
            result = predict_complaint(complaint)

            st.markdown("<div class='section-title'>Analysis Results</div>",
                        unsafe_allow_html=True)

            a, b, c = st.columns(3)

            with a:
                metric_card("Complaint Category", result["category"])
            with b:
                metric_card("Sentiment", result["sentiment"])
            with c:
                metric_card("Priority", result["priority"])

            if result["confidence"] is not None:
                st.markdown("**Category prediction confidence**")
                st.progress(result["confidence"])
                st.caption(f"{result['confidence']:.1%}")

            left, right = st.columns(2)

            with left:
                st.markdown("**Important Keywords**")
                if result["keywords"]:
                    st.write(" | ".join(result["keywords"]))
                else:
                    st.write("No keywords found.")

            with right:
                st.markdown("**Short Summary**")
                st.write(result["summary"])

            st.markdown("**Suggested Department / Action Area**")

            department_map = {
                "Roads / Infrastructure": "Municipal Services / Infrastructure",
                "Electricity": "Electricity Department",
                "Water Supply": "Water and Sanitation Agency",
                "Sanitation": "Waste Management / Sanitation",
                "Health": "Health Department",
                "Education": "Education Department",
                "Traffic": "Traffic Police / Transport Department",
                "General": "Relevant Public Service Department"
            }

            st.success(
                department_map.get(result["category"],
                                   "Relevant Public Service Department")
            )

            st.caption(
                "Department suggestions are rule-based guidance, not an "
                "official government routing decision."
            )


# =========================================================
# MODEL PERFORMANCE
# =========================================================

elif selected_page == "Model Performance":

    page_header(
        "Model Performance",
        "Evaluation results from the held-out test dataset."
    )

    st.markdown("<div class='section-title'>Baseline and Transformer Results</div>",
                unsafe_allow_html=True)

    show_performance_chart()

    st.markdown("<div class='section-title'>Evaluation Summary</div>",
                unsafe_allow_html=True)

    performance = pd.DataFrame({
        "Model": [
            "TF-IDF + Logistic Regression (Category)",
            "TF-IDF + Logistic Regression (Sentiment)",
            "TF-IDF + Logistic Regression (Priority)",
            "RoBERTa (Sentiment)"
        ],
        "Test Accuracy": ["98.67%", "100%", "100%", "52%"],
        "Weighted F1": ["98.67%", "100%", "100%", "0.48"],
        "Task": ["Category", "Sentiment", "Priority", "Sentiment"]
    })

    st.dataframe(performance, use_container_width=True, hide_index=True)

    st.markdown("<div class='section-title'>Interpretation</div>",
                unsafe_allow_html=True)

    st.markdown("""
    <div class="info-card">
        <b>Baseline ML:</b> TF-IDF with Logistic Regression achieved strong
        results on the synthetic civic-feedback dataset.
        <br><br>
        <b>Transformer:</b> The pre-trained RoBERTa sentiment pipeline achieved
        52% accuracy on the same sentiment test samples.
        <br><br>
        <b>Observation:</b> A pre-trained transformer is not automatically
        better for every domain. Domain differences and training data matter.
    </div>
    """, unsafe_allow_html=True)

    st.warning(
        "These scores may be inflated because the dataset is synthetic and "
        "template-based. Real-world evaluation is still required."
    )


# =========================================================
# DATASET INSIGHTS
# =========================================================

elif selected_page == "Dataset Insights":

    page_header(
        "Dataset Insights",
        "Explore sample composition, labels and dataset splits."
    )

    if df.empty:
        st.error("Dataset not found.")
        st.stop()

    c1, c2, c3 = st.columns(3)

    with c1:
        metric_card("Total Records", len(df))
    with c2:
        metric_card("Unique Categories", df["category"].nunique())
    with c3:
        metric_card("Unique Sample IDs",
                    df["sample_id"].nunique() if "sample_id" in df else "N/A")

    if "split" in df:
        st.markdown("<div class='section-title'>Train / Validation / Test Split</div>",
                    unsafe_allow_html=True)

        split_counts = df["split"].value_counts()
        fig, ax = plt.subplots(figsize=(8, 3.5))
        bars = ax.bar(
            split_counts.index.astype(str),
            split_counts.values,
            color=[ORANGE, GOLD, "#4F8580"][:len(split_counts)],
            width=0.55
        )
        chart_theme(ax)
        ax.set_title("Dataset Split Distribution", loc="left",
                     fontsize=14, fontweight="bold", color=CHARCOAL)
        ax.set_ylabel("Samples")

        for bar in bars:
            ax.text(bar.get_x() + bar.get_width()/2,
                    bar.get_height() + 2,
                    str(int(bar.get_height())),
                    ha="center", fontsize=10, color=CHARCOAL)

        fig.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    st.markdown("<div class='section-title'>Dataset Preview</div>",
                unsafe_allow_html=True)

    preview_columns = [
        col for col in [
            "sample_id", "text", "category", "sentiment",
            "priority", "source_type", "manual_reviewed", "split"
        ] if col in df.columns
    ]

    st.dataframe(
        df[preview_columns].head(20),
        use_container_width=True,
        hide_index=True
    )

    st.download_button(
        "Download Dataset CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="citizensense_dataset.csv",
        mime="text/csv"
    )


# =========================================================
# ABOUT
# =========================================================

elif selected_page == "About CitizenSense":

    page_header(
        "About CitizenSense",
        "NLP-based public feedback classification and insight system."
    )

    st.markdown("""
    <div class="info-card">
        <div class="small-heading">Project Objective</div>
        CitizenSense aims to analyze public feedback using Natural Language
        Processing and Machine Learning. It helps organize complaints and
        identify useful information from text.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='section-title'>Core Features</div>",
                unsafe_allow_html=True)

    features = [
        ("01", "Complaint Classification",
         "Classifies feedback into civic-service categories."),
        ("02", "Sentiment Analysis",
         "Identifies Positive, Negative and Neutral feedback."),
        ("03", "Priority Detection",
         "Predicts Low, Medium and High priority."),
        ("04", "Keyword Extraction",
         "Highlights important words in submitted feedback."),
        ("05", "Short Summary",
         "Provides a concise extract from the submitted complaint."),
        ("06", "Department Suggestion",
         "Suggests a relevant department or action area.")
    ]

    for number, title, description in features:
        st.markdown(f"""
        <div class="info-card">
            <span style="color:#0F5B5A;font-weight:800;">{number}</span>
            &nbsp;&nbsp;<b>{title}</b>
            <br><span style="color:#71817D;">{description}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div class='section-title'>Technology Stack</div>",
                unsafe_allow_html=True)

    st.write(
        "Python Â· Pandas Â· Scikit-learn Â· TF-IDF Â· Logistic Regression Â· "
        "Hugging Face Transformers Â· Streamlit Â· Matplotlib"
    )

    st.markdown("<div class='section-title'>Important Limitations</div>",
                unsafe_allow_html=True)

    st.warning("""
    - The current dataset contains synthetic, template-based samples.
    - Manual review was performed on 200 samples; this does not mean the
      dataset was independently labeled from scratch.
    - The transformer is a pre-trained sentiment pipeline, not a fine-tuned
      civic-feedback model.
    - Department suggestions are indicative and require human review.
    - Real public feedback and further validation are needed before deployment.
    """)

    st.caption("CitizenSense | AIRI Team PITB AI Internship | Task 4")

