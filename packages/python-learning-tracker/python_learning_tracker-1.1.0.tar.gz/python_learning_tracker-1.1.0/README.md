# 🐍 Python Learning Tracker

**Flask web app and CLI for analyzing Python learning progress**  
_Author: Andriy Povh_

---

## 🇬🇧 Overview

**Python Learning Tracker** helps you analyze your Python study progress from structured CSV data.

### ✅ Features

- Flask web interface:
  - `/report` – overall learning summary
  - `/report/topics/` – all studied topics
  - `/report/topics/<abbr>` – detailed view per topic
  - `/search?q=...` – search topics
- Command Line Interface (CLI)
- Motivation phrases support
- Data-driven analysis from `abbreviations.csv`, `planned.csv`, `actual.csv`

---

## 🚀 Quick Start (with `uv`)

```bash
uv venv
uv pip install -e .[dev]
uv pip install flask
python app.py
```

---

## 🧪 Run Tests

```bash
pytest
```

Or with coverage:

```bash
pytest --cov=src --cov=app --cov-report=term
```

---

## 🧼 Lint & Format

```bash
ruff check .
ruff format .
```

---

## 💻 CLI Example

```bash
python -m python_learning_tracker.cli --files data --motivate
```