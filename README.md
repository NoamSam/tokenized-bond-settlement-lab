# Tokenized Bond Settlement Lab

Beginner-friendly SG-FORGE-oriented project.

This repository is a local simulation of a tokenized bond settlement flow:

1. An issuer creates a bond product.
2. An investor with a wallet address creates a purchase order.
3. A backend records the off-chain business state.
4. Later, smart contracts will settle fake EUR stablecoin against fake bond tokens.
5. The backend stores the blockchain transaction hash and settlement status.

## Backend

The backend is Django + Django REST Framework using mixins.

Current domain models:

```text
Investor
Bond
BondOrder
SettlementTransaction
```

```bash
source .venv/bin/activate
cd backend
python manage.py runserver
```

API:

```text
GET    /api/investors/
POST   /api/investors/
GET    /api/investors/<id>/
PATCH  /api/investors/<id>/

GET    /api/bonds/
POST   /api/bonds/
GET    /api/bonds/<id>/
PATCH  /api/bonds/<id>/

GET    /api/bond-orders/
POST   /api/bond-orders/
GET    /api/bond-orders/<id>/
PATCH  /api/bond-orders/<id>/

GET    /api/settlement-transactions/
POST   /api/settlement-transactions/
GET    /api/settlement-transactions/<id>/
PATCH  /api/settlement-transactions/<id>/
```

Swagger UI:

```text
GET /api/docs/
```

OpenAPI schema:

```text
GET /api/schema/
```
