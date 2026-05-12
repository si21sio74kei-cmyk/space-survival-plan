# 深空AI生存冷链决策系统

DeepSpace AI Survival Cold-Chain Decision System - Mars Habitat Control Platform

## 项目简介

面向未来火星基地、月球基地、深空空间站的 **AI生存资源管理平台**。

系统核心目标：在资源有限的深空环境中，利用 AI 帮助人类长期生存。

## 技术栈

### 前端
- HTML5 + CSS3 + JavaScript
- Three.js（3D星空背景）
- GSAP（高级动画）
- ECharts（数据可视化）
- Glassmorphism UI（玻璃拟态设计）

### 后端
- Python 3.11+
- FastAPI
- SQLite
- WebSocket（实时通信）
- 智谱 GLM-4-AIR（AI决策引擎）

## 核心功能

### 1. AI 自主决策系统
- 实时调用智谱 GLM-4-AIR 生成决策建议
- 多系统联动逻辑（能源/辐射/食物）
- 紧急协议模式自动触发

### 2. 生存资源管理
- 食物资源系统（分类库存、新鲜度分析）
- 医疗冷链系统（疫苗/血浆温控）
- 能源管理系统（动态优化分配）
- 环境控制系统（O2/CO2/辐射监测）

### 3. 预测与预警
- 生存时间预测（D+30/60/90/120）
- 风险预测曲线
- AI 解释机制（决策原因透明化）

## 本地运行

### 后端启动
```powershell
cd backend
python SpaceSurvivalSystem.py
```

### 前端启动
```powershell
cd frontend
python -m http.server 3000
```

访问：http://localhost:3000

## Vercel 部署

### 1. 推送到 GitHub
```bash
git init
git add .
git commit -m "Initial commit: DeepSpace AI Survival System"
git branch -M main
git remote add origin https://github.com/si21sio74kei-cmyk/space-survival-plan.git
git push -u origin main
```

### 2. 连接 Vercel
1. 访问 [vercel.com](https://vercel.com)
2. 点击 "New Project"
3. 导入 GitHub 仓库
4. 配置环境变量：
   - `ZHIPU_API_KEY`: 您的智谱 API Key
5. 点击 "Deploy"

## 系统架构

```
┌─────────────────────────────────────┐
│         Frontend (HTML/JS)          │
│  Three.js + ECharts + GSAP          │
│  WebSocket Client                   │
└──────────────┬──────────────────────┘
               │ WebSocket
┌──────────────▼──────────────────────┐
│      Backend (FastAPI)              │
│  ├─ AI Engine (GLM-4-AIR)          │
│  ├─ Survival Logic                 │
│  ├─ Resource Management            │
│  └─ SQLite Database                │
└─────────────────────────────────────┘
```

## 功能联动示例

### 能源联动
当能源 < 40%：
- 自动降低次级冷却精度
- 食物保鲜度加速衰减
- 日志显示："能源联动：已降低次级冷却系统精度X%"

### 辐射联动
当辐射 > 50：
- 启动地下储藏模式
- 医疗区防护提升
- 牺牲部分食物保鲜保障医疗资源

### AI 决策执行
GLM-4 建议"降低冷却" → 
- 食物保鲜度 -2.5%
- 能源 +3%
- 日志显示："✓ 已降低非关键区域冷却精度"

## 比赛演示要点

1. **真实 AI 驱动**：每次决策都调用云端 GLM-4-AIR
2. **双向联动**：AI 建议 → 解析关键词 → 执行数值变化 → UI 反馈
3. **多层应急**：本地规则 + 云端 AI + 紧急协议三重保障
4. **航天级 UI**：NASA 控制中心风格 + 动态粒子背景

## 许可证

MIT License

## 联系方式

如有问题，请提交 Issue 或联系项目维护者。
