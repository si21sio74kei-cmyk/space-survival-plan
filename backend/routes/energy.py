from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models import SurvivalStatus, SessionLocal
from services.ai_engine import engine
from services.energy_manager import EnergyManager

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/energy")
def get_energy_status(db: Session = Depends(get_db)):
    """
    获取能源系统状态
    包括能源水平、备用电源小时数等
    """
    status = engine.get_current_status()
    
    # 检查能源阈值
    events = EnergyManager.check_thresholds(status)
    
    return {
        "energy_level": round(status.energy_level, 1),
        "backup_power_hours": round(status.backup_power_hours, 1),
        "events": events,
        "power_distribution": {
            "cold_chain": 40,
            "life_support": 30,
            "ai_core": 20,
            "communications": 10
        }
    }

@router.post("/energy/low-power-mode")
def activate_low_power_mode(db: Session = Depends(get_db)):
    """
    启动低功耗模式
    """
    status = engine.get_current_status()
    
    # 应用低功耗模式
    actions = EnergyManager.apply_low_power_mode(status)
    
    db.merge(status)
    db.commit()
    
    return {
        "message": "Low power mode activated",
        "actions_taken": actions,
        "energy_level": status.energy_level
    }
