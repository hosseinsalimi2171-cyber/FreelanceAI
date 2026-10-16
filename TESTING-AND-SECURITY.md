# FreelanceAI — Stage 2: tests and file-access safety

## What changed
- Added Django tests for registration/login, private request ownership, dashboard order isolation, published-project ordering, and POST-only logout.
- Added `requirements.txt` for the dependencies used by this starter project.
- Removed direct customer-facing links to uploaded preview/final files from the dashboard. Django's default media URL is not a protected download mechanism; files must not be linked publicly until an authenticated, ownership-checked download view/storage policy is implemented.

## Run locally (PowerShell)
From the project directory, with your `.venv` activated or use its Python executable:

```powershell
& ".\.venv\Scripts\python.exe" -m pip install -r requirements.txt
& ".\.venv\Scripts\python.exe" manage.py check
& ".\.venv\Scripts\python.exe" manage.py makemigrations --check --dry-run
& ".\.venv\Scripts\python.exe" manage.py migrate
& ".\.venv\Scripts\python.exe" manage.py test portfolio
```

The source bundle intentionally excludes `.env` and `db.sqlite3`. Keep your original `.env` locally and never commit it. Do not deploy until tests pass in your actual environment.

## Security boundary
Payment verification, authenticated file delivery, email verification, production HTTPS/cookie settings, rate limiting, and live AI/news integrations are not implemented by this stage. Do not claim crypto payment is confirmed or provide final project files until on-chain payment validation and owner authorization are implemented and tested.
