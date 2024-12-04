import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._create_table()

    def _create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fingerprint TEXT NOT NULL UNIQUE,
            created_at TEXT NOT NULL,
            status TEXT NOT NULL
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def get_alert(self, fingerprint):
        query = "SELECT * FROM alerts WHERE fingerprint = ?"
        cursor = self.conn.execute(query, (fingerprint,))
        row = cursor.fetchone()
        return {"fingerprint": row[1], "created_at": row[2], "status": row[3]} if row else None

    def add_alert(self, fingerprint, status):
        query = "INSERT INTO alerts (fingerprint, created_at, status) VALUES (?, ?, ?)"
        self.conn.execute(query, (fingerprint, datetime.now().isoformat(), status))
        self.conn.commit()

    def get_all_alerts(self):
        query = "SELECT * FROM alerts"
        cursor = self.conn.execute(query)
        return [
            {"id": row[0], "fingerprint": row[1], "created_at": row[2], "status": row[3]}
            for row in cursor.fetchall()
        ]