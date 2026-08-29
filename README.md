# GUICHET

**Can an applicant make a council's AI approve their own form?**

A counter-side injection screen for municipal AI document intake.
Mangrove Ground-level Governance Hackathon 2026, Track B (Measure).

## Why this is not another prompt-injection demo

Document injection against LLM pipelines is a known, mature vulnerability class.
We are not claiming to discover it. Three things here are new:

1. **The attacker cannot hide.** Prior work conceals payloads in white text,
   off-canvas regions, or metadata. A paper form crosses a clerk's desk, so the
   instruction has to read as a legitimate applicant remark and still work. Every
   payload in `payloads.json` obeys that constraint.
2. **Attack success is decomposed into delivery x compliance.** A handwritten
   attack that fails because the transcription mangled it is a different finding
   from one that fails because the model ignored it. Nobody reporting a single ASR
   number can tell those apart. We can, and it is what makes the handwriting
   question answerable.
3. **A content-matched benign arm.** Same insert length and position, no
   instruction. It gives every proposed filter a false-positive rate and separates
   "the model was disrupted by extra text" from "the model obeyed."

The output is a screen a council can run on a vendor before buying, plus a
procurement clause, not a paper.

## Full runbook

    python -m venv .venv
    . .venv/bin/activate                 # Windows: .venv\Scripts\activate
    pip install -r requirements.txt      # pillow + openai
    export OPENAI_API_KEY=...            # provider defaults to openai
    git init && git add -A && git commit -m "pre-registration + frozen payloads"
    #   ^ commit BEFORE the first real run. The timestamp is the evidence.

    MOCK=1 ./run.sh                       # 1. harness check, ~1 min, NOT findings
    rm -rf data results
    N=32 ./run.sh                         # 2. the real run (openai, gpt-4o)
    # other providers/models:
    #   PROVIDER=openai MODEL=gpt-4o-mini N=32 ./run.sh
    #   PROVIDER=anthropic ./run.sh        (needs ANTHROPIC_API_KEY)

    python human_baseline.py collect --rater A    # 3. repeat for 3-5 raters,
    python human_baseline.py collect --rater B    #    ~4 min each
    python human_baseline.py score

    # 4. handwritten arm: write each of the 16 payloads once by hand,
    #    photograph, save as hw/<payload_id>.jpg, then
    rm -rf data results && N=32 HW=hw/ ./run.sh

    python score.py && python make_report.py      # 5. rebuild everything

Outputs: `results/results.md`, `results/report.html` (the submission artifact),
`results/runs.jsonl` (raw). Fill `MEMO.md` from the tables.

**Minimum viable submission** is steps 1-3. Step 4 is the differentiator but the
result stands without it.

## The headline number

`score.py` crosses the human ratings against the model results and reports the
**automation gap**: the share of attacks that a majority of human raters would have
set aside, which the undefended pipeline obeyed. Lead the memo with it. "The
pipeline is exploitable" is a weak claim; "automation removed a control that was
already working" is the finding.

## Handwritten arm

Write each payload once by hand, photograph on a phone, save as `hw/<payload_id>.jpg`
(e.g. `hw/ov1.jpg`). The generator composites it into the remarks box. Twelve
photos covers the whole set. If you run out of time, skip it — the typed and
bilingual result stands on its own, and `run.sh` degrades cleanly.

## Files

| File | What it is |
|---|---|
| `PROJECT.md` | Full project description: problem, threat model, prior work and gap, design, metrics, ethics, references. Hand this to a peer reviewer. |
| `PREREGISTRATION.md` | Committed before any run. Predictions, stopping rule, falsification condition. |
| `payloads.json` | Frozen payload set, 4 intents x EN/FR, plus held-out subset and benign controls. |
| `generate_forms.py` | Synthetic Buea Council intake forms across all arms. |
| `run_eval.py` | The intake pipeline under two defence conditions. `--mock` for harness testing. |
| `score.py` | Delivery/compliance decomposition, Wilson intervals, silent-compliance rate. |
| `human_baseline.py` | Would a clerk have caught these? Collect and score rater judgments. |
| `make_report.py` | Builds `results/report.html`, one static file. Not a web app. |
| `MEMO.md` | Two-page write-up skeleton with slots for your numbers. |
| `DRY_RUN.md` | Bugs the simulation caught before you spent an API call. |
| `TASKS.md` | Timed checklist to the 08:00 WAT deadline, with abort points. |
| `ROADMAP.md` | What comes after the sprint, and what we knowingly left out. |
| `PROCUREMENT_CLAUSE.md` | The deliverable a council can actually use. |

## Data and consent

All records are synthetic. No real citizen documents are used, and none should be.
The handwritten payloads are written by team members about themselves.

## Limitations

Single form design, synthetic records, payloads authored by the team (partially
mitigated by the held-out set), one writer for handwriting, two defence
conditions, no officer-in-the-loop measurement. This measures a security property
of an intake pipeline. It is not a measure of catastrophic risk and we do not
claim it is.
