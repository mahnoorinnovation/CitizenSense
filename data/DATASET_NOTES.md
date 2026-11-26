# CitizenSense - Dataset Documentation

## 1. Project Overview

**Project:** CitizenSense - NLP-Based Public Feedback Classification and Insight System

**Purpose:** Analyze public feedback to identify complaint category, sentiment, priority level, important keywords, short summary, and suggested department/action area.

## 2. Dataset Requirements

- Minimum total samples: 500
- Minimum manually labeled samples: 200
- Minimum complaint categories: 4
- Training split: 70%
- Validation split: 15%
- Testing split: 15%

## 3. Complaint Categories

1. Roads / Infrastructure
2. Electricity
3. Water Supply
4. Sanitation
5. Health
6. Education
7. Traffic
8. General

## 4. Dataset Source and Type

**Dataset type:** Original synthetic citizen-feedback dataset.

**Public source:** Not applicable to the planned synthetic samples.

**Transparency:** All generated samples will be identified as synthetic. They will not be represented as actual citizen complaints.

## 5. Data Annotation

Each feedback sample will contain:

- Feedback text
- Complaint category
- Sentiment: Positive, Negative, Neutral
- Priority: Low, Medium, High
- Source type: Synthetic

At least 200 samples must be manually reviewed and labeled. Annotation guidelines and progress will be documented.

## 6. Data Quality and Privacy

- Remove duplicate and irrelevant records.
- Avoid personal and sensitive information.
- Clearly identify synthetic examples.
- Check label consistency.
- Document dataset limitations.

## 7. Dataset Split

For 500 samples, the planned split is:

- Training: 350 samples (70%)
- Validation: 75 samples (15%)
- Testing: 75 samples (15%)

The final split will be recorded after dataset preparation.

## 8. Dataset Strategy and Status

**Decision:** Prepare an original synthetic feedback dataset containing 500 samples across eight complaint categories.

**Current status:** Dataset strategy documented. Sample generation and manual review are pending.

**Last updated:** 25 November 2026

## 9. Initial Dataset Quality Verification

**Verification status:** Passed

- Total records: 500
- Duplicate feedback texts: 0
- Missing values: 0
- Complaint categories: 8
- Manually reviewed records: 0
- Dataset split: Pending

**Note:** Automatically generated labels have not yet been manually verified. At least 200 samples still require human review.

