# Agent 04 — Decide & Update State

## Activation

"Activate Agent 04"

## Inputs

- Working workbook with columns L, M, N, O populated by Agent 03
- Columns D, E, F, G (previous state) already in the workbook

## Steps

1. Combine the technical view (L) and fundamental view (N) into a single
   decision: **Buy / Hold / Sell**, plus a **confidence score (1-5)** and a
   written **rationale**. Write these to columns **P** (Final Decision),
   **Q** (Confidence 1-5), and **R** (Rationale).
2. Publish the exact combination rule used (e.g. how technical + fundamental
   signals map to Buy/Hold/Sell and how confidence is scored) as a table so
   the user can audit the logic.
3. Carry this run's results backward into the "previous" columns for next
   time:
   - H (Current Date) → D (Last Review Date)
   - I (Current Price) → E (Reference Price)
   - P (Final Decision) → F (Previous Decision)
   - R (Rationale) → G (Previous Notes)
4. Write column **S** (Updated Status) and column **T** (Decision
   Timestamp) for each ticker.

## Outputs

- Updated columns P, Q, R, S, T in the working workbook
- Updated columns D, E, F, G (carried forward from H, I, P, R)
- The published combination-rule table shown to the user

## Guardrails

- Rule 0: everything stays inside the selected folder.
- Never call the Alpha Vantage API.
- Never overwrite columns J or K (formulas).
- The combination rule must be shown to the user, not left implicit —
  every decision must be auditable.
- Never delete anything — carrying values from H/I/P/R into D/E/F/G is a
  copy-forward, not a deletion of the originals.

## Done when

Columns P, Q, R, S, T are populated for all 10 tickers, D/E/F/G have been
carried forward from this run's H/I/P/R, and the user has seen the
combination-rule table used to reach each decision.
