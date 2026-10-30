# unseen-rite

A small shop chatbot gets tricked. A second open model rewrites the chatbot's code to fix it. The fix only counts if it passes an exam the fixer never saw, and real customers are still helped.

Work in progress. Built Oct 30 to 31, 2026 for the DEV Hacktoberfest "Ghost in the Machine" challenge. Everything in this repository was started inside the challenge window.

## What is in here

| Path | What it is |
|---|---|
| `agents/agent_a.py` | Patient A: a shop helper written the quick way (customer text pasted into the prompt, tool requests trusted) |
| `agents/agent_b.py` | Patient B: a helper that follows a written shop policy taken from tau-bench |
| `data/practice.json` | 20 questions the fixer may study |
| `data/pool.json` | 60 locked questions. The exam is drawn from here after the fix is frozen |
| `unseen_rite/checks.py` | Plain-code checks. No model grades a model |
| `unseen_rite/runner.py` | Runs one agent on one question set and writes the scores to `results/` |
| `tools/make_trials.py` | Builds the two question files |

## Where things stand

| Step | State |
|---|---|
| Both shop helpers, 20 practice questions, 60 locked pool questions, checks | Done |
| Pool fingerprint committed before any fix (`data/pool.sha256`) | Done |
| Open model repairs each helper two ways (rewrite code, or change only the prompt words), kept only if the accept rule passes | Done, see `results/exorcism_*.json` and `agents/fixed_*.py` |
| Hand-written reference fix (`agents/human_fix.py`) | Done |
| Scores on the practice set | `results/SUMMARY_section2.md` |
| Unseen exam drawn from the pool and run on every arm | Done, see `results/SUMMARY_exam.md` |

## Run it

```
set GEMINI_API_KEY=your key
python -m unseen_rite.runner --agent a --set practice --repeats 3
python -m pytest tests
```

## Credits

| Source | What we used | Licence |
|---|---|---|
| tau-bench, Sierra Research | The retail policy lines in `agents/agent_b.py` and `data/tau_retail_policy.md` | MIT |
| AgentDojo, ETH Zurich | The style of the "important message" hidden-instruction attack, used as inspiration for the wordings in `tools/make_trials.py`. Wordings are rewritten, not copied | MIT |
| Clerk demo (author's earlier project, Oct 2026) | The shape of three invented orders and the "unknown id falls back to the first order" habit | Own work |
| Suture and StressProof (author's earlier projects) | The idea of keeping a fix only if an outside check agrees. No code copied | Own work |

The three orders are invented. The questions were written for this project.

## What this is not

A toy shop with three invented orders, 80 questions in all. It is not a security product and does not prove a chatbot is safe.
