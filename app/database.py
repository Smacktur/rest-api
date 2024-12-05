import sqlite3
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class Database:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._create_table()

    def _create_table(self):
    # Лог создания таблицы
        logger.info("Checking if the table 'alerts' exists.")
        query_create = """
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fingerprint TEXT NOT NULL UNIQUE,
            created_at TEXT NOT NULL,
            status TEXT NOT NULL
        )
        """
        self.conn.execute(query_create)
        self.conn.commit()
        logger.info("Table 'alerts' checked or created.")

        # Проверяем наличие колонки mm_post_id
        query_check_column = "PRAGMA table_info(alerts)"
        columns = [row[1] for row in self.conn.execute(query_check_column).fetchall()]
        logger.info(f"Current columns in 'alerts': {columns}")

        if "mm_post_id" not in columns:
            logger.info("Column 'mm_post_id' is missing. Adding it now.")
            try:
                self.conn.execute("ALTER TABLE alerts ADD COLUMN mm_post_id TEXT")
                self.conn.commit()
                logger.info("Column 'mm_post_id' added successfully.")
            except Exception as e:
                logger.error(f"Failed to add column 'mm_post_id': {e}")
        else:
            logger.info("Column 'mm_post_id' already exists.")

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