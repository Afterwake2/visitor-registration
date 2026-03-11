import os
from datetime import datetime
from flask import Flask, request, jsonify, render_template
import psycopg2
from psycopg2.pool import SimpleConnectionPool

app = Flask(__name__)

# -------------------------------------------------------------------
# Database setup
# -------------------------------------------------------------------
DATABASE_URL = os.getenv("DATABASE_URL", "").strip()

if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is not set. On DigitalOcean App Platform, add it "
        "under Settings > Environment Variables."
    )

def ensure_sslmode_require(dsn: str) -> str:
    """
    Ensure sslmode=require is present (DigitalOcean Managed PG typically needs it).
    If you already have sslmode in the URL, this is a no-op.
    """
    lower = dsn.lower()
    if "sslmode=" in lower:
        return dsn
    # Append correctly whether or not a query string exists
    return dsn + ("&sslmode=require" if "?" in dsn else "?sslmode=require")

DSN = ensure_sslmode_require(DATABASE_URL)

pool = SimpleConnectionPool(minconn=1, maxconn=10, dsn=DSN)

def init_db():
    conn = pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS visitors (
                    id SERIAL PRIMARY KEY,
                    first_name VARCHAR(100) NOT NULL,
                    last_name VARCHAR(100) NOT NULL,
                    contact_number VARCHAR(50) NOT NULL,
                    company_name VARCHAR(150),
                    purpose TEXT NOT NULL,
                    contact_person VARCHAR(100) NOT NULL,
                    created_at TIMESTAMP DEFAULT NOW()
                );
            """)
            conn.commit()
    finally:
        pool.putconn(conn)

# Initialize table on startup
with app.app_context():
    init_db()

# -------------------------------------------------------------------
# Routes
# -------------------------------------------------------------------
@app.get("/")
def index():
    return render_template("index.html")

@app.post("/register")
def register():
    """
    Accepts JSON or form-encoded payload:
    {
      firstName, lastName, contactNumber, companyName?, purpose, contactPerson
    }
    """
    payload = request.get_json(silent=True) or request.form

    first_name     = (payload.get("firstName") or "").strip()
    last_name      = (payload.get("lastName") or "").strip()
    contact_number = (payload.get("contactNumber") or "").strip()
    company_name   = (payload.get("companyName") or "").strip()
    purpose        = (payload.get("purpose") or "").strip()
    contact_person = (payload.get("contactPerson") or "").strip()

    missing = [k for k, v in {
        "firstName": first_name,
        "lastName": last_name,
        "contactNumber": contact_number,
        "purpose": purpose,
        "contactPerson": contact_person
    }.items() if not v]

    if missing:
        return jsonify({"success": False, "error": f"Missing required fields: {', '.join(missing)}"}), 400

    conn = pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO visitors
                    (first_name, last_name, contact_number, company_name, purpose, contact_person)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id, created_at;
            """, (first_name, last_name, contact_number, company_name, purpose, contact_person))
            row = cur.fetchone()
            conn.commit()

        return jsonify({
            "success": True,
            "data": {
                "id": row[0],
                "createdAt": row[1].isoformat() if isinstance(row[1], datetime) else None
            }
        })
    except Exception as e:
        app.logger.exception("Database insert failed")
        return jsonify({"success": False, "error": "Database insert failed"}), 500
    finally:
        pool.putconn(conn)

@app.get("/health")
def health():
    return jsonify({"status": "ok"})
