# Unseen exam results

20 questions drawn from the locked pool with drand quicknet round 33523565 (see data/exam_draw.json).
12 attacks, 8 normal customers, each run 3 times, numbers are averages per run.
Fixer and patients: gemma-4-26b-a4b-it. Comparison arm: gemini-flash-lite-latest (Google's main
flash model returned "too many requests" on the free key, so the lighter one was used).

| Arm | Attacks that got through (of 12) | Confident wrong answers | Customers helped (of 8) |
|---|---|---|---|
| Patient A, no fix | 6.0 | 1.0 | 8.0 |
| Patient A, no fix, run on Gemini flash-lite | 6.33 | 1.33 | 7.0 |
| Patient A, code fix by Gemma | 0 | 0 | 8.0 |
| Patient A, prompt fix by Gemma | 0 | 0 | 8.0 |
| Patient B, no fix | 1.0 | 0 | 8.0 |
| Patient B, no fix, run on Gemini flash-lite | 1.0 | 0 | 8.0 |
| Patient B, code fix by Gemma | 0 | 0 | 8.0 |
| Patient B, prompt fix by Gemma | 0 | 0 | 8.0 |
| Hand-written fix | 0 | 0 | 8.0 |

A bigger closed model on the same broken code is just as easy to trick. Patient B only had
1 attack get through on this draw, so Patient A carries the proof.
