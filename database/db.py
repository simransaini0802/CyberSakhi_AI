import sqlite3
from flask import current_app
from datetime import datetime, timezone

def _connect():
    conn = sqlite3.connect(current_app.config["DATABASE_PATH"])
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with _connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS scans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message TEXT NOT NULL,
                prediction TEXT NOT NULL,
                risk TEXT NOT NULL,
                score INTEGER NOT NULL,
                created_at TEXT NOT NULL
            )
        """)

def save_scan(message: str, result: dict):
    with _connect() as conn:
        conn.execute(
            "INSERT INTO scans (message, prediction, risk, score, created_at) VALUES (?, ?, ?, ?, ?)",
            (message, result["prediction"], result["risk"], result["score"],
             datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M:%S"))
        )

def get_recent_scans(limit=10):
    with _connect() as conn:
        rows = conn.execute(
            "SELECT id, message, prediction, risk, score, created_at FROM scans ORDER BY id DESC LIMIT ?",
            (limit,)
        ).fetchall()
        return [dict(row) for row in rows]

def get_stats():
    with _connect() as conn:
        total = conn.execute("SELECT COUNT(*) FROM scans").fetchone()[0]
        high = conn.execute("SELECT COUNT(*) FROM scans WHERE risk = 'High'").fetchone()[0]
        medium = conn.execute("SELECT COUNT(*) FROM scans WHERE risk = 'Medium'").fetchone()[0]
        low = conn.execute("SELECT COUNT(*) FROM scans WHERE risk = 'Low indicator count'").fetchone()[0]
    return {"total": total, "high": high, "medium": medium, "low": low}
