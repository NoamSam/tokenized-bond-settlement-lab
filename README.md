# Tokenized Bond Settlement Lab

[![CI](https://github.com/NoamSam/Crypto/actions/workflows/ci.yml/badge.svg)](https://github.com/NoamSam/Crypto/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.12-blue)
![Django](https://img.shields.io/badge/Django-6.0-092E20?logo=django)
![DRF](https://img.shields.io/badge/DRF-3.17-red)
![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-261230)

A backend simulating the **settlement of a tokenized bond against a stablecoin**, bridging on-chain settlement data with traditional post-trade infrastructure (ISO 20022-style reporting).

The core idea: when a bond trade settles on a blockchain, back-office, compliance and audit systems still need the transaction in a format they understand. This project models that full flow.

```
Investor onboarding (KYC) ──► Bond issuance ──► Purchase order
                                                      │
                                                      ▼
                              On-chain atomic DvP (Solidity, Hardhat)
                                                      │
                                                      ▼
                              ISO 20022-style camt.054 settlement message
```

> ⚠️ This is a learning/portfolio project: settlement is simulated locally and the camt.054 payload is a simplified educational rendition of the standard, not a certified implementation.

## Domain model

| Model | Role |
|---|---|
| `Investor` | Wallet address + KYC status (pending / verified / rejected) |
| `Bond` | ISIN, issuer, face value, coupon, maturity, total supply |
| `BondOrder` | Purchase order with full status lifecycle (pending → settlement_submitted → settled / failed / cancelled) |
| `SettlementTransaction` | On-chain trace: chain, transaction hash, block number, gas used |
| `SettlementMessage` | Generated camt.054-style XML notification, persisted for audit |

## API

Full CRUD on every resource, documented with Swagger / OpenAPI 3.

```
/api/investors/                  /api/investors/<id>/
/api/bonds/                      /api/bonds/<id>/
/api/bond-orders/                /api/bond-orders/<id>/
/api/settlement-transactions/    /api/settlement-transactions/<id>/
/api/settlement-messages/        /api/settlement-messages/<id>/

/api/docs/      Swagger UI
/api/schema/    OpenAPI schema
```

Creating a `SettlementMessage` from a confirmed `SettlementTransaction` generates and stores the XML payload:

```xml
<Document>
  <BkToCstmrDbtCdtNtfctn>
    <GrpHdr>
      <MsgId>CAMT054-TX-1</MsgId>
      ...
    </GrpHdr>
    <Ntfctn>
      <Ntry>
        <Amt Ccy="EUR">2000.00</Amt>
        <CdtDbtInd>DBIT</CdtDbtInd>
        <AddtlNtryInf>Tokenized bond settlement for 2 BOND2027 against FAKEUR on local_ethereum</AddtlNtryInf>
        <NtryDtls>
          <TxDtls>
            <Refs>
              <AcctSvcrRef>0xaaaa…aaaa</AcctSvcrRef>
              <EndToEndId>ORDER-1</EndToEndId>
            </Refs>
            ...
```

## Tech stack & engineering practices

- **Python 3.12, Django 6, Django REST Framework** (generic views + explicit mixins)
- **drf-spectacular** for OpenAPI 3 schema and Swagger UI
- **Domain-driven layout**: `models/`, `views/`, `serializers/` split per business entity
- **Optimized queries**: `select_related` on all FK-heavy endpoints
- **7 API integration tests** covering the full workflow (order → settlement → camt.054 generation) plus schema/docs availability
- **Ruff** linting (pycodestyle, pyflakes, isort) enforced in CI
- **Seed command** (`seed_demo_data`) for instant demo data

## Quickstart

```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

cd backend
python manage.py migrate
python manage.py seed_demo_data
python manage.py runserver
```

Then open http://127.0.0.1:8000/api/docs/

Run the test suite:

```bash
python manage.py test
```

## On-chain DvP settlement (`chain/`)

Solidity contracts (Hardhat + OpenZeppelin) implementing atomic Delivery-versus-Payment:

| Contract | Role |
|---|---|
| `BondToken` | ERC-20 bond units (0 decimals), full supply minted to the issuer |
| `FakeEuroStablecoin` | ERC-20 demo cash leg, 2 decimals (euro cents), open faucet |
| `DvPSettlement` | Atomic swap of both legs in one transaction; reverts entirely if either leg fails (BIS model 1: no principal risk). Tracks settled off-chain order ids and emits `SettlementExecuted` |

```bash
cd chain
npm ci
npx hardhat test          # 9 tests: happy path, atomicity, access control, replay protection
npx hardhat run scripts/settle-demo.js
```

The demo script prints a JSON settlement receipt that feeds straight into the backend:

```bash
cd backend
python manage.py record_onchain_settlement \
    --order-id 1 \
    --tx-hash 0xf248...17c1 \
    --block-number 7 --gas-used 111910
```

This confirms the `SettlementTransaction`, flips the `BondOrder` to `settled`, and generates the camt.054 message, closing the loop between on-chain settlement and traditional post-trade reporting.

## Roadmap

- [x] Solidity contracts for atomic DvP (bond token vs stablecoin) on a local Hardhat network
- [x] Backend command recording on-chain settlements (tx hash, block) against the order book
- [ ] React dashboard for the order/settlement lifecycle
- [ ] PostgreSQL + dockerized environment

## License

MIT
