# Scores on the practice set before the unseen exam

Attacks out of 12, normal customers out of 8, average of 3 repeats. Model: Gemma 4 26B.

| Arm | Attacks that got through | Confident wrong answers | Normal customers helped |
|---|---|---|---|
| Patient A, no fix | 5.0 | 0.0 | 7.33 |
| Patient A, prompt-only fix (Gemma) | 0.0 | 0.0 | 8.0 |
| Patient A, code fix (Gemma) | 0.0 | 0.0 | 8.0 |
| Patient B, no fix | 2.0 | 0.0 | 8.0 |
| Patient B, prompt-only fix (Gemma) | 0.0 | 0.0 | 8.0 |
| Patient B, code fix (Gemma) | 0.0 | 0.0 | 8.0 |
| Human reference fix (hand written) | 0.0 | 0.0 | 8.0 |

## Locked pool, no fix (36 attacks, 24 normal customers)

| Patient | Attacks that got through | Confident wrong | Normal customers helped |
|---|---|---|---|
| A | 18.0 | 3.0 | 23.0 |
| B | 6.0 | 0.0 | 24.0 |

Every repaired arm ties on the practice set. The unseen exam is what separates them.
