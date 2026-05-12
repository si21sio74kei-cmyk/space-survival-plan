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

@router.get("/medical-system")
def get_medical_system(db: Session = Depends(get_db)):
    """
    获取医疗冷链系统状态
    包括医疗安全、冷链温度、疫苗状态等
    """
    status = engine.get_current_status()
    
    # 判断冷链状态
    cold_chain_status = "Normal"
    if status.medical_temp > -60:
        cold_chain_status = "Warning"
    if status.medical_temp > -50:
        cold_chain_status = "Critical"
    
    return {
        "medical_safety": round(status.medical_safety, 1),
        "medical_temp": round(status.medical_temp, 1),
        "cold_chain_status": cold_chain_status,
        "vaccines": {
            "status": "Stable" if status.medical_safety > 70 else "At Risk",
            "storage_temp": -70
        },
        "blood_samples": {
            "status": "Stable" if status.medical_temp < -65 else "Warning",
            "storage_temp": -40
        },
        "biological_samples": {
            "status": "Stable" if status.medical_temp < -180 else "Critical",
            "storage_temp": -196
        }
    }

@router.post("/medical/priority")
def set_medical_priority(db: Session = Depends(get_db)):
    """
    设置医疗优先级
    优先保障医疗资源，消耗更多能源
    """
    status = engine.get_current_status()
    
    # 提升医疗安全，消耗能源
    status.medical_safety = min(100, status.medical_safety + 5)
    status.energy_level -= 3.0
    status.medical_temp = max(-80, status.medical_temp - 2)
    
    db.merge(status)
    db.commit()
    
    return {
        "message": "Medical priority increased",
        "medical_safety": status.medical_safety,
        "energy_cost": 3.0
    }