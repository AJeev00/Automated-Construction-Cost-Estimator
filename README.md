# BuildQuant — Automated Construction Cost Estimator

A Streamlit prototype for preparing a preliminary building quantity take-off and indicative cost estimate from basic rectangular building inputs.

## Features
- Editable building dimensions and construction assumptions
- Preliminary quantities for key building components
- Rate-based cost build-up and contingency
- Bill of quantities view
- CSV and Excel export

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Scope and limitations
This is an educational estimating prototype, not a tender or execution estimate. Geometry, openings, foundations, structural design, specifications, local schedule-of-rates, wastage and site conditions are simplified. Validate quantities and rates against drawings, applicable codes and current local rates before any real project use.

## Deployment
Deploy `app.py` on [Streamlit Community Cloud](https://share.streamlit.io/).
