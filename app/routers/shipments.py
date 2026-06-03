from fastapi import APIRouter, Depends, HTTPException

from app import store
from app.auth import require_client
from app.models import Shipment, ShipmentIn, ShipmentStatus

router = APIRouter(prefix="/shipments", tags=["shipments"])


@router.get("", response_model=list[Shipment])
def list_shipments(status: ShipmentStatus | None = None, client: str = Depends(require_client)):
    rows = store.shipments.values()
    return [s for s in rows if status is None or s.status == status]


@router.post("", response_model=Shipment, status_code=201)
def book_shipment(body: ShipmentIn, client: str = Depends(require_client)):
    if body.customer_id not in store.customers:
        raise HTTPException(422, "unknown customer_id")
    return store.add_shipment(body)


@router.get("/{shipment_id}", response_model=Shipment)
def get_shipment(shipment_id: str, client: str = Depends(require_client)):
    if shipment_id not in store.shipments:
        raise HTTPException(404, "shipment not found")
    return store.shipments[shipment_id]


@router.patch("/{shipment_id}/cancel", response_model=Shipment)
def cancel_shipment(shipment_id: str, client: str = Depends(require_client)):
    s = store.shipments.get(shipment_id)
    if s is None:
        raise HTTPException(404, "shipment not found")
    s.status = ShipmentStatus.exception
    return s
