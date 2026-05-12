"""
DeepSpace AI Survival System - Vercel API Function
"""
import sys
import os

# 添加backend目录到Python路径
backend_dir = os.path.join(os.path.dirname(__file__), '..', 'backend')
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# 导入后端应用
from SpaceSurvivalSystem import app
