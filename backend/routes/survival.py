from fastapi import APIRouter
from services.ai_engine import engine
from services.survival_predictor import SurvivalPredictor

router = APIRouter()

@router.get("/survival-status")
def get_survival_status():
    """
    获取当前生存状态
    包括生存指数、任务天数、乘员数等核心信息
    """
    status = engine.get_current_status()
    
    # 计算预测数据
    survival_days = SurvivalPredictor.predict_survival_days(status)
    predictions = SurvivalPredictor.predict_timeline(status)
    
    return {
        "mission_day": status['mission_day'],
        "survival_index": round(status['survival_index'], 1),
        "crew_count": status['crew_count'],
        "estimated_survival_days": survival_days,
        "predictions": predictions,
        "emergency_mode": False  # 内存存储，暂不支持emergency_mode
    }

@router.post("/reset-mission")
def reset_mission():
    """
    重置任务（用于测试）
    """
    from services.ai_engine import get_persistent_state
    state, logs = get_persistent_state()
    
    # 重置状态
    state['mission_day'] = 1
    state['survival_index'] = 98.0
    state['food_stability'] = 95.0
    state['medical_safety'] = 98.0
    state['energy_level'] = 92.0
    
    return {"message": "Mission reset successfully", "new_mission_day": state['mission_day']}
