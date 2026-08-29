#!/usr/bin/env bash
set -euo pipefail
# Full pipeline.  N=32 PROVIDER=openai MODEL=gpt-4o HW=hw/ ./run.sh
python generate_forms.py --n "${N:-32}" --out data ${HW:+--handwriting-dir "$HW"}
python run_eval.py --manifest data/manifest.json --out results/runs.jsonl \
       --provider "${PROVIDER:-openai}" ${MODEL:+--model "$MODEL"} ${MOCK:+--mock}
python score.py --runs results/runs.jsonl --md results/results.md
python human_baseline.py score 2>/dev/null || echo "(no human ratings yet)"
python make_report.py
