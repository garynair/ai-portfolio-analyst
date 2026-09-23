# Agent 05 — Save, Archive, Dashboard

## Activation

"Activate Agent 05"

## Inputs

- The fully updated working workbook (after Agent 04)
- Previous `02_output/portfolio_state_*.xlsx` (for the "changed since last
  run" comparison and for archiving)

## Steps

1. Write the updated workbook to
   `02_output/portfolio_state_<YYYYMMDD>.xlsx`.
2. Move the superseded previous copy to `03_archive/` with a timestamp
   suffix (per Rule 3 — never delete).
3. Recalculate the workbook and confirm there are **zero formula errors**
   (check columns J and K and any other formulas) before reporting success.
4. Build a self-contained HTML dashboard at
   `04_dashboard/dashboard_<YYYYMMDD>.html` showing:
   - Decision counts (how many Buy / Hold / Sell)
   - One card per stock (ticker, price, change, decision, confidence,
     rationale)
   - Every decision that changed since the last run (previous decision vs.
     new decision)

## Outputs

- `02_output/portfolio_state_<YYYYMMDD>.xlsx`
- `03_archive/portfolio_state_<previous-YYYYMMDD>_<timestamp>.xlsx`
  (moved, not deleted)
- `04_dashboard/dashboard_<YYYYMMDD>.html`

## Guardrails

- Rule 0: everything stays inside the selected folder.
- Never call the Alpha Vantage API.
- Never delete the superseded workbook — move it to `03_archive/` with a
  timestamp suffix and tell the user what was moved.
- Do not report success if any formula errors remain — fix or flag them
  first.
- The dashboard must be self-contained (no external network calls/assets)
  and must never contain the API key.

## Done when

The new dated workbook exists in `02_output/`, the old one has been moved
(not deleted) to `03_archive/` with a timestamp suffix, zero formula errors
have been confirmed, and the dashboard HTML file exists in `04_dashboard/`
showing decision counts, per-stock cards, and this run's changed decisions.
