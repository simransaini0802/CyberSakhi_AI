# CyberSakhi AI 🛡️
### Explainable NLP-Based Scam Message Detection and Analysis System

A Flask web application that highlights possible scam indicators in messages. This starter project uses transparent, rule-based indicators and a clearly labelled heuristic risk estimate. It is **not a trained or validated scam classifier** yet.

## Features
- Pastel pista, baby pink and light pink responsive interface
- Message scanner with phrase indicators
- URL pattern warnings (does not visit URLs)
- SQLite scan history and dashboard
- Cyber safety guide
- Starter tests

## Run locally
1. Open this folder in VS Code.
2. Create a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
   On Windows use `.venv\\Scripts\\activate`.
3. Install packages:
   ```bash
   pip install -r requirements.txt
   ```
4. Start:
   ```bash
   python app.py
   ```
5. Open `http://127.0.0.1:5002`.

## Important limitations
The current scanner uses explainable phrase/URL indicators only. Its risk label is a heuristic and must not be treated as a verified probability, security verdict, or substitute for checking with the sender through a trusted channel. A legitimate message can contain a warning phrase, and a scam may avoid known phrases. Do not paste private messages containing passwords, OTPs, banking details, or personal information.

## Next development steps
- Download and document a properly licensed labelled dataset.
- Train and evaluate a TF-IDF classifier using a held-out test set.
- Report precision, recall, F1-score and confusion matrix.
- Add calibrated probabilities only if the model supports them.
- Add file upload only with safe file validation and explicit privacy controls.
