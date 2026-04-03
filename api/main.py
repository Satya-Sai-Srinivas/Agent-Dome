from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
import datetime

# --- NEW: Import your database logic ---
from database import init_db, AsyncSessionLocal, DBLogEntry

app = FastAPI(title="Threat Ingestion API")

class LogEntry(BaseModel):
    timestamp: float
    ip_address: str
    method: str
    endpoint: str
    user_agent: str
    payload: str = ""

# --- NEW: This is what triggers the message you're looking for ---
@app.on_event("startup")
async def on_startup():
    await init_db()
    print("✅ Database connection established and tables verified.")

async def process_log_async(log: LogEntry):
    time_str = datetime.datetime.fromtimestamp(log.timestamp).strftime('%Y-%m-%d %H:%M:%S')
    
    # 1. Console Logging
    if log.payload:
        print(f"[🚨 WARNING] Suspicious payload from {log.ip_address} at {time_str}: {log.payload}")
    else:
        print(f"[INFO] Clean traffic from {log.ip_address} at {time_str}")

    # 2. --- NEW: Persistent Database Storage ---
    async with AsyncSessionLocal() as session:
        new_log = DBLogEntry(
            timestamp=log.timestamp,
            ip_address=log.ip_address,
            method=log.method,
            endpoint=log.endpoint,
            user_agent=log.user_agent,
            payload=log.payload
        )
        session.add(new_log)
        await session.commit()

@app.post("/ingest")
async def ingest_log(log: LogEntry, background_tasks: BackgroundTasks):
    background_tasks.add_task(process_log_async, log)
    return {"status": "received and saved to database"}

@app.get("/health")
async def health_check():
    return {"status": "API is live and healthy"}