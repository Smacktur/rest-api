from fastapi import FastAPI, HTTPException
from app.database import Database

app = FastAPI()
db = Database("/data/alerts.db")

@app.get("/check-alert")
async def check_alert(alert_id: str):
    alert = db.get_alert(alert_id)
    if alert:
        return {
            "exists": True,
            "fingerprint": alert["fingerprint"],
            "status": alert["status"],
            "alertname": alert["alertname"],
            "mm_post_id": alert["mm_post_id"],
            "created_at": alert["created_at"],
            "updated_at": alert["updated_at"]
        }
    return {"exists": False}

@app.post("/add-alert")
async def add_alert(
        alert_id: str,
        fingerprint: str,
        alertname: str,
        start_at: str,
        mm_post_id: str = None,
        status: str = "new" 
    ):
    if db.get_alert(alert_id):
        raise HTTPException(status_code=400, detail="Alert already exists")
    db.add_alert(alert_id, fingerprint, alertname, status, start_at, mm_post_id)
    return {"message": "Alert added successfully"}

@app.post("/resolve-alert")
async def resolve_alert(alert_id: str):
    alert = db.get_alert(alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    db.update_alert_status(alert_id, "resolved")
    return {"message": "Alert resolved successfully"}

@app.get("/get-alerts")
async def get_alerts():
    return db.get_all_alerts()

@app.delete("/delete-alerts")
async def delete_alerts():
    try:
        db.delete_all_alerts()
        return {"message": "All alerts have been deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to delete alerts.")