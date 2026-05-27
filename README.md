# Tokenized Bond Settlement Lab

Beginner-friendly SG-FORGE-oriented project.

This repository will become a local simulation of a tokenized bond settlement flow:

1. An investor creates a bond purchase order.
2. A backend records the off-chain business state.
3. Later, smart contracts will settle fake EUR stablecoin against fake bond tokens.

## Backend

The first backend is Django + Django REST Framework using mixins.

```bash
source .venv/bin/activate
cd backend
python manage.py runserver
```

API:

```text
GET    /api/bond-orders/
POST   /api/bond-orders/
GET    /api/bond-orders/<id>/
PATCH  /api/bond-orders/<id>/
DELETE /api/bond-orders/<id>/
```
