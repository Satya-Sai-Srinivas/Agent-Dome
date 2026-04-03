from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
import datetime

app = FastAPI(title="Threat Ingestion API")

# Define the exact structure of the logs we expect to receive
class LogEntry(BaseModel):
    timestamp: float
    ip_address: str
    method: str
    endpoint: str
    user_agent: str
    payload: str = ""

def process_log_async(log: LogEntry):
    # For now, we will just print to the terminal. 
    # Later, this will save to the database and trigger the AI.
    time_str = datetime.datetime.fromtimestamp(log.timestamp).strftime('%Y-%m-%d %H:%M:%S')
    
    if log.payload:
        print(f"[🚨 WARNING] Suspicious payload from {log.ip_address} at {time_str}: {log.payload}")
    else:
        print(f"[INFO] Clean traffic from {log.ip_address} at {time_str}")

@app.post("/ingest")
async def ingest_log(log: LogEntry, background_tasks: BackgroundTasks):
    # Pass the log to the background task to ensure a lightning-fast API response
    background_tasks.add_task(process_log_async, log)
    return {"status": "received"}

@app.get("/health")
async def health_check():
    return {"status": "API is live and healthy"}