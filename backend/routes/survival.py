from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models import SurvivalStatus, SessionLocal, ResourceLog
from services.ai_engine import engine
from services.survival_predictor import SurvivalPredictor

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/survival-status")
def get_survival_status(db: Session = Depends(get_db)):
    """
    获取当前生存状态
    包括生存指数、任务天数、乘员数等核心信息
    """
    status = engine.get_current_status()
    
    # 计算预测数据
    survival_days = SurvivalPredictor.predict_survival_days(status)
    predictions = SurvivalPredictor.predict_timeline(status)
    
    return {
        "mission_day": status.mission_day,
        "survival_index": round(status.survival_index, 1),
        "crew_count": status.crew_count,
        "estimated_survival_days": survival_days,
        "predictions": predictions,
        "emergency_mode": status.emergency_mode if hasattr(status, 'emergency_mode') else False
    }

@router.post("/reset-mission")
def reset_mission(db: Session = Depends(get_db)):
    """
    重置任务（用于测试）
    """
    status = SurvivalStatus()
    db.add(status)
    db.commit()
    db.refresh(status)
    return {"message": "Mission reset successfully", "new_mission_day": status.mission_day}
