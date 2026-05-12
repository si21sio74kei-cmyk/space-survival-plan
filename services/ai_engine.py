import random
import datetime
import json
import os
from zhipuai import ZhipuAI
from config import ZHIPU_API_KEY

# 延迟初始化client，避免API KEY为空时失败
client = None
if ZHIPU_API_KEY:
    try:
        client = ZhipuAI(api_key=ZHIPU_API_KEY)
    except Exception as e:
        print(f"AI client initialization failed: {e}")
        client = None

# Vercel Serverless环境：使用函数属性模拟持久化存储
# 每次请求时，函数实例会保持，但全局变量会重置
def get_persistent_state():
    """获取持久化状态（Vercel兼容）"""
    if not hasattr(get_persistent_state, '_state'):
        # 初始化状态
        get_persistent_state._state = {
            'mission_day': 1,
            'survival_index': 98.0,
            'food_stability': 95.0,
            'medical_safety': 98.0,
            'energy_level': 92.0,
            'oxygen_level': 99.0,
            'co2_level': 0.04,
            'radiation_level': 0.0,
            'protein_level': 100.0,
            'water_reserve': 100.0,
            'medical_temp': -70.0,
            'humidity': 45.0,
            'pressure': 101.3,
            'backup_power_hours': 48.0,
            'crew_count': 4,
            'last_updated': datetime.datetime.utcnow().isoformat()
        }
        get_persistent_state._logs = []
        get_persistent_state._logs.append({
            'timestamp': datetime.datetime.utcnow().isoformat(),
            'log_type': 'INFO',
            'message': '系统初始化完成，开始深空生存任务',
            'ai_decision': 'AI启动深空生存监控系统'
        })
    return get_persistent_state._state, get_persistent_state._logs

