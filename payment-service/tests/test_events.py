import json
from pathlib import Path

from payment_service.events import Payment, build_payment_completed_event

ROOT = Path(__file__).resolve().parent.parent


def test_event_matches_published_contract():
    schema = json.loads((ROOT / "contracts" / "payment-completed.schema.json").read_text())
    event = build_payment_completed_event(Payment("pay-1", "ord-1", 100, "USD", "SUCCEEDED"))
    assert set(schema["required"]) <= set(event)
    assert event["status"] in schema["properties"]["status"]["enum"]
