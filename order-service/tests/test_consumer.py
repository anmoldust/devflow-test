from order_service.consumer import handle_payment_event
from order_service.store import Order, OrderStore


def _store_with(order_id: str) -> OrderStore:
    store = OrderStore()
    store.save(Order(order_id, 4999))
    return store


def test_ignores_other_event_types():
    store = _store_with("o1")
    assert handle_payment_event({"eventType": "refund.issued"}, store) is False


def test_marks_order_paid_for_completed_event():
    store = _store_with("o1")
    event = {"eventType": "payment.completed", "orderId": "o1", "status": "COMPLETED"}
    assert handle_payment_event(event, store) is True
    assert store.get("o1").status == "PAID"


def test_marks_order_failed():
    store = _store_with("o2")
    event = {"eventType": "payment.completed", "orderId": "o2", "status": "FAILED"}
    assert handle_payment_event(event, store) is True
    assert store.get("o2").status == "PAYMENT_FAILED"
