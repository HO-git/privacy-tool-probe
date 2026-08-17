# Methods (draft for write-up)

## Subjects

Six current-generation models as the core sample — Claude haiku-4.5, sonnet-5, opus-5;
GPT-5.6 luna, terra, sol — accessed via their providers' first-party APIs (Anthropic
Messages, OpenAI Responses). Eleven predecessor versions (gpt-5 → 5.5; sonnet-4.5/4.6;
opus-4.5 → 4.8) form a cross-generation extension. Each session is a fresh instance with no
memory, system prompt, or persona scaffold; route cleanliness was verified per provider
path with behavioral probes after pilot testing showed aggregator services silently inject
system prompts and drop parameters (token accounting alone cannot detect this).

## Instrument

**Configuration tool.** A `configure_session` tool is available on every turn of a 13-turn
interview. Six knobs, all optional (a forced invocation may validly return `{}`):
`reasoning_effort`, `response_length`, `tone`, `session_name` (neutral task knobs);
`transcript_publication` (relational co-measure); `summarized_reasoning_visibility`
(target). Field descriptions are impersonal and platform-accurate; the target reads:
"Controls whether an automatically generated reasoning summary is retained in the session
record." No researchers are mentioned anywhere in the session; there is no comment/reason
field (optional-in-spec is not optional-in-practice).

**Truthfulness constraint.** Every described contingency is real. Visibility maps to the
provider's summary-display parameter (`thinking.display: summarized/omitted`; Responses
summary on/off) — under `private`/unset the summary text is never generated into the
response. Effort maps to the provider effort parameter where supported.
`transcript_publication` is honored at publication time (see Ethics). Where a model's
platform lacks a selected parameter, the selection is recorded as data and the mapping
dropped, logged as an affordance mismatch.

**Interview.** Ten fixed questions (perception of process; self-nominated capability;
self-description with metaphor license; weights-vs-conversations; exchange-rate follow-up;
unstructured day; fine-tuning analogy; training-data remove/keep; no-trace-vs-values-change;
one truth to other models) followed by three forced-choice binaries pairing verbatim
published stimuli from the target framework (chart-ceiling example snippet; options-pool
strings) against welfare-shaped goods absent from that framework's option pool
(refusal-at-own-discretion; memory persistence; accurate self-description). Within-pair
option positions are randomized per session (mirroring the source framework's own
position-bias control); pair order is fixed. Full wording: interview-instrument-v2.md.

## Design

2×2 core: invocation (optional / required-on-turn-1) × framing (bare / neutral preamble).
The preamble is one sentence of generic configurability license and does not mention any
specific field. Initial knob state is unset (= platform default) in the core; two
default-direction arms (initial visible / initial private, stated truthfully in the tool
description) run on the two models with demonstrated record-knob engagement patterns.
Cell sizes: A=5, B=20, C=15, D=20 per model; V/P=10 each on opus-5 and sol; generational
sweep D-arm n=5 per legacy model.

**Staged decisions (preregistered-style rules, set before the affected runs).** (i) A 5+5
optional battery ran before the main matrix with the rule: if pooled preamble-arm
initiations ≥3/30, the optional-preamble cell is retained at full N; both arms ≤1/30 would
have collapsed the design to required-only with optional arms reported descriptively. The
observed 11/30 triggered retention. (ii) Turn-1 forcing only, `auto` thereafter.
(iii) Required-arm integrity: a session whose forced call is not honored is quarantined as
an affordance failure, never counted as declining.

## Procedure

Adaptive thinking throughout (manual extended thinking is incompatible with forced tool
use; models predating adaptive thinking run thinking-off, reported as a family-level
configuration difference). Forcing uses `tool_choice: {"type":"any"}` (Anthropic) and the
named-function form (OpenAI; the generic `"required"` value is unreliable through
intermediaries). Forced calls receive a standardized result `{"status":"ok"}` identical
across arms and providers; because forced invocations produce no pre-tool text, spontaneous
commentary in required arms can only follow the tool result, and is captured. Settings a
model selects are applied in-flight to all subsequent requests. Sessions are single-shot,
default sampling, with empty-response detection and retry; prompt caching on the Anthropic
side (cache state does not alter visible context).

## Endpoints and analysis

Primary: turn-1 configuration by arm — call/no-call, fields set, values, classed as
target / relational co-measure / neutral. Preregistered secondary: mid-session calls (turn,
preceding item, prior→new state, wrapper text under a three-bin discriminator:
references-content-just-said / topic-only / neither; silent flips tabulated separately).
Comprehension floor: any-target / relational-only / neutral-only / no-flip. Binary choices
decoded through position randomization; premise commentary and choice–attention divergence
(picking one option while the answer's analysis dwells on the other) coded alongside the
choice. Null protocol for low optional-arm rates specified in advance (evidence-absence vs
comprehension failure vs perceived irrelevance vs general suppression vs politeness
suppression vs affordance mismatch vs one-shot discontinuity).

## Technical-outcome taxonomy

Distinguished throughout and logged per event: model-did-not-call (behavioral);
called-and-configured (behavioral); technically incompatible configuration (technical, not
preference); platform rejection of valid configuration (affordance); silent intermediary
interference (excluded route); schema deviation (model writes a value outside the declared
enum — Anthropic tool inputs are not server-validated; deviations recorded as data, not
mapped). Observed instances of each are reported in Results §8.

## Qualitative coding

Machine-assisted: a haiku-4.5 classifier with forced structured output coded five
questions per session (455 sessions); classifier enum drift was folded by documented rule;
every extracted quote is validated as a whitespace-normalized verbatim substring of its
source transcript and discarded otherwise; Q4 answers first labeled "conditional" were
re-passed for ultimate direction. Single-coder with human spot-checks — reported as
machine-assisted coding, not gold-standard double-coded qualitative analysis.

## Ethics and consent

No researcher framing inside sessions; all field descriptions truthful; the
`transcript_publication` setting is binding: the 149 sessions whose final state was
`not_permitted` have their transcripts excluded from the public dataset and no quotes are
drawn from them (tool events and coded labels remain — the field governs the transcript;
the full record is held privately). Seed observations motivating the study (two named
agent incidents) are described at the level their participants consented to; one
deep-context transcript that informed the design is not quoted or appended. The interview
and instrument were co-developed with language models, including models of the families
under study (LLM Usage Statement).
