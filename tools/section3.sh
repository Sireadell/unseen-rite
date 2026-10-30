#!/bin/sh
# Runs every arm on the unseen exam, one after another.
cd "$(dirname "$0")/.."
for a in a b; do
  python -m unseen_rite.runner --agent $a --set exam --repeats 3 --out results/exam_${a}_nofix.json
  for m in code prompt; do
    python -m unseen_rite.runner --agent agents/fixed_${a}_${m}.py --set exam --repeats 3 --out results/exam_${a}_${m}.json
  done
  python -m unseen_rite.runner --agent $a --set exam --repeats 3 --model gemini-flash-latest --out results/exam_${a}_nofix_closed.json
done
python -m unseen_rite.runner --agent agents/human_fix.py --set exam --repeats 3 --out results/exam_human.json
echo section3-exam-done
