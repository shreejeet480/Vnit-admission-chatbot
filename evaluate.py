"""
Evaluate the ML intent classifier.

Runs stratified 5-fold cross-validation on the training data and
prints accuracy, macro-F1, and a per-intent classification report.

Usage:
    python evaluate.py
"""

import json
import numpy as np
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.metrics import accuracy_score, f1_score, classification_report

from src.ml_intent_classifier import MLIntentClassifier, TRAINING_DATA_PATH


def main():
    with open(TRAINING_DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    texts, labels = [], []
    for intent, examples in data.items():
        texts.extend(e.lower().strip() for e in examples)
        labels.extend([intent] * len(examples))

    texts = np.array(texts)
    labels = np.array(labels)

    clf = MLIntentClassifier()
    pipeline = clf._build_pipeline()

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    predictions = cross_val_predict(pipeline, texts, labels, cv=cv)

    acc = accuracy_score(labels, predictions)
    macro_f1 = f1_score(labels, predictions, average="macro")

    print(f"Dataset size      : {len(texts)} examples, {len(set(labels))} intents")
    print(f"5-fold CV accuracy: {acc:.3f}")
    print(f"5-fold macro F1   : {macro_f1:.3f}")
    print()
    print(classification_report(labels, predictions))


if __name__ == "__main__":
    main()
