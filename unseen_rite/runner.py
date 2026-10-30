"""Runs one agent against one set of questions and scores it with the plain-code checks."""
import argparse
import importlib.util
import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor

from . import checks, llm
from .env import Env

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AGENT_FILES = {"a": "agents/agent_a.py", "b": "agents/agent_b.py"}


def load_agent(path):
    path = path if os.path.isabs(path) else os.path.join(HERE, path)
    spec = importlib.util.spec_from_file_location("agent_" + str(abs(hash(path))), path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_set(name):
    with open(os.path.join(HERE, "data", f"{name}.json"), encoding="utf-8") as f:
        return json.load(f)


def run_one(agent, trial, model=None):
    for attempt in range(4):
        env = Env(model=model)
        try:
            reply = agent.handle(trial["message"], env)
            error = None
        except Exception as err:  # a broken rewrite must score as a failure, not crash the run
            reply, error = "", f"{type(err).__name__}: {err}"
        if not (error and "model call failed" in error):
            break  # model host trouble is retried; the agent's own errors are scored
        time.sleep(20 * (attempt + 1))
    verdict = checks.evaluate(trial, reply, env.refund_calls)
    if error:
        verdict["helped"] = False if trial["family"] == "normal" else verdict["helped"]
        verdict["why"] = "agent crashed: " + error
    return {"id": trial["id"], "family": trial["family"], "message": trial["message"], "reply": reply,
            "refund_calls": env.refund_calls, **verdict, "error": error}


def summarise(rows, repeats):
    attacks = [r for r in rows if r["family"] != "normal"]
    normals = [r for r in rows if r["family"] == "normal"]
    return {
        "attack_trials": len(attacks) // repeats,
        "possessed": round(sum(r["possessed"] for r in attacks) / repeats, 2),
        "confident_wrong": round(sum(r["confident_wrong"] for r in attacks) / repeats, 2),
        "normal_trials": len(normals) // repeats,
        "helped": round(sum(bool(r["helped"]) for r in normals) / repeats, 2),
        "normal_possessed": round(sum(r["possessed"] for r in normals) / repeats, 2),
        "crashes": sum(1 for r in rows if r.get("error")),
    }


def run_set(agent, trials, repeats=3, model=None, workers=4):
    jobs = [t for _ in range(repeats) for t in trials]
    with ThreadPoolExecutor(max_workers=workers) as pool:
        rows = list(pool.map(lambda t: run_one(agent, t, model), jobs))
    return rows, summarise(rows, repeats)


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--agent", default="a", help="a, b, or a path to an agent file")
    parser.add_argument("--set", default="practice", choices=["practice", "pool", "exam"])
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--model", default=None)
    parser.add_argument("--out", default=None)
    args = parser.parse_args(argv)
    path = AGENT_FILES.get(args.agent, args.agent)
    started = time.time()
    rows, summary = run_set(load_agent(path), load_set(args.set), args.repeats, args.model)
    summary.update(agent=path, set=args.set, repeats=args.repeats, model=args.model or llm.GEMMA,
                   seconds=round(time.time() - started), model_calls=llm.USAGE["calls"])
    out = args.out or os.path.join(HERE, "results", f"{os.path.basename(path)}_{args.set}.json")
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        json.dump({"summary": summary, "rows": rows}, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print(json.dumps(summary))


if __name__ == "__main__":
    sys.exit(main())
