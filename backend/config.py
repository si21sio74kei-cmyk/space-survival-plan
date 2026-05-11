import os

# 从环境变量读取 API Key（用于 Vercel 部署）
# 本地开发时，请手动设置环境变量或取消下面一行的注释并填入您的 Key
# ZHIPU_API_KEY = "your_api_key_here"

ZHIPU_API_KEY = os.getenv("ZHIPU_API_KEY", "")

if not ZHIPU_API_KEY:
    raise ValueError(
        "未找到 ZHIPU_API_KEY 环境变量。\n"
        "请在 Vercel 环境变量中配置，或本地运行时设置环境变量。"
    )
