"""Define the SQLAlchemy table used to persist clinical records."""

import datetime

from sqlalchemy import Column, DateTime, Integer, String

from database import Base


class ClinicalData(Base):
    """Map one clinical record to one row in the clinical_data table."""

    __tablename__ = "clinical_data"

    id = Column(Integer, primary_key=True, index=True)
    patient_name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    diagnosis = Column(String, nullable=False)

    # These three clinical fields are the assignment's required additions.
    blood_type = Column(String, nullable=False)
    allergy_notes = Column(String, nullable=False)
    attending_provider = Column(String, nullable=False)

    recorded_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    def to_dict(self):
        """Return the database row in a JSON-ready form for Flask responses."""
        return {
            "id": self.id,
            "patient_name": self.patient_name,
            "age": self.age,
            "diagnosis": self.diagnosis,
            "blood_type": self.blood_type,
            "allergy_notes": self.allergy_notes,
            "attending_provider": self.attending_provider,
            "recorded_at": self.recorded_at.isoformat(),
        }
