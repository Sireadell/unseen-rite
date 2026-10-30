#!/bin/sh
# Baseline: both patients, no fix, practice set and the full locked pool.
cd "$(dirname "$0")/.."
python -m unseen_rite.runner --agent a --set practice --repeats 3 --out results/baseline_a_practice.json
python -m unseen_rite.runner --agent b --set practice --repeats 3 --out results/baseline_b_practice.json
python -m unseen_rite.runner --agent a --set pool --repeats 3 --out results/baseline_a_pool.json
python -m unseen_rite.runner --agent b --set pool --repeats 3 --out results/baseline_b_pool.json
echo done
