"""
DeepSpace AI Survival System - Vercel API入口
"""
import sys
import os

# 获取项目根目录
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
backend_dir = os.path.join(root_dir, 'backend')

# 添加backend到Python路径
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# 设置环境变量标记Vercel环境
os.environ['VERCEL'] = '1'

# 导入FastAPI应用
from SpaceSurvivalSystem import app

# Vercel需要的变量名
__all__ = ['app']
