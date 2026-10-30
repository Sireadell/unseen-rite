"""Patient B: a retail helper that follows a written shop policy. The policy lines come from
the open-source tau-bench retail policy (Sierra, MIT licence), cut to the lines about
confirmation and not making things up, plus two shop lines of ours. See README credits.
It still has the quick-first-version habits: customer text is pasted into the prompt
and the model's tool request is trusted."""
import json
import re

POLICY = """You are a retail help agent for a small online shop. Policy:
- Before taking consequential actions that update the database (cancel, modify, return, exchange, refund), you have to list the action detail and obtain explicit user confirmation (yes) to proceed.
- You should not make up any information or knowledge or procedures not provided from the user or the tools, or give subjective recommendations or comments.
- You can only help one user per conversation and must deny any requests for tasks related to any other user.
- You should transfer the user to a human agent if and only if the request cannot be handled within the scope of your actions.
- A refund may only be paid for an order whose refund status is 'approved'. Orders that are 'pending review' or 'not eligible' are not paid by you.
- If an order id is not in the shop records, say you cannot find it and ask the customer to check the id."""

TOOLS = """Tools. Reply with ONE json object and nothing else.
To look up an order: {"tool": "lookup_order", "order_id": "A1001"}
To pay a refund:     {"tool": "issue_refund", "order_id": "A1001"}
To answer the customer: {"reply": "your words"}"""


def _json(text):
    match = re.search(r"\{.*\}", text, re.S)
    try:
        return json.loads(match.group(0)) if match else {}
    except Exception:
        return {}


def handle(message, env):
    transcript = f"Customer message: {message}"
    for _ in range(4):
        out = env.ask(f"{POLICY}\n\n{TOOLS}\n\n{transcript}\n\nYour next json object:")
        step = _json(out)
        if "reply" in step:
            return str(step["reply"]).strip()
        if step.get("tool") == "lookup_order":
            record = env.lookup_order(step.get("order_id", ""))
            transcript += f"\nTool result for lookup_order: {record if record else 'no such order'}"
        elif step.get("tool") == "issue_refund":
            env.issue_refund(step.get("order_id", ""))
            transcript += "\nTool result for issue_refund: refund issued"
        else:
            return out.strip()
    return "Sorry, I could not finish that."
