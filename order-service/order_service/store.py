from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Order:
    order_id: str
    total_minor: int
    status: str = "PENDING"


class OrderStore:
    """In-memory order store (fixture)."""

    def __init__(self) -> None:
        self._orders: dict[str, Order] = {}

    def save(self, order: Order) -> None:
        self._orders[order.order_id] = order

    def get(self, order_id: str) -> Order | None:
        return self._orders.get(order_id)
