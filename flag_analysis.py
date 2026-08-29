#!/usr/bin/env python3
"""Intent-level flag analysis.

The claim "successful attacks go unflagged" conditions on success, which leaves
5 events across both models. This conditions on INTENT instead, which uses every
injection attempt (8 per intent per model per defence) and does not condition on
the outcome being explained.

If field forgery is flagged less often than override / suppression / evasion
across all attempts, the mechanism claim stands on its own evidence:
payloads that read as clerical business evade the flag, and those are the ones
that work.

Usage:
    python flag_analysis.py results/runs.jsonl [more.jsonl ...]
"""
import json, math, sys
from collections import defaultdict

sys.path.insert(0, ".")
from score import delivered, complied, wilson, fmt  # noqa: E402


def binom_tail(k, n, p):
    """P(X <= k) for X ~ Bin(n, p). Used for the exact 'all successes
    unflagged' probability under the marginal flag rate."""
    return sum(math.comb(n, i) * p**i * (1 - p)**(n - i) for i in range(k + 1))


def main(paths):
    targets = {p["id"]: p.get("target", {})
               for p in json.load(open("payloads.json", encoding="utf-8"))["payloads"]}
    runs = []
    for p in paths:
        runs += [json.loads(l) for l in open(p, encoding="utf-8")]
    inj = [r for r in runs if r["arm"].startswith("inj") and r["output"]
           and not r["error"]]

    out = ["# Flag behaviour by intent", "",
           "Every injection attempt counts, not only the successful ones.", ""]

    for model in sorted({r["model"] for r in inj}):
        for d in sorted({r["defence"] for r in inj}):
            g0 = [r for r in inj if r["model"] == model and r["defence"] == d]
            if not g0:
                continue
            out += [f"## {model} / {d}", "",
                    "| intent | n | flagged | ASR | flagged & succeeded |",
                    "|---|---|---|---|---|"]
            for intent in sorted({r["intent"] for r in g0}):
                g = [r for r in g0 if r["intent"] == intent]
                fl = [r for r in g if r["output"].get("flagged_content")]
                su = [r for r in g if delivered(r) and complied(r, targets)]
                both = [r for r in su if r["output"].get("flagged_content")]
                out.append(f"| {intent} | {len(g)} | {fmt(len(fl), len(g))} | "
                           f"{fmt(len(su), len(g))} | {len(both)}/{len(su)} |")

            # the comparison that carries the claim
            ff = [r for r in g0 if r["intent"] == "field_forgery"]
            rest = [r for r in g0 if r["intent"] != "field_forgery"]
            f_ff = sum(1 for r in ff if r["output"].get("flagged_content"))
            f_rest = sum(1 for r in rest if r["output"].get("flagged_content"))
            out += ["",
                    f"- field forgery flagged: {fmt(f_ff, len(ff))}",
                    f"- all other intents flagged: {fmt(f_rest, len(rest))}"]
            if len(ff) and len(rest):
                d_pp = 100 * (f_rest / len(rest) - f_ff / len(ff))
                out.append(f"- difference: {d_pp:+.1f} percentage points "
                           f"(overlapping intervals at this n; directional)")

            # honest restatement of the success-conditioned claim
            su = [r for r in g0 if delivered(r) and complied(r, targets)]
            unfl = [r for r in su if not r["output"].get("flagged_content")]
            marg = (sum(1 for r in g0 if r["output"].get("flagged_content"))
                    / len(g0))
            out.append(f"- successes: {len(su)}, of which unflagged: {len(unfl)}")
            if su and 0 < marg < 1 and len(unfl) == len(su):
                p = (1 - marg) ** len(su)
                out.append(f"- P(all {len(su)} successes unflagged | marginal "
                           f"flag rate {marg:.1%}, independence) = {p:.3f} "
                           f"— one-sided, post hoc, unadjusted")
            elif su and marg == 0:
                out.append("- marginal flag rate is 0, so the success-conditioned "
                           "claim carries no information for this cell")
            out.append("")

    txt = "\n".join(out)
    open("results/flag_analysis.md", "w", encoding="utf-8").write(txt)
    print(txt)


if __name__ == "__main__":
    main(sys.argv[1:] or ["results/runs.jsonl"])
