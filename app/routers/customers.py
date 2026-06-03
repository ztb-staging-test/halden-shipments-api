from fastapi import APIRouter, Depends, HTTPException

from app import store
from app.auth import require_client
from app.models import Customer, CustomerIn

router = APIRouter(prefix="/customers", tags=["customers"])


@router.get("", response_model=list[Customer])
def list_customers(client: str = Depends(require_client)):
    return list(store.customers.values())


@router.post("", response_model=Customer, status_code=201)
def create_customer(body: CustomerIn, client: str = Depends(require_client)):
    return store.add_customer(body)


@router.get("/{customer_id}", response_model=Customer)
def get_customer(customer_id: str, client: str = Depends(require_client)):
    if customer_id not in store.customers:
        raise HTTPException(404, "customer not found")
    return store.customers[customer_id]


@router.delete("/{customer_id}", status_code=204)
def delete_customer(customer_id: str, client: str = Depends(require_client)):
    store.customers.pop(customer_id, None)
