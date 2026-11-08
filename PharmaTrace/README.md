# PharmaTrace

**Blockchain-Powered Pharmaceutical Supply Chain & Fake Medicine Detection — educational prototype**

PharmaTrace is a local-first web application starter for recording medicine batches in a tamper-evident hash-linked ledger. It includes a four-validator, 3-of-4 consensus simulation, a SQLite medicine registry, a dashboard, and a basic integrity check.

> **Important scope note:** This is an educational prototype. The validator component is a deterministic simulation running in one process, not a production distributed consensus protocol. A registered record does not prove the physical medicine is genuine. Real deployment requires authenticated manufacturers, secure signing keys, independent validator nodes, protected QR labels, and regulatory integration.

## Current working module (Milestone 1)
- Manufacturer medicine-batch registration form
- Required-field and date validation
- Duplicate batch-ID prevention
- Four named validators with a 3-of-4 approval threshold
- SHA-256 hash-linked blocks
- SQLite persistence for registered batches
- Dashboard and medicine record detail page
- Chain integrity API and tests

## Requirements
- Python 3.10 or newer
- VS Code (recommended)
- Git (for GitHub publishing)

## Windows installation
```powershell
# 1. Extract the ZIP and open the PharmaTrace folder in VS Code
# 2. Create a virtual environment
py -m venv .venv

# 3. Activate it
.venv\Scripts\activate

# If PowerShell blocks activation, use:
# Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
# .venv\Scripts\Activate.ps1

# 4. Install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

# 5. Start the application
python app.py
```
Open **http://127.0.0.1:5000** in your browser.

## First demonstration
1. Open the dashboard.
2. Click **Register a medicine**.
3. Enter a sample such as:
   - Medicine: Paracetamol 500 mg
   - Batch ID: PARA-2026-001
   - Manufacturer: ABC Pharmaceuticals (demo data)
   - Manufacturing date: 2026-01-01
   - Expiry date: 2027-01-01
4. Submit. The starter's four simulated validators approve the registration, and the transaction is committed as a new block.
5. Open the batch record and inspect its block hash.
6. Register the same batch ID again; duplicate registration should be rejected.

## Consensus API demonstration
The API accepts exactly four boolean votes:
```powershell
# 3 approvals -> accepted
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:5000/api/consensus/demo `
  -ContentType "application/json" -Body '{"votes":[true,true,true,false]}'

# 2 approvals -> rejected
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:5000/api/consensus/demo `
  -ContentType "application/json" -Body '{"votes":[true,true,false,false]}'
```
This endpoint demonstrates the decision rule; it does not commit a medicine transaction.

## API endpoints
- `GET /health` — health check
- `GET /api/chain` — current in-memory chain and integrity status
- `POST /api/consensus/demo` — evaluate four validator votes
- `GET /medicine/<batch_id>` — view registered batch record

## Run tests
```powershell
pytest -q
```

## GitHub publishing
Create an empty repository named `PharmaTrace` on GitHub. Then, from this project folder:
```powershell
git init
git add .
git commit -m "Initial PharmaTrace starter: registration and 4-validator consensus"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/PharmaTrace.git
git push -u origin main
```
Replace `YOUR-USERNAME` with your GitHub username. Never commit passwords, API keys, `.env` files, or real patient/medicine-sensitive data.

## Planned next milestones
1. Persist and reload the blockchain safely (currently chain blocks are in memory).
2. Add explicit validator voting controls and audit records.
3. Add distributor and pharmacy transfer events with role-based access.
4. Add QR generation and a public batch verification page.
5. Add tamper-evidence and test fixtures in the explorer.
6. Add authentication, signed transactions, deployment configuration, and production security review.
7. Deploy to a hosted service and configure HTTPS.

## Architecture
Browser UI → Flask routes → application modules → SQLite registry + blockchain engine → 4-validator consensus simulation → SHA-256 linked blocks.
