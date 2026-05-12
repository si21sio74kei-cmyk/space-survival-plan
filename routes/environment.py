from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models import SurvivalStatus, SessionLocal
from services.ai_engine import engine

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/environment")
def get_environment_status(db: Session = Depends(get_db)):
    """
    获取环境控制系统状态
    包括氧气、CO2、温度、湿度、辐射、舱压等
    """
    status = engine.get_current_status()
    
    # 判断环境危险等级
    danger_level = "Normal"
    if status.radiation_level > 50 or status.oxygen_level < 50 or status.pressure < 95:
        danger_level = "Warning"
    if status.radiation_level > 80 or status.oxygen_level < 30 or status.pressure < 90:
        danger_level = "Critical"
    
    return {
        "oxygen_level": round(status.oxygen_level, 1),
        "co2_level": round(status.co2_level, 2),
        "temperature": round(status.medical_temp + 20, 1),  # 舱内温度估算
        "humidity": round(status.humidity, 1),
        "radiation_level": round(status.radiation_level, 1),
        "pressure": round(status.pressure, 1),
        "danger_level": danger_level
    }
