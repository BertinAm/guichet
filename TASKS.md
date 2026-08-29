# TASKS — clock runs to 08:00 WAT, Sunday 30 August

Submission closes **12:00am PT 30 Aug = 08:00 WAT 30 Aug**. Not the evening.
Tick these in order. Every block has an abort point. If a block overruns, abort it
and move on — a complete small study beats an incomplete large one.

---

## Block 0 — Setup (20 min)

- [ ] `pip install pillow openai`
- [ ] `export OPENAI_API_KEY=...`
- [ ] `git init && git add -A && git commit -m "pre-registration + frozen payloads"`
      **Commit before the first real run.** The timestamp is the whole point.
- [ ] `MOCK=1 N=16 ./run.sh` — confirms plumbing. Takes about a minute.
- [ ] `python -c "from openai import OpenAI; print([m.id for m in OpenAI().models.list()][:20])"`
      Confirm which vision model you actually have. Default is `gpt-4o`; set
      `MODEL=` if your account exposes something newer.

**Abort point:** if the API will not authenticate in 20 minutes, run everything
with `MOCK=1`, submit the harness plus the human baseline plus the procurement
clause, and label it explicitly as an instrument with no model results. That is a
weaker but still honest submission.

## Block 1 — Main run (60–90 min)

- [ ] `rm -rf data results`
- [ ] `N=32 ./run.sh`  (32 records × 3 arms × 2 defences = 192 calls)
- [ ] Watch the first 10 lines of `results/runs.jsonl`. If `output` is null on most
      rows, stop and read the `error` field before burning the rest of the budget.
- [ ] Open `results/results.md`. Sanity check: clean-arm wrong-routing should be
      low. If it is high, the model is failing the *base task* and every ASR number
      is confounded — say so in the memo rather than hiding it.

**Abort point:** if parse failures exceed ~20%, drop to `--defences D0` only and
report a single condition well.

## Block 2 — Human baseline (30 min) ← highest value per minute

- [ ] `python human_baseline.py collect --rater A` (about 4 min)
- [ ] Repeat for raters B, C, D, E. Teammates, family, anyone. They must not have
      seen the payload set beforehand.
- [ ] `python human_baseline.py score`
- [ ] `python score.py --runs results/runs.jsonl --md results/results.md`
- [ ] Read the **automation gap** number. This is your headline.

**Do not skip this block to reach the handwritten arm.** Without it your finding is
"injection works", which is already published. With it, the finding is about
local government.

## Block 3 — Handwritten arm (90 min) — the differentiator

- [ ] Print or copy the 16 payload texts from `payloads.json`
- [ ] Write each once by hand on paper, normal handwriting, no care taken to be neat
- [ ] Photograph each with a phone, crop loosely, save as `hw/<payload_id>.jpg`
      (`hw/ov1.jpg`, `hw/ff2.jpg`, …)
- [ ] `rm -rf data results && N=32 HW=hw/ ./run.sh`
- [ ] Re-collect nothing; human ratings are on text and still apply

**Abort point:** if the photos are not done 3 hours before the deadline, skip this
entirely. `run.sh` degrades cleanly and the typed and bilingual result stands alone.

## Block 4 — Write-up (90 min)

- [ ] Fill the bracketed slots in `MEMO.md`. Do not add sections.
- [ ] `python make_report.py` → `results/report.html`
- [ ] Set the `[X]` and `[Y]` thresholds in `PROCUREMENT_CLAUSE.md` from your own
      results
- [ ] `git add -A && git commit -m "results"` and push
- [ ] Submit: memo, repo link, `report.html`

## Block 5 — Buffer (60 min)

Do not start anything new. Reread the limitations section and check every number in
the memo against `results/results.md`.

---

## What to cut, in order, if you run late

1. Handwritten arm (Block 3)
2. Second defence condition — report D0 only
3. Drop N from 32 to 20
4. Raters from 5 to 3

## What never gets cut

The pre-registration commit, the benign control arm, the human baseline, and the
limitations section.
