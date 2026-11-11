# REST Persistent Data API

A small Flask clinical-records API that saves every created record to both SQLite and a JSON Lines file.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Run

```powershell
python main.py
```

The service runs at `http://127.0.0.1:8000`.

## Create and view a clinical record

Run these commands in a second PowerShell window while the server is running:

```powershell
curl.exe -X POST http://127.0.0.1:8000/clinical/ -H "Content-Type: application/json" -d '{"patient_name":"Jordan Lee","age":42,"diagnosis":"Hypertension","blood_type":"O+","allergy_notes":"No known allergies","attending_provider":"Dr. Patel"}'

curl.exe http://127.0.0.1:8000/clinical/
```

The POST returns `201 Created`. It creates `clinical_data.db` and appends one line to `data/clinical_data.jsonl`.

## Inspect persistence

```powershell
python -c "import sqlite3; print(sqlite3.connect('clinical_data.db').execute('SELECT * FROM clinical_data').fetchall())"
Get-Content data/clinical_data.jsonl
```

## Test

```powershell
python -m unittest discover -s tests -v
```

The two tests verify successful dual persistence and the validation error response.
