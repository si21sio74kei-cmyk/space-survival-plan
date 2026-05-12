from fastapi import APIRouter
from services.ai_engine import engine

router = APIRouter()

@router.get("/medical-system")
def get_medical_system():
    """
    获取医疗冷链系统状态
    包括医疗安全、冷链温度、疫苗状态等
    """
    status = engine.get_current_status()
    
    # 判断冷链状态
    cold_chain_status = "Normal"
    if status['medical_temp'] > -60:
        cold_chain_status = "Warning"
    if status['medical_temp'] > -50:
        cold_chain_status = "Critical"
    
    return {
        "medical_safety": round(status['medical_safety'], 1),
        "medical_temp": round(status['medical_temp'], 1),
        "cold_chain_status": cold_chain_status,
        "vaccines": {
            "status": "Stable" if status['medical_safety'] > 70 else "At Risk",
            "storage_temp": -70
        },
        "blood_samples": {
            "status": "Stable" if status['medical_temp'] < -65 else "Warning",
            "storage_temp": -40
        },
        "biological_samples": {
            "status": "Stable" if status['medical_temp'] < -180 else "Critical",
            "storage_temp": -196
        }
    }

@router.post("/medical/priority")
def set_medical_priority():
    """
    设置医疗优先级
    优先保障医疗资源，消耗更多能源
    """
    from services.ai_engine import get_persistent_state
    state, logs = get_persistent_state()
    
    # 提升医疗安全，消耗能源
    state['medical_safety'] = min(100, state['medical_safety'] + 5)
    state['energy_level'] -= 3.0
    state['medical_temp'] = max(-80, state['medical_temp'] - 2)
    
    return {
        "message": "Medical priority increased",
        "medical_safety": state['medical_safety'],
        "energy_cost": 3.0
    }