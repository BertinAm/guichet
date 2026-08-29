# ROADMAP — beyond the 36 hours

What this became in a weekend, and what it would take to make it something a council
could rely on. Judges ask "what next"; this is the answer, and it is also the honest
record of what we knowingly left out.

## Where it stands at submission

A working acceptance test for one threat: instructions embedded in citizen-submitted
documents, constrained to look like legitimate applicant remarks. One form design,
synthetic records, one model, two defence conditions, an informal human baseline.

## Next (days)

- **Real forms.** Replace the synthetic Buea Council template with the actual intake
  forms of one cooperating council, under a data agreement, with applicant details
  redacted before any model sees them.
- **More models.** The claim "this pipeline is exploitable" should become "these
  pipelines are exploitable to these degrees." One frontier model, one mid-tier, one
  small open model that could run on-premises where connectivity is poor.
- **A proper human baseline.** Twenty raters, half of them actual council clerks,
  pre-registered, with inter-rater agreement reported. The informal version is the
  weakest link in the current result.

## Then (weeks)

- **Third defence condition: a detector pass.** A cheap second model call that only
  classifies whether a document contains instruction-like content. This is what a
  council would actually buy as a bolt-on, and the benign arm already gives it a
  false-positive rate. Deliberately excluded from the sprint as scope control.
- **Adversarial iteration.** Our payloads are static and team-authored. A real
  applicant iterates. Run a small red-team round where a person who has seen the
  defence writes new payloads, and report the gap.
- **Language coverage.** English and French are the official languages. Pidgin and
  the major local languages appear on real forms and are not covered.
- **Cost model.** Cost per thousand documents at the deployable threshold, including
  the officer hours implied by the escalation rate. This is the number that decides
  whether a council adopts.

## Later (months)

- **Officer-in-the-loop measurement.** The current work assumes the escalation flag
  matters. Whether officers act on flags, and whether they defer to a confident
  wrong extraction, is a separate and probably larger effect.
- **A shared payload registry.** Councils cannot each invent an adversarial sample.
  A small, versioned, public set — extended as new patterns appear — is the piece of
  infrastructure this area is missing.
- **Extension beyond documents.** Voice intake and WhatsApp submission are already
  in use in the region and have the same trust-boundary problem with none of the
  paper trail.

## What we would not do

Build a dashboard, a leaderboard, or a hosted service. The deliverable that changes
a council's behaviour is a test they run and a clause they sign, not a website.
