import logging

from fastapi import FastAPI

from app.routers import customers, shipments, tracking

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")

app = FastAPI(title="Halden Shipments API", version="0.4.0")
app.include_router(customers.router)
app.include_router(shipments.router)
app.include_router(tracking.router)


@app.get("/healthz")
def healthz():
    return {"ok": True}
