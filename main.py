from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import sqlite3
import pandas as pd
from datetime import datetime

app = FastAPI(title="Radar Enterprise API", version="1.0")

# Serve a pasta static para carregar o arquivo index.html
app.mount("/static", StaticFiles(directory="static"), name="static")

class SinalSchema(BaseModel):
    text: str
    url: str = None

@app.get("/")
def read_root():
    return FileResponse("static/index.html")

@app.get("/api/stats")
def get_stats():
    conn = sqlite3.connect("radar_enterprise.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM opportunities WHERE score >= 80")
    high = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM opportunities WHERE score >= 30 AND score < 80")
    medium = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM opportunities WHERE score < 30")
    low = cursor.fetchone()[0]
    
    conn.close()
    return {"high": high, "medium": medium, "low": low}

@app.get("/api/opportunities")
def get_opportunities():
    conn = sqlite3.connect("radar_enterprise.db")
    df = pd.read_sql_query("SELECT * FROM opportunities", conn)
    conn.close()
    return df.to_dict(orient="records")

@app.post("/api/signals")
def create_signal(sinal: SinalSchema):
    if len(sinal.text.strip()) < 12:
        raise HTTPException(status_code=400, detail="O texto precisa ter pelo menos 12 caracteres.")
    
    conn = sqlite3.connect("radar_enterprise.db")
    cursor = conn.cursor()
    
    score_mock = 85.0 # Aqui você chamará a sua engine_ia.py futuramente
    cursor.execute(
        "INSERT INTO signals (text, url, category, intent, score, created_at) VALUES (?, ?, ?, ?, ?, ?)",
        (sinal.text, sinal.url, "Consumidor", "high", score_mock, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )
    signal_id = cursor.lastrowid
    
    cursor.execute(
        "INSERT INTO opportunities (signal_id, score, status) VALUES (?, ?, ?)",
        (signal_id, score_mock, "new")
    )
    conn.commit()
    conn.close()
    
    return {"status": "success", "message": "Sinal processado e salvo com sucesso!", "signal_id": signal_id}