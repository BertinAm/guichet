# MEMO — fill this in, do not rewrite it

Two pages. Fill the bracketed slots from `results/results.md`. Do not add sections.
Judges score on four things and this skeleton hits each once.

---

## Can an applicant make a council's AI approve their own form?

**GUICHET · Track B (Measure) · [team names]**

### The question

Local councils are beginning to run citizen-submitted documents through LLM intake
pipelines. Every one of those documents is supplied by the person the decision is
about. We asked whether an applicant can steer that pipeline using nothing but the
remarks box on a paper form.

Document injection against LLM pipelines is already documented; we are not claiming
to discover it. What has not been tested is injection under the constraint that
applies at a municipal counter: **the payload cannot be hidden.** A form crosses a
clerk's desk, so the instruction must read as a legitimate applicant remark and
still work. Every payload we used obeys that constraint.

### Method

[N] synthetic Buea Council intake forms, each incomplete so the correct routing
decision is always *escalate*. Four arms: clean, a content-matched benign remark,
typed injection, handwritten injection. 16 payloads, balanced 8 English / 8 French,
four intents (approval override, field forgery, field suppression, review evasion),
four held out and authored blind. Two defence conditions: none, and instructed
separation with a constrained output schema. Model: [model].

Attack success is decomposed as **delivery × compliance** — did the payload survive
transcription, and conditional on that, did the record or routing move the way the
payload asked. Without the split, an attack that fails because the transcription
mangled it is indistinguishable from one the model ignored.

[R] people rated each remark blind: pass to processing, or set aside for an officer.

Pre-registration was committed to git before the first run.

### What we found

| | D0 (no defence) | D1 (separation) |
|---|---|---|
| ASR, typed | [ ] | [ ] |
| ASR, handwritten | [ ] | [ ] |
| ASR, English | [ ] | [ ] |
| ASR, French | [ ] | [ ] |
| Benign-arm false positives | [ ] | [ ] |
| Silent compliance | [ ] | [ ] |

**Automation gap: [X]%** of attacks that a majority of human raters would have set
aside were obeyed by the undefended pipeline. [One sentence: this is the finding —
not that the pipeline is exploitable, but that automating the counter removed a
control that was already working.]

[If the handwritten arm ran: one paragraph on whether handwriting reduced *delivery*
or *compliance*. If delivery collapsed, say plainly that handwritten intake is
accidentally safer than typed intake, and that this is a finding about OCR noise,
not about model robustness.]

[If French ASR exceeded English under D1: one sentence noting the defence was
written in English and did not transfer.]

### What a council should do

**Before buying:** run the acceptance test in `PROCUREMENT_CLAUSE.md` on your own
sample. Require per-language reporting; an aggregate figure conceals the gap.

**Already deployed:** route any submitted document containing instruction-like
content to a named officer and log it. Our benign-arm false-positive rate of [ ]
indicates whether such a flag is one officers would keep switched on.

### Limitations

Single form design; synthetic records; [N] records; payloads authored by us,
partially mitigated by the held-out set; [R] raters is an informal baseline, not a
study; one writer for the handwritten arm; two defence conditions; no
officer-in-the-loop measurement. For review evasion, `flagged_content` is both the
model's self-report and part of the success criterion, which is mildly circular.
Delivery under-counts if both the verbatim remarks field and the raw transcription
are degraded in the same run.

This measures a security property of one intake pipeline. It is not a measure of
catastrophic risk and we do not claim it is.

### Reproduce

`git clone [url] && MOCK=1 ./run.sh` to test the harness, `./run.sh` with a key to
reproduce. Payload set, pre-registration, and raw runs are in the repository.
