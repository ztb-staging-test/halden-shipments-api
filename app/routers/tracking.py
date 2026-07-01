from fastapi import APIRouter, Depends, HTTPException

from app import store
from app.auth import require_client
from app.models import ShipmentStatus, TrackingEvent
from app.notifications import notify_delivered

router = APIRouter(prefix="/tracking", tags=["tracking"])


def _record(event: TrackingEvent):
    if event.shipment_id not in store.shipments:
        raise HTTPException(404, "shipment not found")
    shipment = store.add_event(event)
    if event.status == ShipmentStatus.delivered:
        notify_delivered(store.customers[shipment.customer_id], shipment)
    return shipment


@router.get("/{shipment_id}", response_model=list[TrackingEvent])
def shipment_events(shipment_id: str, client: str = Depends(require_client)):
    return store.events.get(shipment_id, [])


@router.post("/events", status_code=202)
def post_event(event: TrackingEvent, client: str = Depends(require_client)):
    _record(event)
    return {"accepted": True}


@router.post("/carrier-webhook", status_code=202)
async def carrier_webhook(event: TrackingEvent):
    # Carriers can't send our API key header; TODO verify their HMAC signature.
    _record(event)
    return {"accepted": True}
