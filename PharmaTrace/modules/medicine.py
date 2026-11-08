
from database.db import get_db


def register_medicine(data, chain):
    required = [
        "medicine_name",
        "batch_id",
        "manufacturer",
        "manufactured_on",
        "expires_on"
    ]

    if any(not data.get(field) for field in required):
        raise ValueError("Please complete all medicine fields.")

    if data["expires_on"] <= data["manufactured_on"]:
        raise ValueError(
            "Expiry date must be later than manufacturing date."
        )

    db = get_db()

    try:
        existing = db.execute(
            "SELECT 1 FROM medicines WHERE batch_id = %s",
            (data["batch_id"],)
        ).fetchone()

        if existing:
            raise ValueError("That batch ID is already registered.")

        transaction = {
            "type": "MEDICINE_REGISTERED",
            **data
        }

        result = chain.add_transaction(transaction)

        if not result["accepted"]:
            return result

        db.execute("""
            INSERT INTO medicines (
                batch_id,
                medicine_name,
                manufacturer,
                manufactured_on,
                expires_on,
                block_index,
                block_hash
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            data["batch_id"],
            data["medicine_name"],
            data["manufacturer"],
            data["manufactured_on"],
            data["expires_on"],
            result["block_index"],
            result["block_hash"]
        ))

        db.commit()
        return result

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


def list_medicines():
    db = get_db()

    try:
        return db.execute(
            "SELECT * FROM medicines ORDER BY created_at DESC"
        ).fetchall()

    finally:
        db.close()


def get_medicine(batch_id):
    db = get_db()

    try:
        row = db.execute(
            "SELECT * FROM medicines WHERE batch_id = %s",
            (batch_id,)
        ).fetchone()

        return dict(row) if row else None

    finally:
        db.close()