class AISurvivalEngine:
    """AI生存引擎 - 负责调用GLM-4进行决策分析并执行系统联动（Vercel兼容版）"""
    
    def __init__(self):
        self.mission_start = datetime.datetime.utcnow()

    def get_current_status(self):
        """获取当前生存状态（Vercel兼容 - 使用内存存储）"""
        state, logs = get_persistent_state()
        # 添加额外字段
        status = state.copy()
        status['base_stability'] = (status['energy_level'] + status['food_stability'] + status['medical_safety']) / 3
        status['environment_score'] = (status['oxygen_level'] + status['humidity'] * 2 + status['pressure']) / 3
        status['estimated_survival_days'] = int(status['survival_index'] * 1.5)
        return status

    def get_food_inventory(self):
        """获取食物库存"""
        state, _ = get_persistent_state()
        return {
            'total_stability': round(state['food_stability'], 1),
            'protein_level': round(state['protein_level'], 1),
            'water_reserve': round(state['water_reserve'], 1),
            'categories': [
                {'name': '蛋白质储备', 'value': round(state['protein_level'], 1), 'unit': '%'},
                {'name': '水资源', 'value': round(state['water_reserve'], 1), 'unit': '%'},
                {'name': '冷冻食品', 'value': round(state['food_stability'] * 0.6, 1), 'unit': '%'},
                {'name': '脱水食品', 'value': round(state['food_stability'] * 0.4, 1), 'unit': '%'}
            ]
        }

    def get_medical_status(self):
        """获取医疗状态"""
        state, _ = get_persistent_state()
        return {
            'safety_level': round(state['medical_safety'], 1),
            'temperature': state['medical_temp'],
            'supplies': round(state['medical_safety'], 1),
            'items': [
                {'name': '疫苗冷藏库', 'temp': state['medical_temp'], 'status': '正常' if state['medical_temp'] < -60 else '警告'},
                {'name': '血浆储存', 'temp': state['medical_temp'] + 5, 'status': '正常'},
                {'name': '药品柜', 'temp': 4, 'status': '正常'}
            ]
        }

    def get_energy_status(self):
        """获取能源状态"""
        state, _ = get_persistent_state()
        return {
            'level': round(state['energy_level'], 1),
            'backup_hours': round(state['backup_power_hours'], 1),
            'consumption_rate': 0.5,
            'sources': [
                {'name': '主反应堆', 'value': round(state['energy_level'] * 0.7, 1)},
                {'name': '太阳能板', 'value': round(state['energy_level'] * 0.2, 1)},
                {'name': '备用电池', 'value': round(state['energy_level'] * 0.1, 1)}
            ]
        }

    def get_environment_status(self):
        """获取环境状态"""
        state, _ = get_persistent_state()
        return {
            'oxygen': round(state['oxygen_level'], 1),
            'co2': state['co2_level'],
            'radiation': round(state['radiation_level'], 1),
            'humidity': round(state['humidity'], 1),
            'pressure': round(state['pressure'], 1),
            'temperature': 22
        }

    def get_recent_logs(self, limit=20):
        """获取最近的AI日志"""
        _, logs = get_persistent_state()
        return logs[-limit:]

    def generate_report(self, report_type='daily'):
        """生成AI报告"""
        state, logs = get_persistent_state()
        return {
            'type': report_type,
            'mission_day': state['mission_day'],
            'summary': f'任务第{state["mission_day"]}天，系统运行基本稳定',
            'recommendations': [
                '继续监控能源消耗',
                '保持医疗冷链温度',
                '优化营养配给方案'
            ],
            'timestamp': datetime.datetime.utcnow().isoformat()
        }

    def trigger_emergency(self, level='warning'):
        """触发紧急协议"""
        state, logs = get_persistent_state()
        
        emergency_messages = {
            'warning': '启动黄色预警协议',
            'critical': '启动红色紧急协议',
            'emergency': '启动最高级别应急响应'
        }
        
        message = emergency_messages.get(level, '启动预警协议')
        
        logs.append({
            'timestamp': datetime.datetime.utcnow().isoformat(),
            'log_type': 'CRITICAL',
            'message': message,
            'ai_decision': f'AI已触发{level}级别紧急协议'
        })
        
        return {
            'status': 'activated',
            'level': level,
            'message': message
        }

    def analyze_with_ai(self, status):
        """调用GLM-4 AI分析当前状态并返回决策"""
        ai_advice = "系统运行稳定"
        ai_action_taken = []
        
        # 如果没有AI客户端，直接返回默认建议
        if client is None:
            return ai_advice, ai_action_taken
        
        try:
            prompt = f"""
你是一个深空基地的 AI 生存控制核心。当前状态如下：
- 任务天数: {status['mission_day']}
- 能源水平: {status['energy_level']:.1f}%
- 食物稳定性: {status['food_stability']:.1f}%
- 医疗安全: {status['medical_safety']:.1f}%
- 辐射等级: {status['radiation_level']:.1f}
- 氧气浓度: {status['oxygen_level']:.1f}%
- 水资源: {status['water_reserve']:.1f}%
- 蛋白质储备: {status['protein_level']:.1f}%

请分析当前风险，并给出具体的资源调度指令。格式要求：
1. 先说明当前最紧急的问题
2. 给出具体行动（如：降低食物区冷却精度15%、优先保障医疗区等）
3. 解释原因

控制在80字以内。
"""
            response = client.chat.completions.create(
                model="glm-4-air",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            ai_advice = response.choices[0].message.content
            
            # 解析 AI 决策并执行真实联动
            advice_lower = ai_advice.lower()
            
            # 联动规则1: 如果 AI 建议降低冷却精度
            if any(keyword in advice_lower for keyword in ['降低冷却', '减少制冷', '关闭非必要', '降低功耗']):
                status['food_stability'] -= 2.5
                status['energy_level'] += 3.0
                ai_action_taken.append("已降低非关键区域冷却精度")
            
            # 联动规则2: 如果 AI 建议优先保障医疗
            if any(keyword in advice_lower for keyword in ['医疗优先', '保护药品', '疫苗', '血浆']):
                status['medical_safety'] = min(100, status['medical_safety'] + 3)
                status['energy_level'] -= 2.0
                ai_action_taken.append("已提升医疗冷链优先级")
            
            # 联动规则3: 如果 AI 建议调整营养分配
            if any(keyword in advice_lower for keyword in ['营养', '食谱', '配给', '蛋白质']):
                status['protein_level'] -= 0.5
                ai_action_taken.append("已启动AI营养优化策略")
                
        except Exception as e:
            ai_advice = f"AI 连接异常: {str(e)[:50]} (已切换至本地规则模式)"
        
        return ai_advice, ai_action_taken

    def simulate_step(self):
        """模拟一步系统演化（Vercel兼容 - 使用内存存储）"""
        status = self.get_current_status()
        state, logs = get_persistent_state()
        
        # 1. 基础衰减与消耗
        energy_decay = random.uniform(0.2, 0.8)
        food_decay = random.uniform(0.1, 0.4)
        water_consumption = random.uniform(0.05, 0.2)
        protein_consumption = random.uniform(0.05, 0.15)
        
        status['energy_level'] = max(0, status['energy_level'] - energy_decay)
        status['food_stability'] = max(0, status['food_stability'] - food_decay)
        status['water_reserve'] = max(0, status['water_reserve'] - water_consumption)
        status['protein_level'] = max(0, status['protein_level'] - protein_consumption)
        status['humidity'] = max(30, min(60, status['humidity'] + random.uniform(-1, 1)))
        status['pressure'] = max(95, min(105, status['pressure'] + random.uniform(-0.1, 0.1)))
        status['backup_power_hours'] = max(0, status['backup_power_hours'] - 0.01)
        status['mission_day'] += 1
        
        # AI 营养分配与食谱调整逻辑
        diet_advice = "标准配给"
        if status['food_stability'] < 50:
            diet_advice = "低能耗营养模式：减少高蛋白摄入，增加合成碳水比例。"
        
        # 2. 随机事件触发 (太阳风暴/能源危机)
        event_log = []
        radiation_spike = random.random() < 0.05
        emergency_mode = False
        
        if radiation_spike:
            status['radiation_level'] = random.uniform(50, 95)
            event_log.append("警告：检测到强太阳辐射风暴！")
            event_log.append("AI决策：已启动地下储藏模式，优先保障医疗冷链。")
            status['food_stability'] -= 5
            status['medical_safety'] = min(100, status['medical_safety'] + 5)
            status['medical_temp'] = max(-80, status['medical_temp'] - 2)
            emergency_mode = True
        else:
            status['radiation_level'] = max(0, status['radiation_level'] - 2)
            event_log.append("环境监测：舱内环境稳定。")
            
        # 3. AI 动态能源调节联动
        if status['energy_level'] < 30:
            event_log.append("AI决策：能源低于阈值，已降低非关键区域冷却精度。")
            status['food_stability'] -= 1.0
            status['oxygen_level'] = max(0, status['oxygen_level'] - 0.1)
            if status['energy_level'] < 10:
                emergency_mode = True

        # 4. 执行多系统联动逻辑
        
        # 能源联动：能源不足时自动降低次级系统
        if status['energy_level'] < 40:
            reduction_rate = (40 - status['energy_level']) * 0.1
            status['food_stability'] -= reduction_rate
            event_log.append(f"能源联动：已降低次级冷却系统精度{reduction_rate:.1f}%")
        
        # 辐射联动：辐射升高时强化医疗保护
        if status['radiation_level'] > 50:
            protection_boost = (status['radiation_level'] - 50) * 0.05
            status['medical_safety'] = min(100, status['medical_safety'] + protection_boost)
            status['food_stability'] -= protection_boost * 0.5
            event_log.append(f"辐射联动：已启动地下储藏模式，医疗区防护+{protection_boost:.1f}%")
        
        # 食物联动：食物短缺时调整配给
        if status['food_stability'] < 30:
            status['crew_count'] = max(1, status['crew_count'] - 1)
            diet_advice = "紧急配给模式：每日热量摄入降低20%"
            event_log.append("食物联动：已启动紧急营养分配方案")
        
        # 重新计算综合生存指数
        status['survival_index'] = (
            status['food_stability'] * 0.2 +
            status['medical_safety'] * 0.3 +
            status['energy_level'] * 0.2 +
            status['oxygen_level'] * 0.2 +
            status['water_reserve'] * 0.1
        )
        
        # 生成预测时间线（基于当前状态推演）
        predictions = [
            max(0, int(status['survival_index'] * 0.9)),
            max(0, int(status['survival_index'] * 0.75)),
            max(0, int(status['survival_index'] * 0.6)),
            max(0, int(status['survival_index'] * 0.45))
        ]
        
        # 5. 调用 GLM-4-AIR 进行真实 AI 决策
        ai_advice, ai_action_taken = self.analyze_with_ai(status)
        
        # 6. 记录日志（内存存储）
        log_type = "CRITICAL" if emergency_mode else ("WARNING" if radiation_spike else "INFO")
        log_message = f"AI 决策: {ai_advice} | 执行动作: {'; '.join(ai_action_taken)}"
        logs.append({
            'timestamp': datetime.datetime.utcnow().isoformat(),
            'log_type': log_type,
            'message': log_message,
            'ai_decision': ai_advice
        })
        
        # 只保留最近50条日志
        if len(logs) > 50:
            logs[:] = logs[-50:]
        
        # 合并 AI 采取的行动到日志
        if ai_action_taken:
            event_log.extend([f"✓ {action}" for action in ai_action_taken])
        
        return {
            "mission_day": status['mission_day'],
            "survival_index": status['survival_index'],
            "energy_level": status['energy_level'],
            "food_stability": status['food_stability'],
            "medical_safety": status['medical_safety'],
            "oxygen_level": status['oxygen_level'],
            "radiation_level": status['radiation_level'],
            "protein_level": status['protein_level'],
            "water_reserve": status['water_reserve'],
            "humidity": status['humidity'],
            "pressure": status['pressure'],
            "backup_power_hours": round(status['backup_power_hours'], 1),
            "crew_count": status['crew_count'],
            "diet_advice": diet_advice,
            "emergency_mode": emergency_mode,
            "predictions": predictions,
            "estimated_survival_days": int(status['survival_index'] * 1.5),
            "logs": event_log
        }

# 全局实例
engine = AISurvivalEngine()
