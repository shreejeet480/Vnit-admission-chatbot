# VNIT Admission Assistant 🍊

A hybrid **ML + rule-based chatbot** that answers admission queries for VNIT Nagpur — programs, eligibility, JEE/GATE cutoffs, fees, documents, counselling, and placements — with **built-in explainability**: every answer shows the predicted intent, model confidence, and which engine (ML or rules) produced it.

![Python](https://img.shields.io/badge/Python-3.10+-blue) ![scikit--learn](https://img.shields.io/badge/scikit--learn-TF--IDF%20%2B%20LogReg-orange) ![Flask](https://img.shields.io/badge/Flask-Web%20UI-lightgrey)

## Why this project is interesting

Most college-FAQ bots are pure keyword matchers. This one treats intent detection as a **supervised text-classification problem** and uses rules only as a safety net:

1. **Vectorize** — TF-IDF over word (1–2) *and* character (3–5) n-grams, making the model tolerant to typos ("fee structre") and code-mixed Hinglish ("counselling kab hai").
2. **Classify** — Logistic Regression over 9 intents, returning calibrated probabilities used as confidence scores.
3. **Fall back** — predictions below a confidence threshold (0.40) route to a regex/keyword recognizer, so the bot never answers blindly.

## Results

| Metric | Value |
|---|---|
| Intents | 9 |
| Labeled training examples | 257 |
| 5-fold CV accuracy | **0.82** |
| 5-fold macro F1 | **0.82** |

Expanding the dataset from 145 → 257 examples raised macro-F1 from **0.68 → 0.82** — a concrete demonstration that data quality/quantity beats model complexity at this scale.

Reproduce with:
```bash
python evaluate.py
```

## Architecture

```
User message
     │
     ▼
┌────────────────────┐   confident?   ┌──────────────────────┐
│  MLIntentClassifier │──── yes ────▶ │                      │
│  TF-IDF + LogReg    │               │  ResponseGenerator   │──▶ Answer + intent
└────────┬───────────┘               │  (per-intent handlers)│    + confidence
         │ no (low confidence)        │                      │    + source badge
         ▼                            └──────────────────────┘
┌────────────────────┐                          ▲
│  IntentRecognizer   │──────────────────────────┘
│  regex + keywords   │   (also extracts program/specialization entities)
└────────────────────┘

SQLite logs every conversation (users, queries, intents) for the admin analytics CLI.
```

## Run it

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start the web app (trains & caches the model on first run)
python interfaces/web_app.py

# 3. Open http://127.0.0.1:5000
```

Other interfaces:
```bash
python main.py                  # CLI chat
python interfaces/admin.py      # admin analytics (query stats, popular intents)
python evaluate.py              # ML evaluation report
```

## Project structure

```
├── data/
│   └── training_data.json      # 257 labeled examples across 9 intents
├── src/
│   ├── ml_intent_classifier.py # TF-IDF + LogisticRegression (scikit-learn)
│   ├── intent_recognition.py   # rule-based fallback + entity extraction
│   ├── response_generator.py   # per-intent answer templates
│   ├── chatbot.py              # hybrid orchestration
│   └── database.py             # SQLite logging
├── interfaces/
│   ├── web_app.py              # Flask REST API + web UI
│   ├── cli.py                  # terminal interface
│   └── admin.py                # analytics dashboard
├── templates/ & static/        # explainable chat UI
└── evaluate.py                 # 5-fold cross-validation report
```

## Roadmap

- [ ] Replace TF-IDF with sentence-transformer embeddings for semantic matching
- [ ] Active learning: log low-confidence queries and add them to training data
- [ ] RAG over official VNIT documents for always-current answers
- [ ] Deploy on Render/Railway with CI

## Author

**Shreejeet** — M.Tech CSE, VNIT Nagpur
