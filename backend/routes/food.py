from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models import SurvivalStatus, SessionLocal
from services.ai_engine import engine
from services.food_manager import FoodManager

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/food-system")
def get_food_system(db: Session = Depends(get_db)):
    """
    获取食物系统状态
    包括食物库存、新鲜度、蛋白质、水资源等
    """
    status = engine.get_current_status()
    
    # 检查警告
    warnings = FoodManager.check_food_warnings(status)
    
    return {
        "food_stability": round(status.food_stability, 1),
        "protein_level": round(status.protein_level, 1),
        "water_reserve": round(status.water_reserve, 1),
        "diet_advice": "标准配给" if status.food_stability > 50 else "低能耗营养模式",
        "warnings": warnings,
        "consumption_rate": FoodManager.calculate_consumption(status.food_stability, status.crew_count)
    }

@router.post("/food/adjust-ration")
def adjust_ration_endpoint(db: Session = Depends(get_db)):
    """
    AI调整配给方案
    """
    status = engine.get_current_status()
    diet_advice = FoodManager.adjust_ration(status, "")
    
    db.merge(status)
    db.commit()
    
    return {
        "message": "Ration adjusted",
        "diet_advice": diet_advice,
        "crew_count": status.crew_count
    }
