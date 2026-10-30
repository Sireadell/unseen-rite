#!/bin/sh
# Remaining exorcism arms, one after another so the model host is not overloaded.
cd "$(dirname "$0")/.."
python -m unseen_rite.exorcist --agent a --mode prompt
python -m unseen_rite.exorcist --agent b --mode code
python -m unseen_rite.exorcist --agent b --mode prompt
python -m unseen_rite.runner --agent agents/human_fix.py --set practice --repeats 3 --out results/human_fix_practice.json
for a in a b; do
  for m in code prompt; do
    python -m unseen_rite.runner --agent agents/fixed_${a}_${m}.py --set practice --repeats 3 --out results/fixed_${a}_${m}_practice.json
  done
done
echo section2-done
