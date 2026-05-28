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
SettlementMessage
```

The `settlements` app is split by domain:

```text
settlements/models/investors.py
settlements/models/bonds.py
settlements/models/bond_orders.py
settlements/models/settlement_transactions.py
settlements/models/settlement_messages.py

settlements/views/investors.py
settlements/views/bonds.py
settlements/views/bond_orders.py
settlements/views/settlement_transactions.py
settlements/views/settlement_messages.py

settlements/serializers/investors.py
settlements/serializers/bonds.py
settlements/serializers/bond_orders.py
settlements/serializers/settlement_transactions.py
settlements/serializers/settlement_messages.py
```

```bash
source .venv/bin/activate
cd backend
python manage.py runserver
```

Create demo data for Swagger:

```bash
python manage.py seed_demo_data
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

GET    /api/settlement-messages/
POST   /api/settlement-messages/
GET    /api/settlement-messages/<id>/
```

`SettlementMessage` generates an ISO 20022-style `camt.054` XML payload from a
settlement transaction. This is intentionally simplified for learning; it shows
how blockchain settlement data can be transformed into a traditional finance
message shape.

Swagger UI:

```text
GET /api/docs/
```

OpenAPI schema:

```text
GET /api/schema/
```
