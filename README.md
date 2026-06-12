# halden-shipments-api

Shipments, customers and tracking API behind the Halden Freight Analytics dashboard.
Partners (3PLs, carriers) and the dashboard call it with an API key; carriers push
status updates to the tracking endpoints.

> Demo repository. Halden Freight Analytics is a fictional company used to test
> ZeroTB's compliance engine. It contains deliberately planted issues. All credentials
> in it are fabricated and were never issued by any provider.

## Endpoints

| Method | Path | Purpose |
|---|---|---|
| GET/POST | `/customers` | List or create shippers |
| GET/DELETE | `/customers/{id}` | Read or remove a shipper |
| GET/POST | `/shipments` | List (filter by `status`) or book a shipment |
| GET | `/shipments/{id}` | Shipment detail |
| PATCH | `/shipments/{id}/cancel` | Cancel a booking |
| GET | `/tracking/{shipment_id}` | Tracking history |
| POST | `/tracking/events` | Partner status update |
| POST | `/tracking/carrier-webhook` | Carrier push (DHL, DB Schenker) |

Every request sends `X-API-Key`. Keys are set per client in `HALDEN_API_KEYS`
(`client:key,client:key`), injected from AWS Secrets Manager at deploy.

## Run locally

```sh
pip install -e '.[dev]'
HALDEN_API_KEYS=dashboard:local-dev uvicorn app.main:app --reload
pytest
```

## Layout

```
app/
  main.py            FastAPI app and router wiring
  auth.py            API-key dependency
  models.py          Pydantic models
  store.py           In-memory store (Postgres in prod)
  notifications.py   Delivery notices
  routers/           customers, shipments, tracking
scripts/             One-off ops scripts
tests/
```

## License

MIT. Written for this demo; structure follows the FastAPI "Bigger Applications"
tutorial (https://fastapi.tiangolo.com/tutorial/bigger-applications/, MIT).
