# Insurance Claim Management System (ICMS)

A production-ready full-stack Flask web application for managing insurance policies and claims.

## Features

- **Role-based users**: Admin and Customer
- **Authentication**: Registration/Login/Logout with hashed passwords (Werkzeug)
- **Policy management**: CRUD operations for insurance policies
- **Claim management**:
  - Claim submission
  - Document upload (PNG/JPG/PDF)
  - Status tracking (Pending/Approved/Rejected)
- **Dashboards**:
  - Admin analytics (total, approved, pending claims)
  - Customer dashboard (policies, claims, notifications)
- **Notifications**: In-app notifications for claim status updates
- **Validation and security**:
  - Positive amount checks
  - Date parsing/validation
  - Role-based access control
  - Secure uploads via `secure_filename`
  - Max upload size limit
- **REST API endpoints** (session-auth protected)
- **Extra features**:
  - Search and pagination on claim list
  - Simple approval probability and fraud risk scoring heuristic

## Tech Stack

- Backend: Flask + SQLAlchemy ORM
- Frontend: HTML/CSS/JS + Bootstrap 5
- Database: SQLite by default, PostgreSQL supported via `DATABASE_URL`
- Deployment: Gunicorn-compatible for Render/Heroku-style platforms

## Project Structure

```text
app/
  models/
  routes/
  templates/
  static/
  uploads/
config.py
run.py
requirements.txt
README.md
```

## Installation

1. Clone and enter repository:
   ```bash
   git clone <repo-url>
   cd DesktopAppComputerSystemArchByGagan
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # macOS/Linux
   # .venv\Scripts\activate   # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set environment variables (optional but recommended):
   ```bash
   export FLASK_ENV=development
   export SECRET_KEY='replace-with-strong-secret'
   # SQLite default (no need to set DATABASE_URL)
   # For PostgreSQL:
   # export DATABASE_URL='postgresql+psycopg2://user:password@host:5432/dbname'
   ```

5. Initialize DB:
   ```bash
   flask --app run.py shell
   # In shell:
   # >>> from app.extensions import db
   # >>> db.create_all()
   # >>> exit()
   ```

6. Run app:
   ```bash
   flask --app run.py run
   ```

First registered user is auto-promoted to **admin**. Later registrations become **customers**.

## REST API Documentation

All endpoints are under `/api` and require a valid logged-in session.

- `GET /api/claims`
  - Admin: all claims
  - Customer: own claims
  - Includes approval probability and fraud risk score

- `GET /api/policies`
  - Admin: all policies
  - Customer: own policies

- `GET /api/users`
  - Admin-only user list

### Example response (`/api/claims`)

```json
[
  {
    "claim_id": "CLM-ABC12345",
    "policy_id": 1,
    "customer_id": 2,
    "amount": 1250.5,
    "status": "Pending",
    "approval_probability": 0.75,
    "fraud_risk_score": 0.2
  }
]
```

## Deployment Notes (Render/Heroku)

- Use `gunicorn run:app` as start command.
- Set environment variables:
  - `SECRET_KEY`
  - `FLASK_ENV=production`
  - `DATABASE_URL` (for PostgreSQL)
- Ensure uploads directory is writable. For ephemeral file systems, move documents to cloud storage (S3/GCS) in production.

## Security Notes

- Passwords are hashed (Werkzeug).
- Role-based route protection is enforced.
- File upload extensions are restricted and filenames sanitized.
- Set a strong production `SECRET_KEY`.

## Future Improvements

- JWT auth for external/mobile clients
- Real-time websocket notifications
- Robust ML fraud model (scikit-learn pipeline)
- Audit logs and multi-factor authentication
