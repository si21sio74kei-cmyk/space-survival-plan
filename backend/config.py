import os

# 从环境变量读取 API Key（用于 Vercel 部署）
ZHIPU_API_KEY = os.getenv("ZHIPU_API_KEY", "")

# 如果环境变量为空，使用备用 Key（仅用于测试部署）
if not ZHIPU_API_KEY:
    ZHIPU_API_KEY = "57fff4bc9b704a2385c9918ae75f967b.Yq8MzZlugpsFwF6z"
