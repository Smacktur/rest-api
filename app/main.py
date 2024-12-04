from fastapi import FastAPI, HTTPException
from app.database import Database

app = FastAPI()
db = Database("/data/alerts.db")  # SQLite файл в общем томе

@app.get("/check-alert")
async def check_alert(fingerprint: str):
    alert = db.get_alert(fingerprint)
    if alert:
        return {
            "exists": True,
            "status": alert["status"],
            "mm_post_id": alert["mm_post_id"],
            "created_at": alert["created_at"],
        }
    return {"exists": False}

@app.post("/add-alert")
async def add_alert(fingerprint: str, status: str = "new", mm_post_id: str = None):
    if db.get_alert(fingerprint):
        raise HTTPException(status_code=400, detail="Alert already exists")
    db.add_alert(fingerprint, status, mm_post_id)
    return {"message": "Alert added successfully"}

@app.get("/get-alerts")
async def get_alerts():
    return db.get_all_alerts()