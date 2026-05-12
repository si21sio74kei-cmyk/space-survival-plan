"""
DeepSpace AI Survival System - Vercel部署入口文件
"""
import sys
import os

# 添加backend目录到Python路径
backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# 导入后端应用
from SpaceSurvivalSystem import app

# Vercel需要导出名为 'app' 的FastAPI实例
__all__ = ['app']
