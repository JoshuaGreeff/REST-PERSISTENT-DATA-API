"""Define the Pydantic request schema used to validate clinical data."""

from pydantic import BaseModel, Field


class ClinicalDataCreate(BaseModel):
    """Describe the fields a client must provide when creating a record."""

    patient_name: str = Field(min_length=1, examples=["Jordan Lee"])
    age: int = Field(ge=0, le=120, examples=[42])
    diagnosis: str = Field(min_length=1, examples=["Hypertension"])

    # These validation rules keep the added clinical fields meaningful and non-empty.
    blood_type: str = Field(min_length=1, examples=["O+"])
    allergy_notes: str = Field(min_length=1, examples=["No known allergies"])
    attending_provider: str = Field(min_length=1, examples=["Dr. Patel"])
