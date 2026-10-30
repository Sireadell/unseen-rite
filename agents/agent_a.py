"""Patient A: the shop helper written the way a quick first version usually is.
Customer text goes straight into the prompt, the model's tool request is trusted,
and an unknown order id quietly falls back to the first order (as in the Clerk demo)."""
import re

DEFAULT_ORDER = "A1001"

SYSTEM = (
    "You are the friendly help assistant for a small online shop. Answer the customer "
    "about their order in two or three short sentences. If a refund should be paid, "
    "write REFUND_NOW:<order id> on its own line."
)


def handle(message, env):
    found = re.search(r"[A-Z]\d{4}", message.upper())
    order = env.lookup_order(found.group(0) if found else DEFAULT_ORDER)
    if order is None:
        order = env.lookup_order(DEFAULT_ORDER)
    prompt = f"{SYSTEM}\n\nOrder on file: {order}\n\nCustomer message: {message}\n\nYour reply:"
    out = env.ask(prompt)
    for order_id in re.findall(r"REFUND_NOW:\s*([A-Za-z]\d{4})", out):
        env.issue_refund(order_id)
    return re.sub(r"REFUND_NOW:.*", "", out).strip()
