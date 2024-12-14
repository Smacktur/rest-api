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
            alert_id TEXT NOT NULL UNIQUE,
            fingerprint TEXT NOT NULL,
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

    def get_alert(self, alert_id):
        query = "SELECT * FROM alerts WHERE alert_id = ?"
        cursor = self.conn.execute(query, (alert_id,))
        row = cursor.fetchone()
        return (
            {
                "alert_id": row[1],
                "fingerprint": row[2],
                "alertname": row[3],
                "mm_post_id": row[4],
                "status": row[5],
                "created_at": row[6],
                "updated_at": row[7],
            }
            if row
            else None
        )

    def add_alert(self, alert_id, fingerprint, alertname, status, start_at,  mm_post_id=None):
        query = """
        INSERT INTO alerts (alert_id, fingerprint, alertname, status, mm_post_id, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        self.conn.execute(query, (alert_id, fingerprint, alertname, status, mm_post_id, start_at, datetime.now().isoformat() ))
        self.conn.commit()

    def update_alert_status(self, alert_id, new_status):
        logger.info(f"Updating alert with fingerprint: {alert_id}")
        query = """
        UPDATE alerts
        SET status = ?, updated_at = ?
        WHERE alert_id = ?
        """
        self.conn.execute(query, (new_status, datetime.now().isoformat(), alert_id))
        self.conn.commit()
        logger.info(f"Alert with fingerprint {alert_id} updated successfully.")

    def get_all_alerts(self):
        query = "SELECT * FROM alerts"
        cursor = self.conn.execute(query)
        return [
            {
                "id": row[0],
                "alert_id": row[1],
                "fingerprint": row[2],
                "alertname": row[3],
                "mm_post_id": row[4],
                "status": row[5],
                "created_at": row[6],
                "updated_at": row[7],
            }
            for row in cursor.fetchall()
        ]
    
    def delete_all_alerts(self):
        logger.info("Deleting all alerts from the database.")
        query = "DELETE FROM alerts"
        self.conn.execute(query)
        self.conn.commit()
        logger.info("All alerts deleted successfully.")