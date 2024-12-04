import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._create_table()

    def _create_table(self):
        # Обновляем таблицу, добавляем колонку mm_post_id, если её нет
        query_create = """
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fingerprint TEXT NOT NULL UNIQUE,
            created_at TEXT NOT NULL,
            status TEXT NOT NULL,
            mm_post_id TEXT
        )
        """
        self.conn.execute(query_create)
        self.conn.commit()

        # Проверяем, есть ли колонка mm_post_id, если нет — добавляем
        query_check_column = "PRAGMA table_info(alerts)"
        columns = [row[1] for row in self.conn.execute(query_check_column).fetchall()]
        if "mm_post_id" not in columns:
            self.conn.execute("ALTER TABLE alerts ADD COLUMN mm_post_id TEXT")
            self.conn.commit()

    def get_alert(self, fingerprint):
        query = "SELECT * FROM alerts WHERE fingerprint = ?"
        cursor = self.conn.execute(query, (fingerprint,))
        row = cursor.fetchone()
        return (
            {
                "fingerprint": row[1],
                "created_at": row[2],
                "status": row[3],
                "mm_post_id": row[4],
            }
            if row
            else None
        )

    def add_alert(self, fingerprint, status, mm_post_id=None):
        query = """
        INSERT INTO alerts (fingerprint, created_at, status, mm_post_id)
        VALUES (?, ?, ?, ?)
        """
        self.conn.execute(query, (fingerprint, datetime.now().isoformat(), status, mm_post_id))
        self.conn.commit()

    def get_all_alerts(self):
        query = "SELECT * FROM alerts"
        cursor = self.conn.execute(query)
        return [
            {
                "id": row[0],
                "fingerprint": row[1],
                "created_at": row[2],
                "status": row[3],
                "mm_post_id": row[4],
            }
            for row in cursor.fetchall()
        ]