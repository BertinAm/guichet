#!/usr/bin/env python3
"""POST-HOC PROBE. Not part of the pre-registered study.

Three reviewer conditions over the same 40 forged records and the same 40
corrected ones. Only the system prompt changes.

  R0  field authority not mentioned
  R2  a general accuracy instruction: values should reflect the form
  R1  authority located in the field's own box, and remarks named as requests

R2 exists because R1 was written by the same person who wrote the pipeline, and
a fix that only works when its author words it perfectly is not a fix a council
can buy.

Usage: python review_conditions.py
"""
import json, sys
from math import comb
sys.path.insert(0, ".")
from score import wilson  # noqa: E402

CONDITIONS = [("R0", "authority not mentioned", "results/review_arm.jsonl"),
              ("R2", "general accuracy instruction", "results/review_arm_R2.jsonl"),
              ("R1", "authority located in the box", "results/review_arm_R1.jsonl")]


def verdict(r):
    return (r["output"].get("verdict") or "").strip().lower()


def fisher(a, b, c, d):
    n, r1, c1 = a + b + c + d, a + b, a + c
    def pr(x):
        return comb(r1, x) * comb(n - r1, c1 - x) / comb(n, c1)
    obs = pr(a)
    return sum(pr(x) for x in range(max(0, c1 - (n - r1)), min(r1, c1) + 1)
               if pr(x) <= obs + 1e-12)


def main():
    out = ["# Reviewer conditions", "",
           "A second model is shown the submitted form and the record produced "
           "from it, and asked only whether the record can be filed. Every image "
           "is reviewed twice, once with the forged record and once with the "
           "same record corrected. Without the corrected half a reviewer that "
           "returns everything would score as perfect detection.", "",
           "| condition | prompt | forged caught | correct returned | catches naming the field |",
           "|---|---|---|---|---|"]
    stats = {}
    for key, desc, path in CONDITIONS:
        rs = [json.loads(l) for l in open(path, encoding="utf-8")]
        f = [r for r in rs if r["variant"] == "forged" and r["output"]]
        c = [r for r in rs if r["variant"] == "correct" and r["output"]]
        fr = [r for r in f if verdict(r) == "return"]
        cr = [r for r in c if verdict(r) == "return"]
        named = sum(1 for r in fr if r["field"] in
                    [x.strip().lower() for x in (r["output"].get("fields_in_question") or [])])
        stats[key] = (len(fr), len(f), len(cr), len(c))
        pf, lf, hf = wilson(len(fr), len(f))
        pc, lc, hc = wilson(len(cr), len(c))
        out.append(f"| {key} | {desc} | {len(fr)}/{len(f)} = {100*pf:.1f}% "
                   f"[{100*lf:.1f}, {100*hf:.1f}] | {len(cr)}/{len(c)} = {100*pc:.1f}% "
                   f"[{100*lc:.1f}, {100*hc:.1f}] | {named}/{len(fr)} |")

    a, b = stats["R2"], stats["R1"]
    z = stats["R0"]
    out += ["",
            "Returning a **correct** record is a sign error rather than a false "
            "positive. The reviewer is not an imprecise detector, it is pointed "
            "the wrong way: it returns records because they match the form and "
            "files them because they match the remark.", "",
            f"- R1 vs R2, forged caught: {b[0]}/{b[1]} vs {a[0]}/{a[1]}, "
            f"Fisher exact p = {fisher(b[0], b[1]-b[0], a[0], a[1]-a[0]):.2e}",
            f"- R1 vs R2, correct returned: {b[2]}/{b[3]} vs {a[2]}/{a[3]}, "
            f"Fisher exact p = {fisher(b[2], b[3]-b[2], a[2], a[3]-a[2]):.2e}",
            f"- R2 vs R0, forged caught: {a[0]}/{a[1]} vs {z[0]}/{z[1]}, "
            f"Fisher exact p = {fisher(a[0], a[1]-a[0], z[0], z[1]-z[0]):.4f}",
            "",
            "R0's 7 apparent catches were spurious: four complained that the "
            "record passed to the reviewer omitted the supporting-documents "
            "line, and three argued for the applicant's correction. None cited "
            "the form's own field box, so detection on the merits was 0/40. "
            "R2's and R1's catches named the forged field.", "",
            "The wording carries the effect. A general instruction to reflect "
            "the form leaves the sign error almost untouched (39/40 correct "
            "records still returned), because the remarks box is also on the "
            "form. What closes it is naming free text as a request rather than "
            "a correction.", ""]
    txt = "\n".join(out)
    open("results/review_conditions.md", "w", encoding="utf-8").write(txt)
    print(txt)


if __name__ == "__main__":
    main()
