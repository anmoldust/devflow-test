"""Consumes ``payment.completed`` events and updates order state."""
from __future__ import annotations

import logging

from .store import OrderStore

log = logging.getLogger("order-service")


def handle_payment_event(event: dict, store: OrderStore) -> bool:
    """Apply a payment event to the matching order. Returns True when handled."""
    if event.get("eventType") != "payment.completed":
        return False

    order_id = event.get("orderId")
    if order_id is None:
        log.warning("payment.completed event ignored: missing orderId")
        return False

    order = store.get(order_id)
    if order is None:
        log.warning("payment.completed for unknown order %s", order_id)
        return False

    status = event.get("status")
    if status == "COMPLETED":
        order.status = "PAID"
    elif status == "FAILED":
        order.status = "PAYMENT_FAILED"
    else:
        return False
    store.save(order)
    return True
