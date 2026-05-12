import sys
import os

# 添加backend目录到Python路径，支持Vercel部署
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import Base, engine
from routes import survival, food, medical, energy, environment, ai
from services.ai_engine import engine as ai_engine

# 确保数据库表已创建
Base.metadata.create_all(bind=engine)

app = FastAPI(title="DeepSpace AI Survival Cold-Chain System")

# CORS配置：允许跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由模块
app.include_router(survival.router, prefix="/api", tags=["生存状态"])
app.include_router(food.router, prefix="/api", tags=["食物系统"])
app.include_router(medical.router, prefix="/api", tags=["医疗冷链"])
app.include_router(energy.router, prefix="/api", tags=["能源系统"])
app.include_router(environment.router, prefix="/api", tags=["环境控制"])
app.include_router(ai.router, prefix="/api", tags=["AI决策"])

# Vercel Serverless架构：每次请求时自动执行模拟
from fastapi import Request

@app.middleware("http")
async def auto_simulate(request: Request, call_next):
    """每次API请求时自动执行系统模拟（Vercel兼容）"""
    # 仅对/api路径执行模拟
    if request.url.path.startswith("/api/"):
        try:
            ai_engine.simulate_step()
        except Exception as e:
            print(f"Auto-simulate error: {e}")
    
    response = await call_next(request)
    return response

# 本地开发启动（Vercel环境下不会执行）
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
