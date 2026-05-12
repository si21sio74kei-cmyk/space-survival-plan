from fastapi import FastAPI, Depends, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models, ai_engine
import json, asyncio

app = FastAPI(title="DeepSpace AI Survival System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = models.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/api/status")
def get_status(db: Session = Depends(get_db)):
    status = db.query(models.SurvivalStatus).order_by(models.SurvivalStatus.id.desc()).first()
    if not status:
        status = models.SurvivalStatus()
        db.add(status)
        db.commit()
        db.refresh(status)
    return status

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # 模拟实时数据推送和 AI 决策
            data = ai_engine.simulate_step()
            await websocket.send_text(json.dumps(data))
            await asyncio.sleep(2)
    except WebSocketDisconnect:
        print("Client disconnected")

if __name__ == "__main__":
    import uvicorn, asyncio
    uvicorn.run(app, host="0.0.0.0", port=8001)
