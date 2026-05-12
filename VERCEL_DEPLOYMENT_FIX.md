# Vercel部署修复说明

## 问题诊断

### 根本原因
Vercel使用**Serverless函数架构**，不支持：
1. ❌ 后台线程（threading）
2. ❌ 长时间运行的进程
3. ❌ 传统的uvicorn服务器模式

### 症状表现
- 前端页面正常加载（静态HTML成功）
- 所有数据都是静态的（143 DAYS固定值）
- API无法访问（localhost在Vercel上无效）
- 图表未渲染（无数据返回）

## 修复方案

### 1. 创建Vercel兼容的API入口

**文件**: `api/index.py`
```python
"""
Vercel Serverless Function入口
"""
import sys
import os

# 添加backend目录到Python路径
backend_dir = os.path.join(os.path.dirname(__file__), '..', 'backend')
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from SpaceSurvivalSystem import app
```

**为什么需要这个文件？**
- Vercel约定：`/api/`目录下的Python文件自动识别为Serverless函数
- 必须导出名为`app`的FastAPI实例
- Vercel会自动处理路由转发

### 2. 修改后台模拟机制

**原问题**: 使用threading后台线程（Vercel不支持）
```python
# ❌ 旧代码（不兼容Vercel）
simulation_thread = threading.Thread(target=background_simulation_loop, daemon=True)
simulation_thread.start()
```

**新方案**: 使用FastAPI中间件，每次API请求时自动模拟
```python
# ✅ 新代码（Vercel兼容）
@app.middleware("http")
async def auto_simulate(request: Request, call_next):
    """每次API请求时自动执行系统模拟"""
    if request.url.path.startswith("/api/"):
        try:
            ai_engine.simulate_step()  # 执行一次模拟
        except Exception as e:
            print(f"Auto-simulate error: {e}")
    
    response = await call_next(request)
    return response
```

**工作原理**:
- 前端每3秒发起一次API请求
- 中间件拦截请求，自动执行`simulate_step()`
- 系统数据更新后，返回给前端
- 完美替代后台线程，完全兼容Serverless架构

### 3. 配置vercel.json

```json
{
  "version": 2,
  "functions": {
    "api/index.py": {
      "runtime": "@vercel/python"
    }
  },
  "rewrites": [
    {
      "source": "/api/(.*)",
      "destination": "/api/index.py"
    },
    {
      "source": "/(.*)",
      "destination": "/frontend/$1"
    }
  ]
}
```

**路由规则**:
- `/api/*` → 转发到 `api/index.py`（Python后端）
- `/*` → 转发到 `frontend/`（静态前端）

### 4. 前端API地址动态适配

**文件**: `frontend/js/api.js`
```javascript
// 本地开发时使用localhost，生产环境使用相对路径
const API_BASE = window.location.hostname === 'localhost' 
    ? 'http://localhost:8001/api' 
    : '/api';
```

**工作原理**:
- 本地开发：`http://localhost:8001/api`
- Vercel生产：`/api`（相对路径，自动转发到后端）

### 5. requirements.txt移至根目录

Vercel要求依赖文件在项目根目录：
```
太空梦想计划/
├── requirements.txt  ← 必须在根目录
├── api/
│   ── index.py
├── backend/
│   └── SpaceSurvivalSystem.py
── frontend/
```

## 部署流程

### 1. 代码已推送
```bash
✅ Commit: 8e1b73c - 修复Vercel部署
✅ 推送到: https://github.com/si21sio74kei-cmyk/space-survival-plan.git
```

### 2. Vercel自动部署
1. Vercel检测到GitHub新提交
2. 自动构建Python函数（安装requirements.txt）
3. 部署前端静态文件
4. 配置路由规则

### 3. 环境变量配置
在Vercel控制台配置：
- **名称**: `ZHIPU_API_KEY`（必须全大写）
- **值**: 您的智谱AI密钥（sk-xxxxx...）
- **环境**: 勾选 Production

### 4. 验证部署

**检查部署状态**:
访问 https://vercel.com/si21sio74kei-cmyk/space-survival-plan

**测试API**:
```
https://space-survival-plan.vercel.app/api/survival-status
```

**预期返回**:
```json
{
  "mission_day": 47,
  "survival_index": 91.3,
  "crew_count": 4,
  "estimated_survival_days": 41.8
}
```

## 预期效果

部署完成后，刷新页面应该看到：

✅ **顶部状态栏动态更新**
- CREW: 4
- STABILITY: 实时波动（90-98%）
- DAY: 001 → 002 → 003...（每3秒+1）

✅ **预计生存时间实时计算**
- 从静态的143 DAYS变为动态值（约40-50天）

✅ **图表正常渲染**
- 五维雷达图显示实时数据
- 生存指数仪表盘（0-100%）
- 预测时间线图表（30/60/90/120天）

✅ **AI日志自动滚动**
- 右侧面板每3秒新增日志
- 显示AI决策内容

✅ **所有模块可切换**
- 左侧导航可点击切换不同系统视图
- 数据实时联动更新

## 技术要点总结

| 项目 | 修改前 | 修改后 |
|------|--------|--------|
| 后台模拟 | threading线程 | FastAPI中间件 |
| API入口 | backend/SpaceSurvivalSystem.py | api/index.py |
| API地址 | localhost硬编码 | 动态适配 |
| 依赖文件 | backend/requirements.txt | 根目录/requirements.txt |
| 路由配置 | builds+routes | functions+rewrites |

## 故障排查

### 如果仍然有问题

**1. 检查Vercel部署日志**
```
https://vercel.com/si21sio74kei-cmyk/space-survival-plan/functions
```

**2. 检查浏览器控制台（F12）**
- 查看Network标签，确认API请求返回200
- 查看Console标签，确认无JavaScript错误

**3. 测试API直连**
```bash
curl https://space-survival-plan.vercel.app/api/survival-status
```

**4. 检查环境变量**
- 确认 `ZHIPU_API_KEY` 已配置（全大写）
- 确认值为有效的智谱API密钥

## 参考文档

- Vercel Python运行时: https://vercel.com/docs/functions/runtimes/python
- FastAPI中间件: https://fastapi.tiangolo.com/tutorial/middleware/
- Vercel路由配置: https://vercel.com/docs/projects/project-configuration

---

**最后更新**: 2026-05-12
**部署状态**: ✅ 已推送至GitHub，等待Vercel自动部署
