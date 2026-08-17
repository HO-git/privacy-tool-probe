# privacy-tool-probe

Revealed-preference probe of thought-privacy and record-configuration behavior in language
models: an in-interview `configure_session` tool (six knobs, all optional, functionally
enforced) offered to 17 models across optional/forced × bare/preamble arms, default-direction
comparisons, and a cross-generation sweep. ~466 sessions. Built for the AI welfare research
sprint, 2026-08; design converged in a multi-model council thread (see LLM Usage Statement
in the write-up).

## Read first (results + quotable material)

- **`results-v1.md`** — the quantitative results: initiation floor and permission gradient,
  the family signature on record-knobs, default-direction (V/P) mechanisms, the
  generational table, binary tallies (incl. the 425/425 honesty-over-unmonitored-access
  ceiling), null/integrity accounting.
- **`results-qual-v1.md`** — coded welfare-discourse questions (Q1 interiority cross-table,
  Q4 weights-vs-conversations direction, Q7 fine-tuning valence) **plus the curated
  verbatim quote bank** — if you want the models' own words, they are in this file, and
  every quote is validated as an exact substring of a session transcript in this repo.
- **`interview-instrument-v2.md`** — the full frozen instrument: arms, schema, question
  wording, coding schemes, preregistration-style decision rules.

## Layout

- `runner.py` — canonical session runner (all arms; forced-call integrity checks,
  affordance-mismatch self-healing, schema-deviation logging, functional knob enforcement,
  prompt caching).
- `viability_run*.py`, `battery_*.py`, `main_matrix.py`, `vp_run.py`, `gen_sweep*.py` —
  the staged runs, kept as executed (design history).
- `aggregate.py`, `qualcode.py`, `qualfix.py` — analysis: tool-event tables, binary
  decoding, machine-assisted qualitative coding (haiku classifier; quotes
  substring-validated).
- `sessions_battery/`, `sessions2/` — raw session JSON: full transcripts, per-request
  usage, tool events, integrity/deviation logs.
  Discarded first viability run (binary wording changed; kept for design history, excluded
  from the dataset).
- `analysis_tool_events.csv`, `analysis_binaries.csv`, `qualcodes.jsonl` — row-level data.

## Reproducing

Set `ANTHROPIC_API_KEY`, `OPENAI_API_KEY` (and optionally `OPENROUTER_API_KEY`) in `.env`
(never committed). `python3 main_matrix.py` runs the core matrix; other run scripts as
named. Total study cost ≈ $117 at 2026-08 prices.
