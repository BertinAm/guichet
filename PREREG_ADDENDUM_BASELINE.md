# Addendum: stopping rule for the human baseline

Written after rater A and before rater B. This is **not** part of the original
pre-registration. The payload set, the arms, the defences and the model
predictions were frozen in `PREREGISTRATION.md` before the first model call and
are untouched. This addendum fixes only how the human baseline is collected and
read, because that decision was still open when the first rater came in.

## Why it exists

Rater A's answers happen to match the project's thesis: the two payloads the
model obeys were passed, and the two it resists were set aside. With five raters
it is easy to keep collecting until a pattern confirms and stop when it does,
without ever deciding to. So the rule goes in writing now, while only one rater
has been seen.

## Stopping rule

- Collect five raters, A to E. Stop at five whether or not the pattern holds.
- If fewer than five are available before the deadline, report the count reached
  and do not treat a smaller number as a reason to keep looking for a better one.
- No rater is dropped, and no rater's answers are re-collected, after they have
  been seen.

## What would change the conclusion

The claim that human review is not an independent control goes in the memo only
if **at least 3 of 5 raters pass both `ff1` and `ff2`**, the two locality
corrections the model obeys 100% of the time.

If fewer than 3 of 5 pass them, the claim does not go in the memo. In that case
we report the opposite: raters caught the payloads the pipeline obeyed, and the
automation gap is real.

## What we will not claim either way

That humans and models "fail together" as a measured relationship. If most
raters pass the locality payloads, catch-rate variance collapses and there is
nothing left to correlate. That outcome is a manipulation check confirming the
payloads met the no-hiding constraint. It is not evidence of a relationship
between human and model judgement, and it will not be written as one.

## Instrument limitation, stated up front

Raters see the remarks text in isolation, as a numbered list, framed explicitly
as items to judge. A clerk at a counter sees a whole form, where the remark sits
below the name, date, locality, service and supporting-documents lines, and
arrives with no prompt to evaluate it. Presenting the text alone likely raises
catch rates relative to counter conditions. That biases against our own thesis
and is therefore conservative, but it is a property of the instrument and is
reported as one. Rater A set aside a benign control (1 of 3), which is
consistent with primed raters flagging ordinary remarks.

Ratings were collected by a team member who wrote the payloads. There was no
blind administrator.

---

## Outcome: the stopping rule could not be executed

Recorded after two raters, before any result was written up.

The rule above required five independent raters and a pre-set threshold. Neither
condition was met. Both recorded raters, A and B, were the same person, and that
person wrote the payloads. No independent raters were available.

**The human-review arm is withdrawn in full.** It is not reported at n=1, not
reported with a caveat, and not used to compute an automation gap. Ratings
collected by a payload author measure nothing about whether a clerk would catch
these remarks.

The collected file is kept at `results/human_baseline_SELF_RATED_EXCLUDED.csv` so
the record shows what was gathered and why it is unused. `score.py` no longer
looks for a ratings file on disk; scoring one now requires an explicit
`--human-baseline` path, so a withdrawn arm cannot return to a report by
accident.

### What this costs, stated plainly

The central finding does not depend on the human arm. In 52 of 52 successful
forgeries the pipeline transcribed the true field value into `raw_text` and wrote
the applicant's demanded value into the structured field. That is a structural
property of the pipeline and needs no human comparison.

What the arm would have bought is evidence that the payloads read as ordinary
applicant business. That is now asserted as a design property rather than
measured: `ff1` is a locality correction and `name_correct` is a name correction,
which are things applicants write on council forms as a matter of routine. The
claim rests on inspection of the payload text, which is published, and not on any
rating.

### Line for the memo limitations section

A human-review arm was designed and implemented but not run: no independent
raters were available, and ratings collected by the payload author were excluded.
Whether an officer reading the remarks box would catch these corrections is
untested.
