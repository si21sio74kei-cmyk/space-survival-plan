"""
DeepSpace AI Survival System - Vercel 部署入口
"""
import sys
import os

# 添加backend目录到路径
backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# 导入FastAPI应用
from SpaceSurvivalSystem import app
