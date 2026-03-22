# GymAura Nutrition PoC

## Goal
Validate whether natural language meal descriptions can be converted into structured food data using the internal USDA-based dataset.

## Scope
This PoC focuses on the internal text pipeline only:

1. text input
2. food extraction
3. dataset matching
4. nutrition calculation

Speech-to-text and AI comparison are intentionally left for later phases.

## KPIs
Supervisor targets for the PoC:

- Food detection accuracy >= 80%
- Dataset matching success >= 85%
- Quantity detection accuracy (simple cases) >= 60%
- End-to-end success >= 70%

## Project Structure

```bash
GYMAURA-NUTRITION-POC/
│
├── data/
│   └── food_item_rows.csv
│
├── src/
│   ├── __init__.py
│   ├── data_prep.py
│   ├── extractor.py
│   ├── matcher.py
│   ├── nutrition.py
│   ├── pipeline.py
│   └── evaluation.py
│
├── tests/
│   ├── __init__.py
│   └── test_cases.py
│
├── main.py
├── README.md
└── requirements.txt