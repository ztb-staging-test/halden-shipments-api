"""In-memory store. Swapped for Postgres in prod via STORE_BACKEND (see README)."""

import uuid
from datetime import UTC, datetime

from app.models import Customer, CustomerIn, Shipment, ShipmentIn, TrackingEvent

customers: dict[str, Customer] = {}
shipments: dict[str, Shipment] = {}
events: dict[str, list[TrackingEvent]] = {}


def _id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


def add_customer(data: CustomerIn) -> Customer:
    c = Customer(**data.model_dump(), id=_id("cus"), created_at=datetime.now(UTC))
    customers[c.id] = c
    return c


def add_shipment(data: ShipmentIn) -> Shipment:
    now = datetime.now(UTC)
    s = Shipment(**data.model_dump(), id=_id("shp"), created_at=now, updated_at=now)
    shipments[s.id] = s
    events[s.id] = []
    return s


def add_event(event: TrackingEvent) -> Shipment:
    s = shipments[event.shipment_id]
    events[s.id].append(event)
    s.status, s.updated_at = event.status, event.occurred_at
    return s
