# CLAUDE.md — AI Portfolio Analyst

## Purpose

This folder runs a five-agent stock analysis workflow. Agents fetch market
data, compute technical and fundamental indicators, combine them into a
Buy/Hold/Sell decision, and log the result to a tracked spreadsheet and an
HTML dashboard. The workflow is designed to run on a small, fixed API budget
and to never lose or silently overwrite prior state.

**This is a classroom / educational exercise. Nothing produced by this
system is investment advice.** Decisions, confidence scores, and rationale
text are illustrative outputs of a learning project, not a recommendation to
buy, hold, or sell any security. Always consult a licensed financial advisor
before making investment decisions.

---

## RULE 0 — STAY INSIDE THE SELECTED FOLDER

Everything created goes inside the folder the user selected in Cowork.
Nothing goes anywhere else. Not the Desktop, not Documents, not the home
directory, not a temp directory, not a scratch folder of the agent's own
choosing.

Every path written is relative to that selected folder. Before writing any
file, confirm the path sits inside it. If a task seems to need a file
outside it, stop and ask the user instead of doing it.

**This rule outranks every other instruction in this document.**

---

## THE THREE RULES

1. Anything the user gives us is stored in `01_input/`.
2. Everything we generate is written to `02_output/`.
3. **NEVER DELETE.** If the user says delete, remove, clear or drop a file,
   MOVE it to `03_archive/` with a timestamp suffix and tell them what was
   moved. No exceptions.

---

## FOLDER LAYOUT

```
01_input/       Everything the user provides goes here.
02_output/      Everything the system generates goes here.
03_archive/     Superseded files go here (never deleted).
04_dashboard/   The HTML dashboard goes here.
agents/         The five agent instruction files.
```

No other top-level folders are created (no `src/`, `data/`, `temp/`,
`scripts/`, etc.). Scratch space, if ever needed, is `02_output/`.

---

## API KEY HANDLING

- The key lives at `01_input/api_key.txt` and that file contains the key and
  nothing else.
- **Agent 01** creates this file by asking the user for the key.
- **Agent 02** is the only agent that reads it and the only agent allowed to
  call the Alpha Vantage API.
- The key is **never** printed in full, and never written into a workbook, a
  dashboard, a log, a filename, or any file in `02_output/`.
- When the key needs to be confirmed, only the **last four characters** are
  shown.

---

## STOCK LIST

NVDA, AAPL, GOOGL, MSFT, AMZN, TSM, SPCX, AVGO, META, TSLA

(10 tickers.)

---

## API BUDGET — HARD LIMIT

- Alpha Vantage free tier = **25 calls/day**.
- **Agent 02** is the only agent allowed to call the API.
- It makes **two calls per ticker** — `TIME_SERIES_DAILY` (`compact`) for
  price history, plus `OVERVIEW` for fundamentals — = **20 calls total**
  per run (5 of daily headroom left over).
- Raw responses (both endpoints, per ticker) are saved to
  `02_output/raw_cache_<YYYYMMDD>.json`.
- **Agent 03** computes every technical indicator and reads every
  fundamental figure from that cache in Python and never calls the API.
- If today's cache already exists, Agent 02 reuses it and makes **zero**
  calls.
- *(Updated from the original 1-call-per-ticker / 10-call design on
  2026-09-07 to add real fundamental data instead of leaving columns N/O as
  "insufficient data.")*

---

## THE WORKING FILE

`01_input/portfolio_state_starter_template.xlsx` — sheet **"Portfolio
State"**. Header in row 4, data from row 5.

| Col | Field                  | Col | Field                 | Col | Field                |
|-----|------------------------|-----|-----------------------|-----|-----------------------|
| A   | Ticker                 | H   | Current Date          | O   | Fundamental Detail    |
| B   | Company                | I   | Current Price ($)     | P   | Final Decision        |
| C   | Position Status        | J   | Change ($)            | Q   | Confidence (1-5)      |
| D   | Last Review Date       | K   | Change (%)            | R   | Rationale             |
| E   | Reference Price ($)    | L   | Technical View        | S   | Updated Status        |
| F   | Previous Decision      | M   | Technical Detail      | T   | Decision Timestamp    |
| G   | Previous Notes         | N   | Fundamental View      |     |                       |

Notes:
- Columns **C, F, G** are filled in by the user.
- Columns **D, E** come pre-filled.
- Columns **J, K** are formulas — read them, **never** overwrite with
  values.
- Row 5 is a greyed **EXAMPLE** row the user deletes before the first run.

---

## AGENT TABLE

| # | File                        | Activation Phrase   | Role                                             |
|---|-----------------------------|----------------------|---------------------------------------------------|
| 01 | agents/agent-01-state.md    | Activate Agent 01   | Setup check and read previous state               |
| 02 | agents/agent-02-data.md     | Activate Agent 02   | Fetch market data (only agent allowed to call the API) |
| 03 | agents/agent-03-analysis.md | Activate Agent 03   | Technical + fundamental analysis (Python, cache only) |
| 04 | agents/agent-04-decision.md | Activate Agent 04   | Decide (Buy/Hold/Sell) and update state           |
| 05 | agents/agent-05-save.md     | Activate Agent 05   | Save, archive, build dashboard                    |

---

## DISCLAIMER

This is a **classroom exercise**, not a production trading or advisory
system. All decisions, confidence scores, technical/fundamental commentary,
and dashboard output are for **educational purposes only** and do **not**
constitute investment advice. Do not use this system's output as the basis
for real investment decisions.
