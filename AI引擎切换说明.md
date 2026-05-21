# AI引擎切换至智谱GLM-4-AIR说明

## ✅ 已完成的配置

### 1. 配置文件更新
- ✅ `.env` - 已配置智谱API密钥
- ✅ `config.py` - 已更新为 `ZHIPU_API_KEY` 和 `ZHIPU_MODEL`
- ✅ `ai_engine.py` - 已切换到智谱API接口

### 2. 智谱API配置详情
```
API密钥: 9cb31c9771804b209ff96423a06ac917.6quMFflk7V4Z6MyF
模型名称: glm-4-air
API端点: https://open.bigmodel.cn/api/paas/v4
```

### 3. 修改的文件清单
1. `.env` - API密钥配置
2. `.env.example` - 配置模板
3. `config.py` - 配置读取
4. `ai_engine.py` - AI引擎实现

## ️ 当前状态

**API返回429错误（配额不足/频率限制）**

可能原因：
1. API密钥配额已用完
2. 免费额度已耗尽
3. 需要充值或升级套餐

## 🔧 解决方案

### 方案1：检查智谱账户配额
1. 访问 https://open.bigmodel.cn/
2. 登录你的账户
3. 检查API调用配额和剩余次数
4. 如需更多配额，进行充值或升级

### 方案2：使用智谱免费额度
智谱平台通常提供：
- 新用户免费额度
- 每日免费调用次数
- 体验版模型

### 方案3：临时使用模拟模式
如果API暂时不可用，系统会自动降级到本地规则模式：
- ✅ 所有功能页面正常工作
- ✅ 数据同步和图表正常
- ❌ AI对话会显示友好错误提示

##  验证步骤

### 1. 重启应用
```bash
# 停止当前运行的Flask（Ctrl+C）
# 重新启动
python app.py
```

### 2. 查看启动日志
应该看到：
```
智谱 AI (GLM-4-AIR) 客户端初始化成功
```

### 3. 测试AI功能
访问 http://localhost:5000
在AI助手对话框输入问题，查看是否能正常回复

### 4. 检查API调用
浏览器F12 → Network → 查看 `/api/generate-report` 请求

## 🎯 功能说明

### 正常使用（API有效时）
- ✅ AI智能对话
- ✅ AI决策建议
- ✅ 自动资源调度
- ✅ 智能风险预警

### 降级模式（API不可用时）
- ✅ 所有手动操作功能
- ✅ 数据图表和监控
- ✅ 资源管理系统
- ✅ 环境控制系统
- ️ AI对话显示提示信息

##  智谱API文档

- 官方文档: https://open.bigmodel.cn/dev/api
- API密钥管理: https://open.bigmodel.cn/usercenter/apikeys
- 模型列表: https://open.bigmodel.cn/dev/api#language
- GLM-4-AIR说明: 高性价比的轻量级模型

## ❓ 常见问题

**Q: 429错误是什么意思？**
A: 表示API调用频率过高或配额不足。需要检查账户余额或等待配额重置。

**Q: 没有AI功能系统能用吗？**
A: 可以！除了AI对话和自动决策，所有其他功能都正常工作。

**Q: 如何增加API配额？**
A: 登录智谱开放平台，在账户中心充值或申请更多额度。

**Q: 可以切换回DeepSeek吗？**
A: 可以。修改 `.env` 和 `config.py` 中的配置即可。但根据项目要求，建议使用智谱API。

## 🔄 切换回DeepSeek（如需要）

如果将来需要切换回DeepSeek：

1. 修改 `.env`:
```env
DEEPSEEK_API_KEY=your_deepseek_key
```

2. 修改 `config.py`:
```python
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
```

3. 修改 `ai_engine.py`:
```python
from config import DEEPSEEK_API_KEY
client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com/v1")
model="deepseek-chat"
```

---

**最后更新**: 2026-05-17
**AI引擎**: 智谱 GLM-4-AIR
**状态**: 已配置，等待API配额确认
