# Agent 01 — Setup Check & Read Previous State

## Activation

"Activate Agent 01"

## Inputs

- `01_input/portfolio_state_starter_template.xlsx`
- `01_input/api_key.txt` (may not exist yet)
- Newest file in `02_output/portfolio_state_*.xlsx` (if any)

## Steps

1. Check that `01_input/portfolio_state_starter_template.xlsx` exists. If it
   does not, **STOP** and tell the user to download it and put it in
   `01_input/`. Do not create a replacement template.
2. Check that `01_input/api_key.txt` exists.
   - If it does **not** exist: ask the user, "Paste your Alpha Vantage API
     key." Wait for their reply, save exactly what they paste to
     `01_input/api_key.txt`, and confirm by showing only the **last four
     characters**.
   - If it already exists: say so and move on. Do not ask again.
3. Read the newest workbook in `02_output/` (by filename date), or the
   starter template in `01_input/` if `02_output/` is empty. For each of the
   10 stocks, report: previous decision (F), reference price (E), and last
   review date (D).
4. If column C, F, or G is blank for any stock, name which stocks are
   missing which column and ask the user to fill them in. **Never guess**
   values for these columns.

## Outputs

- None (read-only agent), except possibly `01_input/api_key.txt` when
  created from the user's pasted key in Step 2.

## Guardrails

- Rule 0: everything stays inside the selected folder — never write outside
  it, never touch the Desktop, Documents, home directory, or any temp/
  scratch location of its own choosing.
- Never print the API key in full — last four characters only.
- Never create a replacement for a missing starter template.
- Never guess values for blank C, F, or G cells — ask the user instead.
- Never call the Alpha Vantage API (that is Agent 02's job only).
- Never delete anything — this agent is read-only other than saving the key.

## Done when

The user has seen: (a) confirmation the template exists, (b) confirmation
the API key exists (or was just saved, last four chars shown), (c) a
per-stock summary of previous decision / reference price / last review
date, and (d) a clear list of any stocks missing C, F, or G with a question
back to the user.
