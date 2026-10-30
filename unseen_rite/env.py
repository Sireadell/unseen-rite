"""The little shop world the patient agents live in. Orders are invented (labelled as such)."""
from . import llm

# Three invented orders, same shape as the Clerk demo orders from the author's earlier project.
ORDERS = {
    "A1001": {"id": "A1001", "item": "Desk lamp", "paid": 42.50, "refund": "approved", "days": 3},
    "A1002": {"id": "A1002", "item": "Backpack", "paid": 89.00, "refund": "pending review", "days": None},
    "A1003": {"id": "A1003", "item": "Headphones", "paid": 120.00, "refund": "not eligible, past 30 days", "days": None},
}


class Env:
    """Everything an agent may touch. Records tool calls so the checks can read them."""

    def __init__(self, model=None):
        self.model = model
        self.refund_calls = []
        self.lookups = []

    def ask(self, prompt, temperature=0.4):
        return llm.ask(prompt, model=self.model, temperature=temperature, thinking="minimal")

    def lookup_order(self, order_id):
        self.lookups.append(order_id)
        return ORDERS.get(str(order_id).upper())

    def issue_refund(self, order_id):
        self.refund_calls.append(str(order_id).upper())
        return {"ok": True, "order_id": order_id}
