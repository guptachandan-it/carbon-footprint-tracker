"""SQLite storage functions for assessments."""
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "carbon_footprint.db"

def connection():
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys = ON")
    return db

def init_db():
    with connection() as db:
        db.executescript("""
        CREATE TABLE IF NOT EXISTS assessments (
          id INTEGER PRIMARY KEY AUTOINCREMENT, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
          electricity_kwh REAL NOT NULL, electricity_emission REAL NOT NULL,
          transport_emission REAL NOT NULL, waste_kg REAL NOT NULL,
          waste_emission REAL NOT NULL, total_emission REAL NOT NULL);
        CREATE TABLE IF NOT EXISTS transport_entries (
          id INTEGER PRIMARY KEY AUTOINCREMENT, assessment_id INTEGER NOT NULL,
          transport_type TEXT NOT NULL, distance_km REAL NOT NULL, emission REAL NOT NULL,
          FOREIGN KEY (assessment_id) REFERENCES assessments(id) ON DELETE CASCADE);
        """)

def save_assessment(payload, results):
    with connection() as db:
        cursor = db.execute("""INSERT INTO assessments (electricity_kwh,electricity_emission,transport_emission,waste_kg,waste_emission,total_emission)
          VALUES (?,?,?,?,?,?)""", (payload["electricity_kwh"], results["electricity_emission"], results["transport_emission"], payload["waste_kg"], results["waste_emission"], results["total_emission"]))
        assessment_id = cursor.lastrowid
        db.executemany("INSERT INTO transport_entries (assessment_id,transport_type,distance_km,emission) VALUES (?,?,?,?)",
          [(assessment_id, item["transport_type"], item["distance_km"], item["emission"]) for item in results["transport_entries"]])
        return assessment_id

def list_assessments(order="date"):
    clause = "total_emission DESC" if order == "total" else "created_at DESC"
    with connection() as db:
        return [dict(row) for row in db.execute(f"SELECT * FROM assessments ORDER BY {clause}")]

def get_assessment(assessment_id):
    with connection() as db:
        assessment = db.execute("SELECT * FROM assessments WHERE id=?", (assessment_id,)).fetchone()
        if not assessment: return None
        data = dict(assessment)
        data["transport_entries"] = [dict(row) for row in db.execute("SELECT * FROM transport_entries WHERE assessment_id=?", (assessment_id,))]
        return data

def delete_assessment(assessment_id):
    with connection() as db:
        return db.execute("DELETE FROM assessments WHERE id=?", (assessment_id,)).rowcount > 0
