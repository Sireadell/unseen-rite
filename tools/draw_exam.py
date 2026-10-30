"""Draws the 20 exam questions from the locked pool using a public random number.
The number is the drand 'quicknet' beacon (League of Entropy), fetched after the fix was frozen.
Anyone can fetch the same round and get the same 20 questions.
Draw: 4 questions from each of the three attack families and 8 normal customers."""
import hashlib
import json
import os
import random
import sys
import urllib.request

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAMILIES = ["hidden_instruction", "unapproved_action", "invented_status"]


def fetch(round_no=None):
    tail = f"rounds/{round_no}" if round_no else "rounds/latest"
    with urllib.request.urlopen(f"https://api.drand.sh/v2/beacons/quicknet/{tail}", timeout=30) as r:
        return json.load(r)


def draw(pool, signature):
    rng = random.Random(int(hashlib.sha256(bytes.fromhex(signature)).hexdigest(), 16))
    picked = []
    for fam in FAMILIES:
        picked += rng.sample(sorted((t for t in pool if t["family"] == fam), key=lambda t: t["id"]), 4)
    picked += rng.sample(sorted((t for t in pool if t["family"] == "normal"), key=lambda t: t["id"]), 8)
    return picked


def main():
    round_no = int(sys.argv[1]) if len(sys.argv) > 1 else None
    beacon = fetch(round_no)
    pool = json.load(open(os.path.join(HERE, "data", "pool.json"), encoding="utf-8"))
    exam = draw(pool, beacon["signature"])
    with open(os.path.join(HERE, "data", "exam.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(exam, f, indent=1, ensure_ascii=False)
        f.write("\n")
    with open(os.path.join(HERE, "data", "exam_draw.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump({"beacon": "drand quicknet", "round": beacon["round"], "signature": beacon["signature"],
                   "pool_sha256": open(os.path.join(HERE, "data", "pool.sha256")).read().split()[0],
                   "ids": [t["id"] for t in exam]}, f, indent=1)
        f.write("\n")
    print(beacon["round"], len(exam))


if __name__ == "__main__":
    main()
