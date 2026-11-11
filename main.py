"""A Flask API that persists clinical records to SQLite and JSON Lines."""

import json
import os
from pathlib import Path

from flask import Flask, g, jsonify, request
from pydantic import ValidationError
from sqlalchemy.orm import Session

from database import Base, SessionLocal, engine
from models import ClinicalData
from schemas import ClinicalDataCreate


app = Flask(__name__)

# Creating tables at startup gives the local application a usable SQLite file on
# its first run, without requiring a separate database setup command.
Base.metadata.create_all(bind=engine)

# JSON Lines keeps one complete record on each line, so I can easily check that
# the same clinical data was also saved outside of the database.
DATA_FILE = Path(os.getenv("CLINICAL_JSONL_FILE", "data/clinical_data.jsonl"))
DATA_FILE.parent.mkdir(parents=True, exist_ok=True)


def append_to_file(record: dict):
    """Append one created clinical record to the JSONL persistence file."""
    with DATA_FILE.open("a", encoding="utf-8") as file:
        file.write(json.dumps(record) + "\n")


@app.before_request
def create_session():
    """Open one SQLAlchemy session for the current Flask request."""
    g.db = SessionLocal()


@app.teardown_appcontext
def close_session(exception=None):
    """Close the request session after Flask finishes the response."""
    db: Session | None = getattr(g, "db", None)
    if db is not None:
        db.close()


@app.route("/clinical/", methods=["POST"])
def create_record():
    """Validate and persist a clinical record in SQLite and JSONL."""
    try:
        # Pydantic checks the incoming JSON before either storage location changes.
        payload = request.get_json(silent=True)
        clinical_data = ClinicalDataCreate.model_validate(payload)
    except ValidationError as error:
        # A 400 response gives an API client usable validation feedback instead of a traceback.
        return jsonify({"detail": error.errors()}), 400

    db: Session = g.db
    db_record = ClinicalData(**clinical_data.model_dump())
    db.add(db_record)
    db.commit()
    db.refresh(db_record)

    # The JSONL record uses the database-generated ID and timestamp so both stores
    # describe the same created clinical event.
    file_record = db_record.to_dict()
    append_to_file(file_record)

    return jsonify(file_record), 201


@app.route("/clinical/", methods=["GET"])
def read_records():
    """Return every clinical record from the SQLite database as JSON."""
    db: Session = g.db
    records = db.query(ClinicalData).order_by(ClinicalData.id).all()
    return jsonify([record.to_dict() for record in records]), 200


if __name__ == "__main__":
    # The walkthrough uses port 8000 for this local clinical-records API.
    app.run(host="127.0.0.1", port=8000, debug=True)
