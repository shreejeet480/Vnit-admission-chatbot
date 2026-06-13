"""
ML Intent Classifier
--------------------
Machine-learning based intent classification using TF-IDF features
and Logistic Regression (scikit-learn).

Why this design:
- TF-IDF with word + character n-grams handles typos and short queries well
- Logistic Regression gives calibrated probabilities -> usable confidence scores
- Model is trained once and cached to disk (joblib) for fast startup

Used in a HYBRID setup: the chatbot tries this ML classifier first;
if confidence is below threshold, it falls back to the rule-based
IntentRecognizer (regex + keywords).
"""

import json
import os
import logging
from typing import Dict, List, Tuple

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.pipeline import FeatureUnion
import joblib

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRAINING_DATA_PATH = os.path.join(BASE_DIR, "data", "training_data.json")
MODEL_PATH = os.path.join(BASE_DIR, "data", "intent_model.joblib")


class MLIntentClassifier:
    """TF-IDF + Logistic Regression intent classifier with confidence scores."""

    def __init__(self,
                 training_data_path: str = TRAINING_DATA_PATH,
                 model_path: str = MODEL_PATH,
                 confidence_threshold: float = 0.40):
        self.training_data_path = training_data_path
        self.model_path = model_path
        self.confidence_threshold = confidence_threshold
        self.pipeline = None
        self._load_or_train()

    # ------------------------------------------------------------------ #
    # Training
    # ------------------------------------------------------------------ #
    def _load_training_data(self) -> Tuple[List[str], List[str]]:
        """Load labeled examples from JSON -> (texts, labels)."""
        with open(self.training_data_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        texts, labels = [], []
        for intent, examples in data.items():
            for example in examples:
                texts.append(example.lower().strip())
                labels.append(intent)
        return texts, labels

    def _build_pipeline(self) -> Pipeline:
        """TF-IDF (word 1-2 grams + char 3-5 grams) -> Logistic Regression."""
        features = FeatureUnion([
            ("word", TfidfVectorizer(analyzer="word",
                                     ngram_range=(1, 2),
                                     sublinear_tf=True)),
            ("char", TfidfVectorizer(analyzer="char_wb",
                                     ngram_range=(3, 5),
                                     sublinear_tf=True)),
        ])
        return Pipeline([
            ("features", features),
            ("clf", LogisticRegression(max_iter=1000, C=5.0)),
        ])

    def train(self) -> None:
        """Train the classifier and cache it to disk."""
        texts, labels = self._load_training_data()
        self.pipeline = self._build_pipeline()
        self.pipeline.fit(texts, labels)
        joblib.dump(self.pipeline, self.model_path)
        logger.info("ML intent model trained on %d examples, saved to %s",
                    len(texts), self.model_path)

    def _load_or_train(self) -> None:
        """Load cached model if present; otherwise train from scratch."""
        if os.path.exists(self.model_path):
            try:
                self.pipeline = joblib.load(self.model_path)
                logger.info("Loaded cached ML intent model from %s", self.model_path)
                return
            except Exception as exc:  # corrupted cache -> retrain
                logger.warning("Failed to load cached model (%s); retraining", exc)
        self.train()

    # ------------------------------------------------------------------ #
    # Inference
    # ------------------------------------------------------------------ #
    def predict(self, message: str) -> Dict:
        """
        Classify a message.

        Returns:
            {
              'intent': str,            # top predicted intent
              'confidence': float,      # probability of top intent (0-1)
              'is_confident': bool,     # confidence >= threshold
              'all_scores': dict        # intent -> probability
            }
        """
        message = (message or "").lower().strip()
        if not message:
            return {"intent": "general", "confidence": 0.0,
                    "is_confident": False, "all_scores": {}}

        probabilities = self.pipeline.predict_proba([message])[0]
        classes = self.pipeline.named_steps["clf"].classes_
        all_scores = {c: round(float(p), 4) for c, p in zip(classes, probabilities)}

        top_intent = max(all_scores, key=all_scores.get)
        confidence = all_scores[top_intent]

        return {
            "intent": top_intent,
            "confidence": confidence,
            "is_confident": confidence >= self.confidence_threshold,
            "all_scores": all_scores,
        }
