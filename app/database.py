import sqlite3
import logging
from datetime import datetime

# Настройка логгера
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class Database:
    def __init__(self, db_path):
        logger.info("Initializing Database")
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._create_table()

    def _create_table(self):
        logger.info("Checking if the table 'alerts' exists.")
        query_create = """
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fingerprint TEXT NOT NULL UNIQUE,
            alertname TEXT,
            mm_post_id TEXT,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT
        )
        """
        self.conn.execute(query_create)
        self.conn.commit()
        logger.info("Table 'alerts' checked or created.")

    def get_alert(self, fingerprint):
        query = "SELECT * FROM alerts WHERE fingerprint = ?"
        cursor = self.conn.execute(query, (fingerprint,))
        row = cursor.fetchone()
        return (
            {
                "fingerprint": row[1],
                "alertname": row[2],
                "mm_post_id": row[3],
                "status": row[4],
                "created_at": row[5],
                "updated_at": row[6],
            }
            if row
            else None
        )

    def add_alert(self, fingerprint, alertname, status, mm_post_id=None):
        query = """
        INSERT INTO alerts (fingerprint, alertname, status, mm_post_id, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        self.conn.execute(query, (fingerprint, alertname, status, mm_post_id, datetime.now().isoformat(), datetime.now().isoformat() ))
        self.conn.commit()

    def update_alert_status(self, fingerprint, new_status):
        logger.info(f"Updating alert with fingerprint: {fingerprint}")
        query = """
        UPDATE alerts
        SET status = ?, updated_at = ?
        WHERE fingerprint = ?
        """
        self.conn.execute(query, (new_status, datetime.now().isoformat(), fingerprint))
        self.conn.commit()
        logger.info(f"Alert with fingerprint {fingerprint} updated successfully.")

    def get_all_alerts(self):
        query = "SELECT * FROM alerts"
        cursor = self.conn.execute(query)
        return [
            {
                "id": row[0],
                "fingerprint": row[1],
                "alertname": row[2],
                "mm_post_id": row[3],
                "status": row[4],
                "created_at": row[5],
                "updated_at": row[6],
            }
            for row in cursor.fetchall()
        ]
    
    def delete_all_alerts(self):
        logger.info("Deleting all alerts from the database.")
        query = "DELETE FROM alerts"
        self.conn.execute(query)
        self.conn.commit()
        logger.info("All alerts deleted successfully.")