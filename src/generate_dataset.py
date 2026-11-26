

import csv
import itertools
import random
from pathlib import Path

# Reproducible dataset generation
random.seed(42)

OUTPUT_FILE = Path("data/labels.csv")
TARGET_SAMPLES = 500

# Category-specific feedback topics
CATEGORY_ISSUES = {
    "Roads / Infrastructure": [
        "potholes on the main road",
        "damaged road surfaces",
        "broken streetlights",
        "a damaged public footpath",
        "poor road maintenance",
    ],
    "Electricity": [
        "frequent power outages",
        "unstable electricity supply",
        "low voltage in residential areas",
        "electricity service interruptions",
        "damaged public power infrastructure",
    ],
    "Water Supply": [
        "irregular water supply",
        "water leakage in public pipelines",
        "shortage of clean drinking water",
        "poor water distribution",
        "water quality concerns",
    ],
    "Sanitation": [
        "uncollected garbage",
        "blocked drainage systems",
        "overflowing public waste bins",
        "unclean public streets",
        "poor waste management",
    ],
    "Health": [
        "long waiting times at public hospitals",
        "shortage of basic medical facilities",
        "poor cleanliness in public clinics",
        "delays in healthcare services",
        "limited availability of medical staff",
    ],
    "Education": [
        "shortage of classroom facilities",
        "poor maintenance of public schools",
        "lack of educational resources",
        "damaged school buildings",
        "limited classroom equipment",
    ],
    "Traffic": [
        "poorly managed traffic signals",
        "traffic congestion at busy roads",
        "unsafe pedestrian crossings",
        "lack of traffic management",
        "poor public transport coordination",
    ],
    "General": [
        "delays in public service responses",
        "difficulty accessing government services",
        "lack of information about public services",
        "delayed resolution of public requests",
        "general public service concerns",
    ],
}

SENTIMENT_PHRASES = {
    "Positive": [
        "The recent improvements have been helpful.",
        "Thank you for addressing this matter.",
        "The service has shown positive progress.",
        "I appreciate the efforts made so far.",
        "The recent response has been satisfactory.",
    ],
    "Negative": [
        "This ongoing problem is causing frustration.",
        "The situation is disappointing for residents.",
        "The issue has not been resolved properly.",
        "Residents are dissatisfied with the current situation.",
        "This problem is affecting everyday activities.",
    ],
    "Neutral": [
        "I would like to report this situation.",
        "Please record this issue for review.",
        "This matter is being brought to your attention.",
        "The current situation requires an assessment.",
        "Please review the reported condition.",
    ],
}

PRIORITY_PHRASES = {
    "High": [
        "It requires urgent attention due to its serious impact.",
        "Immediate assessment is needed because public safety may be affected.",
        "Please escalate this matter for urgent action.",
    ],
    "Medium": [
        "Please arrange an inspection in a reasonable time.",
        "This issue needs attention to prevent further inconvenience.",
        "A timely response would help resolve the matter.",
    ],
    "Low": [
        "Please consider this during routine service improvements.",
        "This suggestion can be reviewed during regular maintenance.",
        "It would be helpful to include this in future planning.",
    ],
}

def generate_samples():
    samples = []
    sample_id = 1

    # Generate a balanced number of samples per category
    categories = list(CATEGORY_ISSUES.keys())
    category_counts = {
        category: TARGET_SAMPLES // len(categories)
        for category in categories
    }

    remainder = TARGET_SAMPLES % len(categories)

    for category in categories[:remainder]:
        category_counts[category] += 1

    for category, count in category_counts.items():
        combinations = []

        for issue in CATEGORY_ISSUES[category]:
            for sentiment, sentiment_phrases in SENTIMENT_PHRASES.items():
                for priority, priority_phrases in PRIORITY_PHRASES.items():
                    for sentiment_text in sentiment_phrases:
                        for priority_text in priority_phrases:
                            combinations.append((
                                issue,
                                sentiment,
                                priority,
                                sentiment_text,
                                priority_text,
                            ))

        random.shuffle(combinations)

        for issue, sentiment, priority, sentiment_text, priority_text in combinations[:count]:

            feedback = (
                f"I would like to report {issue}. "
                f"{sentiment_text} "
                f"{priority_text}"
            )

            samples.append({
                "sample_id": f"CS-{sample_id:04d}",
                "text": feedback,
                "category": category,
                "sentiment": sentiment,
                "priority": priority,
                "source_type": "Synthetic",
                "manual_reviewed": "false",
                "split": "pending",
            })

            sample_id += 1

    random.shuffle(samples)
    return samples


def save_dataset(samples):
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "sample_id",
        "text",
        "category",
        "sentiment",
        "priority",
        "source_type",
        "manual_reviewed",
        "split",
    ]

    with OUTPUT_FILE.open(
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(samples)


def main():
    samples = generate_samples()
    save_dataset(samples)

    print("\nCitizenSense dataset generated successfully!")
    print(f"Total samples: {len(samples)}")
    print(f"Output file: {OUTPUT_FILE}")

    print("\nCategory distribution:")
    for category in CATEGORY_ISSUES:
        count = sum(
            sample["category"] == category
            for sample in samples
        )
        print(f"{category}: {count}")

    print("\nAll samples are marked Synthetic.")
    print("Manual review status: false")
    print("Dataset split: pending")


if __name__ == "__main__":
    main()
