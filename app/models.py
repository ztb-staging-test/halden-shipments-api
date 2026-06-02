from datetime import datetime
from enum import Enum

from pydantic import BaseModel, EmailStr, Field


class ShipmentStatus(str, Enum):
    booked = "booked"
    picked_up = "picked_up"
    in_transit = "in_transit"
    out_for_delivery = "out_for_delivery"
    delivered = "delivered"
    exception = "exception"


class CustomerIn(BaseModel):
    name: str
    email: EmailStr
    phone: str | None = None
    notify_on_delivery: bool = True


class Customer(CustomerIn):
    id: str
    created_at: datetime


class ShipmentIn(BaseModel):
    customer_id: str
    origin: str = Field(examples=["Rotterdam, NL"])
    destination: str = Field(examples=["Leipzig, DE"])
    weight_kg: float = Field(gt=0)
    carrier: str


class Shipment(ShipmentIn):
    id: str
    status: ShipmentStatus = ShipmentStatus.booked
    created_at: datetime
    updated_at: datetime


class TrackingEvent(BaseModel):
    shipment_id: str
    status: ShipmentStatus
    location: str
    occurred_at: datetime
    note: str | None = None
