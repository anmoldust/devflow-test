"""Payment domain events published to the message bus.

Published events follow the contract in ``contracts/payment-completed.schema.json``.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Payment:
    payment_id: str
    order_ref: str
    amount_minor: int
    currency: str
    outcome: str  # "SUCCEEDED" | "FAILED"


def build_payment_completed_event(payment: Payment) -> dict:
    """Build the ``payment.completed`` event (schema version 2)."""
    return {
        "eventType": "payment.completed",
        "schemaVersion": 2,
        "paymentId": payment.payment_id,
        "orderRef": payment.order_ref,
        "amountMinor": payment.amount_minor,
        "currency": payment.currency,
        "status": payment.outcome,
    }
