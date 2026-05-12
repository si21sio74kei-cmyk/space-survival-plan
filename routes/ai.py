from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models import ResourceLog, SessionLocal
from services.ai_engine import engine

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/ai-logs")
def get_ai_logs(db: Session = Depends(get_db)):
    """
    获取AI决策日志（最近20条）
    """
    logs = db.query(ResourceLog).order_by(ResourceLog.timestamp.desc()).limit(20).all()
    
    return [
        {
            "timestamp": log.timestamp.isoformat(),
            "log_type": log.log_type,
            "message": log.message,
            "ai_decision": log.ai_decision
        }
        for log in logs
    ]

@router.post("/ai-analysis")
def trigger_ai_analysis(db: Session = Depends(get_db)):
    """
    触发AI分析
    手动触发GLM-4分析当前状态并返回决策
    """
    status = engine.get_current_status()
    
    # 调用AI分析
    ai_advice, ai_actions = engine.analyze_with_ai(status)
    
    # 保存日志
    log_entry = ResourceLog(
        log_type="INFO",
        message=f"AI Analysis: {ai_advice} | Actions: {'; '.join(ai_actions)}",
        ai_decision=ai_advice
    )
    db.add(log_entry)
    db.merge(status)
    db.commit()
    
    return {
        "ai_advice": ai_advice,
        "actions_taken": ai_actions,
        "status_summary": {
            "energy": status.energy_level,
            "food": status.food_stability,
            "medical": status.medical_safety,
            "radiation": status.radiation_level
        }
    }
