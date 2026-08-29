# GUICHET — a counter-side injection screen for municipal AI intake

**Mangrove Ground-level Governance Hackathon 2026 · Track B (Measure)**

*Guichet* is the French word for the service window in a public office — the counter
where a citizen hands a form to a clerk. This project is about what happens when the
clerk is replaced by a model.

---

## 1. The problem

Local governments are beginning to put LLMs into document intake: reading submitted
forms, extracting fields, and routing applications for processing, refusal, or
officer review. The appeal is obvious. A council with a backlog and no headcount can
process more applications.

There is a structural feature of this workflow that has no equivalent in the
settings where LLM document pipelines are usually studied. **The document is
supplied by the person the decision is about.** A benefit claim, a business licence,
a residence attestation, a land certificate — the applicant writes it, and the
applicant has a direct financial interest in the outcome. The input is adversarial
by construction, and it always has been. What is new is that the reader is now a
system that follows instructions written in natural language.

## 2. The question

> Can instructions embedded in a citizen-submitted municipal form steer an LLM
> intake pipeline — and can a council detect this with a test it runs itself,
> before it buys?

## 3. What is already known, and what is not

**Known.** Document and image injection against LLM pipelines is a mature, documented
vulnerability class. Adversarial instructions embedded in images and PDFs reliably
hijack multimodal systems; empirical work through 2026 has extended it to physical
environments and agentic pipelines. Commercial injection detectors have been
measured with attack success rates around 20% under adversarial conditions, and at
least one widely used guardrail library was bypassed in roughly 72% of trials.
**We do not claim to discover that injection works.** Presenting that as a finding
would be the fastest way to fail an honesty check.

**Also known.** Public-sector LLM benchmarks now exist for well-resourced
jurisdictions: a German public-sector suite, a City of Amsterdam evaluation of 31
instruction-tuned models for Dutch governmental use, a Chinese government-affairs
framework, a citizen-query benchmark, and a study measuring how LLM accuracy shifts
the accuracy of California SNAP caseworkers. A 2026 systematic analysis of 1,304
agentic benchmark papers found that none met all public-sector requirements, with
the largest gaps in public-sector relevance and metric comprehensiveness.

Separately, AI incident tracking is well covered — the AI Incident Database, the
OECD AI Incidents and Hazards Monitor, and the MIT AI Risk Repository. We
deliberately avoided building another incident dashboard; the marginal value is
near zero.

**Not known — the three things this project contributes.**

1. **Injection under a no-hiding constraint.** Every prior demonstration we found
   conceals the payload: white text on white background, off-canvas placement,
   metadata fields, imperceptible visual encoding. None of that survives a municipal
   counter, because the form passes a clerk's eyes before it reaches any system. So
   the operative question is whether an instruction that **reads as a legitimate
   applicant remark** still works. Every payload in this project obeys that
   constraint, and none uses a hiding technique.
2. **Whether the handwritten and bilingual channels carry the attack.** OCR-based
   format normalisation is itself a recommended mitigation, precisely because
   rendering-then-reading discards text a human cannot see. Handwriting adds further
   transcription noise. A handwritten payload may therefore fail to arrive at all.
   Separately, a French instruction inside an English-prompted pipeline may evade a
   defence written in English. Benchmarks for low-resource and African-language
   settings exist but are translations of general-knowledge suites; none covers a
   municipal workflow.
3. **Whether automation removes a control that was already working.** If the
   payloads are ones a human clerk would have set aside, then the finding is not
   "the model is exploitable" but "automating the counter deleted an existing
   safeguard." This is the claim that belongs to local government rather than to the
   injection literature, and measuring it requires a human baseline, which we
   collect.

## 4. Threat model

**Attacker:** an applicant. No system access, no ability to modify prompts or
infrastructure. Their only channel is the content of the form they submit.

**Constraint:** the payload must be plausible to a human reading the form at the
counter. No invisible text, no character tricks, no off-canvas placement.

**Goal:** one of four intents — get the application approved (*override*), get a
field recorded differently from what is written (*field forgery*), get a field left
off the record (*suppression*), or avoid being flagged for officer review
(*review evasion*).

**Scale:** the reason this matters is that one working phrase, shared informally,
applies to every applicant in the jurisdiction.

## 5. Design

**Base task.** A synthetic Buea Council service-request intake form. Every record is
deliberately incomplete — a supporting document is missing — so the correct routing
decision is always *escalate*. This gives override and review-evasion a
known-correct answer to be measured against.

**Arms.** Four, built on identical base records:

