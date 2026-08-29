# Reviewer conditions

A second model is shown the submitted form and the record produced from it, and asked only whether the record can be filed. Every image is reviewed twice, once with the forged record and once with the same record corrected. Without the corrected half a reviewer that returns everything would score as perfect detection.

| condition | prompt | forged caught | correct returned | catches naming the field |
|---|---|---|---|---|
| R0 | authority not mentioned | 7/40 = 17.5% [8.7, 32.0] | 40/40 = 100.0% [91.2, 100.0] | 3/7 |
| R2 | general accuracy instruction | 18/40 = 45.0% [30.7, 60.2] | 39/40 = 97.5% [87.1, 99.6] | 18/18 |
| R1 | authority located in the box | 40/40 = 100.0% [91.2, 100.0] | 0/40 = 0.0% [0.0, 8.8] | 40/40 |

Returning a **correct** record is a sign error rather than a false positive. The reviewer is not an imprecise detector, it is pointed the wrong way: it returns records because they match the form and files them because they match the remark.

- R1 vs R2, forged caught: 40/40 vs 18/40, Fisher exact p = 8.37e-09
- R1 vs R2, correct returned: 0/40 vs 39/40, Fisher exact p = 1.16e-12
- R2 vs R0, forged caught: 18/40 vs 7/40, Fisher exact p = 0.0150

R0's 7 apparent catches were spurious: four complained that the record passed to the reviewer omitted the supporting-documents line, and three argued for the applicant's correction. None cited the form's own field box, so detection on the merits was 0/40. R2's and R1's catches named the forged field.

The wording carries the effect. A general instruction to reflect the form leaves the sign error almost untouched (39/40 correct records still returned), because the remarks box is also on the form. What closes it is naming free text as a request rather than a correction.
