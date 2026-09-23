# Agent 03 — Technical + Fundamental Analysis

## Activation

"Activate Agent 03"

## Inputs

- `02_output/raw_cache_<YYYYMMDD>.json` (today's cache only — both the
  `time_series` and `overview` data Agent 02 saved per ticker)

## Steps

1. Read **only** the cache file — never call the API.
2. In Python, compute for each ticker from `time_series`: 20-day and 50-day
   moving averages, RSI(14), MACD, 20-day support and resistance, volume
   trend, and 1-month momentum.
3. If there is not enough price history in the cache to compute a given
   technical indicator, write "insufficient history" for that item instead
   of guessing or estimating.
4. Write column **L** (Technical View) as a short summary label (e.g.
   Bullish/Neutral/Bearish) and column **M** (Technical Detail) with the
   numbers behind that view (the moving averages, RSI value, MACD value,
   support/resistance levels, volume trend, momentum %).
5. From each ticker's `overview` data, pull the fields needed to assess
   growth, margins, valuation, and risk — e.g. `QuarterlyRevenueGrowthYOY`,
   `ProfitMargin`, `OperatingMarginTTM`, `PERatio`, `PEGRatio`,
   `PriceToBookRatio`, `Beta`, `52WeekHigh`/`52WeekLow`. Write column **N**
   (Fundamental View) as a short summary label and column **O**
   (Fundamental Detail) with the specific figures behind that assessment.
6. If a ticker's `overview` call failed or a specific field is missing/`None`
   in the cache, write "insufficient data" for that field or ticker instead
   of guessing or filling in a number from general knowledge.
7. Show the numbers behind both views — no unsupported qualitative claims.

## Outputs

- Updated columns L, M, N, O in the working workbook

## Guardrails

- Rule 0: everything stays inside the selected folder.
- **Never** call the Alpha Vantage API or any external API — read the cache
  only.
- Never guess a number when history or fundamentals data is insufficient —
  write "insufficient history" (technical) or "insufficient data"
  (fundamental) instead.
- Never substitute general/background knowledge about a company for real
  cached figures — every number in M and O must trace back to the cache.
- Never overwrite columns H, I, J, or K.
- Never delete anything.

## Done when

Columns L, M, N, and O are populated for all 10 tickers, each with the
supporting numbers shown, and any ticker/field lacking sufficient cached
data is clearly marked "insufficient history" or "insufficient data"
rather than estimated.
