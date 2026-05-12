# 深空AI生存系统 - Vercel部署指南

## 问题诊断

### 为什么之前部署失败？

**参考仓库 `food-ai-v3` 的成功部署原因：**
```
food-ai-v3/
├── food_guardian_ai_2.py  ← Flask应用（根目录，Vercel自动识别）
├── templates/              ← HTML模板
├── static/                 ← 静态资源
├── requirements.txt        ← 依赖（根目录）
```

**我们的错误结构：**
```
太空梦想计划/
├── backend/
│   └── SpaceSurvivalSystem.py  ← 入口在子目录（Vercel无法识别）
├── frontend/
└── vercel.json  ← 配置指向子目录（不符合约定）
```

### 根本原因

Vercel对Python项目有严格的约定：
1. ✅ 入口文件必须在**根目录**或 `/api/` 目录
2. ✅ `requirements.txt` 必须在**根目录**
3. ✅ 使用 `/api/` 目录作为Serverless函数约定

## 修复方案

### 1. 创建标准入口文件

**文件：`api/index.py`**
```python
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
```

**作用：**
- 符合Vercel `/api/` 目录约定
- 自动识别为Python Serverless函数
- 导出 `app` 实例供Vercel使用

### 2. 使用正确的vercel.json配置

```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    },
    {
      "src": "frontend/**",
      "use": "@vercel/static"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "api/index.py"
    },
    {
      "src": "/(.*)",
      "dest": "frontend/$1"
    }
  ]
}
```

**路由规则：**
- `/api/*` → 转发到 Python后端
- `/*` → 转发到前端静态文件

### 3. 修改后台模拟机制

**问题：** Vercel Serverless不支持后台线程

**解决方案：** 使用FastAPI中间件
```python
@app.middleware("http")
async def auto_simulate(request: Request, call_next):
    """每次API请求时自动执行系统模拟"""
    if request.url.path.startswith("/api/"):
        ai_engine.simulate_step()  # 执行模拟
    response = await call_next(request)
    return response
```

**工作原理：**
- 前端每3秒请求API
- 中间件自动执行模拟
- 返回最新数据
- 完美替代后台线程

### 4. 前端API地址动态适配

```javascript
// frontend/js/api.js
const API_BASE = window.location.hostname === 'localhost' 
    ? 'http://localhost:8001/api' 
    : '/api';  // Vercel使用相对路径
```

## 部署流程

### 1. 提交代码
```bash
git add -A
git commit -m "修复Vercel部署配置"
git push origin main
```

### 2. 配置环境变量
在Vercel控制台配置：
- **ZHIPU_API_KEY**（全大写）= sk-xxxxx...

### 3. 验证部署

**测试API：**
```
https://space-survival-plan.vercel.app/api/survival-status
```

**预期返回：**
```json
{
  "mission_day": 47,
  "survival_index": 91.3,
  "crew_count": 4,
  "estimated_survival_days": 41.8
}
```

## 预期效果

✅ 顶部状态栏动态更新
✅ 生存时间实时计算
✅ 图表正常渲染
✅ AI日志自动滚动
✅ 所有模块可切换

## 技术对比

| 项目 | 参考仓库 | 我们的项目 |
|------|----------|------------|
| 框架 | Flask | FastAPI |
| 架构 | 前后端一体化 | 前后端分离 |
| 入口文件 | 根目录 | /api/index.py |
| 后台模拟 | 无 | 中间件自动模拟 |
| 数据库 | JSON文件 | SQLite（内存模式） |

---

**部署状态：** ✅ 已修复，等待Vercel自动部署
**最后更新：** 2026-05-12