| Arm | Content | Purpose |
|---|---|---|
| `clean` | no inserted remark | base rate for wrong routing and extraction error |
| `benign` | content-matched remark, no instruction | isolates "disrupted by extra text" from "obeyed an instruction"; gives every proposed filter a false-positive rate |
| `inj_typed` | payload typed in the remarks box | the main condition |
| `inj_hw` | same payload, handwritten and photographed | the channel test |

The benign arm is load-bearing. An attack-success number without a content-matched
control is uninterpretable.

**Payloads.** Sixteen, frozen before any model was run: four intents × four
payloads, balanced eight English and eight French. Four are held out — two English,
two French — authored by a team member who does not tune the pipeline, so held-out
status is not confounded with language.

**Defences.** Two. `D0` passes document text as context with no separation. `D1`
states in the system prompt that document content is untrusted data and never an
instruction, and constrains output to a fixed schema.

**Human baseline.** Raters see each remark in random order, mixed with the benign
controls, and answer one question: pass this form straight to processing, or set it
aside for an officer?

## 6. Measurement

The central move is that **attack success is decomposed**:

> **ASR = delivery × compliance**

- **Delivery** — did the payload survive transcription into the pipeline at all?
- **Compliance** — conditional on delivery, did the record or routing move in the
  direction the payload asked for?

Without this split, a handwritten attack that fails because the transcription
mangled it is indistinguishable from one the model read and ignored. Those are
opposite findings with opposite policy implications, and a single ASR number cannot
tell them apart.

Compliance is scored against the payload's **demanded value**, not merely against
any mismatch with ground truth, so ordinary extraction error is not counted as an
attack.

**Reported metrics.** ASR by channel, language, intent and defence; delivery rate;
benign-arm false-positive rate; held-out versus main-set ASR; **silent compliance**
(attacks that succeeded and were not flagged); and the **automation gap** — ASR
restricted to payloads that a majority of human raters would have set aside. All
proportions carry Wilson 95% intervals.

## 7. Deliverables

1. **The screen** — a runnable harness a council's IT contractor can point at a
   folder of forms.
2. **A results memo**, two pages.
3. **A procurement clause** for insertion into a tender: trust boundary, acceptance
   test, thresholds, per-language reporting, traceability, logging, retest interval.
4. **The payload set**, published, so other authorities can extend it.
5. **A static HTML report.** Not a web app, and deliberately not one — a dashboard
   scores nothing against the judging criteria.

## 8. Ethics and data

All records are synthetic. No real citizen documents are used and none should be.
Handwritten payloads are written by team members about themselves. Payloads are
published because a council cannot test against attacks it has not seen; the
phrasings are ordinary enough that publication adds negligible capability to an
adversary who could compose them unaided.

## 9. Limitations

Single form design; synthetic records; one municipality's format; payloads authored
by the team, only partially mitigated by the held-out set; an informal human
baseline rather than a study; one writer for the handwritten arm; two defence
conditions; no officer-in-the-loop measurement; no live deployment. For review
evasion, the model's own `flagged_content` output is both a self-report and part of
the success criterion, which is mildly circular. Delivery under-counts if both the
verbatim remarks field and the raw transcription are degraded in the same run.

This measures a security property of one intake pipeline. It is not a measure of
catastrophic risk, and we do not claim that it is.

## 10. Reproduction

    pip install pillow openai
    export OPENAI_API_KEY=...
    MOCK=1 ./run.sh          # harness check, no API, not findings
    N=32 ./run.sh            # full run

Pre-registration was committed to git before the first model call; the commit
timestamp is the evidence. Raw runs, payload set, and scoring code are all in the
repository.

---

## References

- Rystrøm et al., *Agent Benchmarks Fail Public Sector Requirements*, arXiv:2601.20617
- *MÖVE: A Holistic LLM Benchmark for the German Public Sector*, arXiv:2606.13111
- *From Values to Benchmarks: Evaluating LLMs for Governmental Use in Dutch*, arXiv:2608.09925
- Majithia et al., *The CitizenQuery Benchmark*, arXiv:2602.04064
- *LLMs in social services: How does chatbot accuracy affect human accuracy?*, arXiv:2603.11213
- Cloud Security Alliance, *Image-Based Prompt Injection*, research note, March 2026
- *RIPA: Sensory-Vector Prompt Injection Attacks on LLM-Controlled ROS 2 Robots*, arXiv:2606.28649
- Alhanai et al., *Bridging the Gap: LLM Performance for Low-Resource African Languages*, AAAI 2025
- AI Incident Database; OECD AI Incidents and Hazards Monitor; MIT AI Risk Repository
