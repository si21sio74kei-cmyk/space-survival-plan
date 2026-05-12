from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import Base, engine
from routes import survival, food, medical, energy, environment, ai
import uvicorn
import os
import threading
import time
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

# 后台任务：每3秒自动更新一次系统状态
def background_simulation_loop():
    """后台模拟循环 - 每3秒执行一次系统演化"""
    print("🔄 后台模拟任务已启动：每3秒更新一次系统状态")
    while True:
        try:
            result = ai_engine.simulate_step()
            # print(f"📊 Mission Day {result['mission_day']}: Survival Index = {result['survival_index']:.1f}")
        except Exception as e:
            print(f"❌ 后台任务错误: {e}")
        time.sleep(3)  # 每3秒更新一次

# 启动后台任务
simulation_thread = threading.Thread(target=background_simulation_loop, daemon=True)
simulation_thread.start()

if __name__ == "__main__":
    # 从环境变量获取端口，默认8001
    port = int(os.getenv("PORT", 8001))
    print(f"🚀 DeepSpace AI Survival System 正在启动...")
    print(f"📡 API服务地址: http://0.0.0.0:{port}")
    print(f"🔗 前端访问地址: http://localhost:3000 (需单独启动前端服务器)")
    uvicorn.run(app, host="0.0.0.0", port=port)
