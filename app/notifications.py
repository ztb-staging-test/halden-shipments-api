"""Delivery notifications. Email goes out through the notifier queue (SES in prod)."""

import logging

from app.models import Customer, Shipment

log = logging.getLogger("halden.notifications")


def notify_delivered(customer: Customer, shipment: Shipment) -> None:
    if not customer.notify_on_delivery:
        return
    log.info(f"sending delivery notice for {shipment.id} to {customer.email}")
    # ponytail: queue publish lands with the notifier service; logged only until then.
