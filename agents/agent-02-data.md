# Agent 02 — Fetch Market Data

## Activation

"Activate Agent 02"

## Inputs

- `01_input/api_key.txt`
- `02_output/raw_cache_<YYYYMMDD>.json` (today's date, if it already exists)

## Steps

1. Read the API key from `01_input/api_key.txt`. Never print it in full.
2. Check whether `02_output/raw_cache_<YYYYMMDD>.json` already exists for
   **today's** date. If it does, reuse it and make **zero** API calls.
3. If it does not exist, call Alpha Vantage **twice per ticker** for all 10
   stocks (NVDA, AAPL, GOOGL, MSFT, AMZN, TSM, SPCX, AVGO, META, TSLA):
   - `TIME_SERIES_DAILY` with `outputsize=compact` (price history, for
     Agent 03's technical indicators)
   - `OVERVIEW` (company fundamentals — margins, growth, valuation ratios,
     for Agent 03's fundamental view)
   = **20 calls total** per run (still under the 25/day cap, leaving 5 of
   headroom).
4. If the API returns a rate-limit message or an invalid-key message for a
   given call, record it and move on to the next ticker/endpoint — do not
   retry silently and do not fall back to guessed data. Stop the whole run
   early only if it becomes clear the daily budget is exhausted (repeated
   rate-limit responses).
5. Save all raw responses (both endpoints, per ticker) into a single file:
   `02_output/raw_cache_<YYYYMMDD>.json`, structured so Agent 03 can find
   each ticker's `TIME_SERIES_DAILY` result and `OVERVIEW` result
   separately (e.g. `{"results": {"<TICKER>": {"time_series": {...},
   "overview": {...}}}, "errors": {...}}`).
6. From the fetched `TIME_SERIES_DAILY` data, write column **H** (Current
   Date) and column **I** (Current Price ($)) into the working workbook for
   each ticker.
7. Report calls used this run (out of 20 planned) and remaining budget out
   of 25/day.

## Outputs

- `02_output/raw_cache_<YYYYMMDD>.json` (price history + company overview
  per ticker)
- Updated columns H and I in the working workbook

## Guardrails

- Rule 0: everything stays inside the selected folder.
- This is the **only** agent allowed to call the Alpha Vantage API.
- Exactly two calls per ticker — `TIME_SERIES_DAILY`/`compact` and
  `OVERVIEW` — never more.
- If today's cache already exists, make **zero** calls — reuse it.
- Never write the API key anywhere except reading it from
  `01_input/api_key.txt`. Never print it in full, never log it, never put it
  in a filename.
- Never overwrite columns J or K (formulas).
- On a rate-limit or invalid-key response for any call, record it plainly
  and move on — do not fabricate price or fundamental data.
- Never delete anything.

## Done when

`02_output/raw_cache_<YYYYMMDD>.json` exists for today with both endpoints
per ticker (or a recorded error for whichever failed), columns H and I are
populated for every ticker with price data, and the user has seen a report
of calls used vs. the 25/day budget (or confirmation that zero calls were
made because today's cache already existed).
