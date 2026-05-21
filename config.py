import os

# 从环境变量读取 智谱 AI API Key
ZHIPU_API_KEY = os.getenv("ZHIPU_API_KEY", "")

# 智谱模型配置
ZHIPU_MODEL = "glm-4-air"

if not ZHIPU_API_KEY:
    # 本地开发提示
    import warnings
    warnings.warn(
        "未配置 ZHIPU_API_KEY 环境变量。AI 功能将不可用。\n"
        "请在 .env 文件中配置或在 Vercel 环境变量中设置。"
    )
