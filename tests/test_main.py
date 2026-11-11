"""Test clinical-record creation, validation, and both persistence outputs."""

import json
import os
import tempfile
import unittest
from pathlib import Path


# Set test-specific paths before importing the application modules so tests do not
# change the assignment's local clinical_data.db or data/clinical_data.jsonl files.
TEST_DIRECTORY = tempfile.TemporaryDirectory()
TEST_PATH = Path(TEST_DIRECTORY.name)
os.environ["CLINICAL_DATABASE_URL"] = f"sqlite:///{(TEST_PATH / 'test_clinical.db').as_posix()}"
os.environ["CLINICAL_JSONL_FILE"] = str(TEST_PATH / "clinical_data.jsonl")

from database import Base, engine  # noqa: E402
from main import DATA_FILE, app  # noqa: E402


class ClinicalApiTests(unittest.TestCase):
    """Use a clean temporary database and JSONL file for each test."""

    def setUp(self):
        app.config["TESTING"] = True
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        DATA_FILE.unlink(missing_ok=True)
        self.client = app.test_client()

    def test_post_creates_record_in_sqlite_and_jsonl(self):
        """A valid POST writes the added fields to both required storage formats."""
        payload = {
            "patient_name": "Jordan Lee",
            "age": 42,
            "diagnosis": "Hypertension",
            "blood_type": "O+",
            "allergy_notes": "No known allergies",
            "attending_provider": "Dr. Patel",
        }

        create_response = self.client.post("/clinical/", json=payload)
        list_response = self.client.get("/clinical/")

        self.assertEqual(create_response.status_code, 201)
        self.assertEqual(list_response.status_code, 200)
        self.assertEqual(list_response.get_json()[0]["attending_provider"], "Dr. Patel")

        jsonl_record = json.loads(DATA_FILE.read_text(encoding="utf-8").strip())
        self.assertEqual(jsonl_record["blood_type"], "O+")
        self.assertEqual(jsonl_record["id"], create_response.get_json()["id"])

    def test_post_rejects_invalid_clinical_data(self):
        """An invalid age receives the required client-error response before storage."""
        response = self.client.post(
            "/clinical/",
            json={
                "patient_name": "Jordan Lee",
                "age": 130,
                "diagnosis": "Hypertension",
                "blood_type": "O+",
                "allergy_notes": "No known allergies",
                "attending_provider": "Dr. Patel",
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("detail", response.get_json())


def tearDownModule():
    """Release the temporary persistence files after the test module finishes."""
    engine.dispose()
    TEST_DIRECTORY.cleanup()


if __name__ == "__main__":
    unittest.main()
