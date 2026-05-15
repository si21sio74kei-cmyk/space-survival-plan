import random
import datetime
import json
import os
import sys
from openai import OpenAI

# 添加父目录到路径以导入config
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from config import DEEPSEEK_API_KEY

# 延迟初始化client，避免API KEY为空时失败
client = None
if DEEPSEEK_API_KEY:
    try:
        client = OpenAI(
            api_key=DEEPSEEK_API_KEY,
            base_url="https://api.deepseek.com/v1"
        )
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
            # 基础生存状态
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
            'last_updated': datetime.datetime.utcnow().isoformat(),
            
            # 食物资源管理
            'food_inventory': [],  # 食物库存列表
            'consumption_rate': 1.0,  # 每日消耗速率
            'emergency_ration_mode': False,  # 紧急配给模式
            'ration_percentage': 100,  # 配给百分比
            'food_temperature_zones': {'zone1': -18, 'zone2': 4, 'zone3': -70},  # 温度区域
            'food_expiry_warning_days': 7,  # 过期预警天数
            'food_min_stock_warning': 20,  # 最低库存预警
            
            # 医疗冷链管理
            'medical_items': [],  # 医疗物品列表
            'medical_temp_range': {'min': -80, 'max': -60},  # 温度范围
            'medical_alert_threshold': 5,  # 警报阈值
            'medical_backup_trigger': 30,  # 备用电源触发条件
            'medical_priority_level': 'high',  # 优先级
            
            # 能源管理
            'energy_distribution': {  # 能源分配比例
                'medical': 30,
                'food': 25,
                'environment': 25,
                'other': 20
            },
            'energy_saving_mode': 'normal',  # 节能模式
            'solar_charging_hours': 8,  # 太阳能充电时间
            'low_battery_response': ['communications', 'life_support'],  # 低电量保留功能
            
            # 环境控制
            'env_targets': {  # 目标值
                'oxygen': 21.0,
                'temperature': 22.0,
                'humidity': 45.0,
                'co2_max': 0.5
            },
            'env_alerts': {  # 警报阈值
                'oxygen_min': 19.0,
                'oxygen_max': 23.0,
                'temp_min': 18.0,
                'temp_max': 26.0,
                'humidity_min': 30.0,
                'humidity_max': 60.0,
                'co2_max': 1.0
            },
            'ventilation_mode': 'auto',  # 通风模式
            'ventilation_cycle': 30,  # 循环时间(分钟)
            
            # AI预测与决策
            'ai_automation_level': 'semi-auto',  # 自动化级别
            'ai_risk_tolerance': 50,  # 风险承受度
            'ai_priority_preference': 'survival',  # 优先级偏好
            'prediction_params': {  # 预测参数
                'crew_count': 4,
                'mission_duration': 365,
                'activity_level': 'normal',
                'resupply_interval': 90
            },
            
            # 紧急协议
            'emergency_protocols': [],  # 协议配置
            'emergency_triggers': {  # 触发器
                'survival_index_min': 30,
                'energy_level_min': 10,
                'oxygen_level_min': 15
            },
            'emergency_actions': ['alert_crew', 'conserve_energy', 'prioritize_life_support'],  # 执行动作
            
            # 宇航员管理
            'crew_members': [  # 宇航员列表
                {
                    'id': 1,
                    'name': '宇航员A',
                    'weight': 70,
                    'age': 35,
                    'health_status': 'good',
                    'special_needs': [],
                    'calorie_needs': 2500,
                    'diet_requirements': [],
                    'allergies': []
                }
            ],
            'crew_activities': [],  # 活动安排
            
            # 系统设置
            'notification_settings': {  # 通知设置
                'alert_types': ['critical', 'warning'],
                'notification_methods': ['visual', 'sound']
            },
            'display_settings': {  # 显示设置
                'refresh_rate': 3,  # 刷新频率(秒)
                'chart_options': 'detailed'
            },
            'backup_settings': {  # 备份设置
                'auto_backup_time': '00:00',
                'data_retention_days': 30
            },
            
            # 通信与日志
            'communication_reports': [],  # 通信报告
            'manual_logs': [],  # 手动日志
            'report_preferences': {  # 报告偏好
                'depth': 'standard',
                'focus_areas': ['survival', 'resources']
            }
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
        
        # 智能计算预计生存天数（基于动态衰减率，与simulate_step保持一致）
        crew_members = state.get('crew_members', [])
        crew_count = len(crew_members) if crew_members else status['crew_count']
        
        # 计算乘员消耗乘数（与simulate_step()保持一致）
        if crew_count > 0 and crew_members:
            total_calorie_needs = sum(member.get('calorie_needs', 2500) for member in crew_members)
            avg_calorie_needs = total_calorie_needs / crew_count
            consumption_multiplier = avg_calorie_needs / 2500.0
            
            health_factors = []
            for member in crew_members:
                health = member.get('health_status', 'good')
                if health == 'poor':
                    health_factors.append(1.2)
                elif health == 'excellent':
                    health_factors.append(0.9)
                else:
                    health_factors.append(1.0)
            avg_health_factor = sum(health_factors) / len(health_factors)
            consumption_multiplier *= avg_health_factor
        else:
            consumption_multiplier = 1.0
        
        # 基础衰减率
        base_food_decay = 2.0
        base_water_consumption = 1.5
        base_energy_decay = 1.0
        base_oxygen_decay = 0.5
        
        # 应用乘员消耗乘数
        food_decay_rate = base_food_decay * consumption_multiplier
        water_consumption_rate = base_water_consumption * consumption_multiplier
        energy_decay_rate = base_energy_decay  # 能源衰减不受乘员影响
        oxygen_decay_rate = base_oxygen_decay  # 氧气衰减不受乘员影响
        
        # 根据能源分配比例调整（与simulate_step()保持一致）
        distribution = state.get('energy_distribution', {})
        medical_alloc = distribution.get('medical', 30)
        food_alloc = distribution.get('food', 25)
        env_alloc = distribution.get('environment', 25)
        alloc_factor = (medical_alloc + food_alloc + env_alloc) / 80.0
        if alloc_factor > 0:
            energy_decay_rate = energy_decay_rate / alloc_factor
        
        # 计算预计生存天数（资源量 / 衰减率）
        food_days = status['food_stability'] / food_decay_rate if food_decay_rate > 0 else 999
        energy_days = status['energy_level'] / energy_decay_rate if energy_decay_rate > 0 else 999
        oxygen_days = status['oxygen_level'] / oxygen_decay_rate if oxygen_decay_rate > 0 else 999
        water_days = status['water_reserve'] / water_consumption_rate if water_consumption_rate > 0 else 999
        
        status['estimated_survival_days'] = max(0, round(min(food_days, energy_days, oxygen_days, water_days), 1))
        
        # 智能生成预测时间线（基于真实衰减率推演）
        daily_decay = {
            'food': 2.0 * crew_count / 4.0,
            'energy': 1.0,
            'oxygen': 0.5,
            'water': 1.5 * crew_count / 4.0,
            'medical': 0.3
        }
        
        predictions = []
        for day in [30, 60, 90, 120]:
            food_future = max(0, status['food_stability'] - daily_decay['food'] * day)
            energy_future = max(0, status['energy_level'] - daily_decay['energy'] * day)
            oxygen_future = max(0, status['oxygen_level'] - daily_decay['oxygen'] * day)
            water_future = max(0, status['water_reserve'] - daily_decay['water'] * day)
            medical_future = max(0, status['medical_safety'] - daily_decay['medical'] * day)
            
            predicted_index = (
                food_future * 0.2 +
                medical_future * 0.3 +
                energy_future * 0.2 +
                oxygen_future * 0.2 +
                water_future * 0.1
            )
            predictions.append(round(max(0, predicted_index), 1))
        
        status['predictions'] = predictions
        
        # emergency_mode默认为False（只在simulate_step中可能为True）
        status['emergency_mode'] = False
        
        return status

    def get_food_inventory(self):
        """获取食物库存"""
        state, _ = get_persistent_state()
        return {
            'food_stability': round(state['food_stability'], 1),  # 前端图表所需字段
            'protein_level': round(state['protein_level'], 1),
            'water_reserve': round(state['water_reserve'], 1),
            'total_stability': round(state['food_stability'], 1),
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
            'medical_safety': round(state['medical_safety'], 1),  # 前端所需字段
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
            'energy_level': round(state['energy_level'], 1),  # 前端所需字段
            'level': round(state['energy_level'], 1),
            'backup_hours': round(state['backup_power_hours'], 1),
            'backup_power_hours': round(state['backup_power_hours'], 1),  # 前端所需字段
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
            'oxygen_level': round(state['oxygen_level'], 1),  # 前端所需字段
            'humidity': round(state['humidity'], 1),  # 前端所需字段
            'pressure': round(state['pressure'], 1),  # 前端所需字段
            'radiation_level': round(state['radiation_level'], 1),  # 前端所需字段
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

    def generate_report(self, report_type='daily', query=None):
        """生成AI报告或回答用户提问（使用智谱API）"""
        state, logs = get_persistent_state()
        status = self.get_current_status()
        
        # 如果没有AI客户端，返回基础报告
        if client is None:
            return {
                'type': report_type,
                'mission_day': state['mission_day'],
                'summary': f'任务第{state["mission_day"]}天，系统运行基本稳定',
                'recommendations': ['继续监控能源消耗', '保持医疗冷链温度', '优化营养配给方案'],
                'timestamp': datetime.datetime.utcnow().isoformat()
            }
        
        try:
            if query:
                # 处理用户自由问答
                prompt = f"""
你是一个深空基地的 AI 生存控制核心。当前状态如下：
- 任务天数: {status['mission_day']}
- 生存指数: {status['survival_index']:.1f}%
- 能源水平: {status['energy_level']:.1f}%
- 食物稳定性: {status['food_stability']:.1f}%
- 医疗安全: {status['medical_safety']:.1f}%
- 氧气浓度: {status['oxygen_level']:.1f}%
- 水资源: {status['water_reserve']:.1f}%

宇航员询问: "{query}"
请结合当前系统状态，给出专业、简洁且符合深空生存背景的回答。
控制在100字以内。
"""
            else:
                # 处理固定报告
                prompt = f"""
你是一个深空基地的 AI 生存控制核心。当前状态如下：
- 任务天数: {status['mission_day']}
- 生存指数: {status['survival_index']:.1f}%
- 能源水平: {status['energy_level']:.1f}%
- 食物稳定性: {status['food_stability']:.1f}%
- 医疗安全: {status['medical_safety']:.1f}%
- 氧气浓度: {status['oxygen_level']:.1f}%
- 水资源: {status['water_reserve']:.1f}%

请生成一份{report_type}报告，包括：
1. 当前系统状态总结
2. 主要风险点
3. 具体建议措施

控制在150字以内。
"""
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            
            return {
                'type': report_type,
                'mission_day': state['mission_day'],
                'summary': response.choices[0].message.content,
                'report': response.choices[0].message.content, # 兼容前端字段
                'timestamp': datetime.datetime.utcnow().isoformat()
            }
        except Exception as e:
            return {
                'type': report_type,
                'mission_day': state['mission_day'],
                'summary': f'AI报告生成失败: {str(e)[:50]}',
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
                model="deepseek-chat",
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
        
        # 根据乘员配置调整消耗率
        crew_members = state.get('crew_members', [])
        crew_count = len(crew_members)
        
        if crew_count > 0:
            # 计算平均热量需求
            total_calorie_needs = sum(member.get('calorie_needs', 2500) for member in crew_members)
            avg_calorie_needs = total_calorie_needs / crew_count
            
            # 根据热量需求调整消耗率（基准2500卡）
            consumption_multiplier = avg_calorie_needs / 2500.0
            
            # 考虑特殊健康状况
            health_factors = []
            for member in crew_members:
                health = member.get('health_status', 'good')
                if health == 'poor':
                    health_factors.append(1.2)  # 健康状况差，消耗增加20%
                elif health == 'excellent':
                    health_factors.append(0.9)  # 健康状况好，消耗减少10%
                else:
                    health_factors.append(1.0)
            
            avg_health_factor = sum(health_factors) / len(health_factors)
            consumption_multiplier *= avg_health_factor
        else:
            consumption_multiplier = 1.0
        
        # 应用乘数
        food_decay = food_decay * consumption_multiplier
        water_consumption = water_consumption * consumption_multiplier
        protein_consumption = protein_consumption * consumption_multiplier
        
        # 根据能源分配比例调整衰减率
        distribution = state.get('energy_distribution', {})
        medical_alloc = distribution.get('medical', 30)
        food_alloc = distribution.get('food', 25)
        env_alloc = distribution.get('environment', 25)
        
        # 分配越低，衰减越快（基准75%）
        alloc_factor = (medical_alloc + food_alloc + env_alloc) / 80.0
        if alloc_factor > 0:
            energy_decay = energy_decay / alloc_factor
        
        status['energy_level'] = max(0, status['energy_level'] - energy_decay)
        status['food_stability'] = max(0, status['food_stability'] - food_decay)
        status['water_reserve'] = max(0, status['water_reserve'] - water_consumption)
        status['protein_level'] = max(0, status['protein_level'] - protein_consumption)
        
        # 环境参数向目标值靠拢
        env_targets = state.get('env_targets', {})
        target_temp = env_targets.get('temperature', 22.0)
        target_humidity = env_targets.get('humidity', 45.0)
        target_oxygen = env_targets.get('oxygen', 21.0)
        
        # 温度向目标值缓慢靠近（每次调整0.1度）
        temp_diff = target_temp - status.get('temperature', 22.0)
        status['temperature'] = (status.get('temperature', 22.0) or 22.0) + temp_diff * 0.1 + random.uniform(-0.5, 0.5)
        
        # 湿度向目标值靠近
        humidity_diff = target_humidity - status['humidity']
        status['humidity'] = max(30, min(60, status['humidity'] + humidity_diff * 0.1 + random.uniform(-1, 1)))
        
        # 氧气向目标值靠近
        oxygen_diff = target_oxygen - status['oxygen_level']
        status['oxygen_level'] = max(0, min(100, status['oxygen_level'] + oxygen_diff * 0.05 + random.uniform(-0.5, 0.5)))
        
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
        
        # 智能计算预计生存天数
        crew_count = max(1, status['crew_count'])
        food_days = status['food_stability'] / (2.0 * crew_count / 4.0)
        energy_days = status['energy_level'] / 1.0
        oxygen_days = status['oxygen_level'] / 0.5
        water_days = status['water_reserve'] / (1.5 * crew_count / 4.0)
        estimated_survival_days = max(0, round(min(food_days, energy_days, oxygen_days, water_days), 1))
        
        # 智能生成预测时间线
        daily_decay = {
            'food': 2.0 * crew_count / 4.0,
            'energy': 1.0,
            'oxygen': 0.5,
            'water': 1.5 * crew_count / 4.0,
            'medical': 0.3
        }
        
        predictions = []
        for day in [30, 60, 90, 120]:
            food_future = max(0, status['food_stability'] - daily_decay['food'] * day)
            energy_future = max(0, status['energy_level'] - daily_decay['energy'] * day)
            oxygen_future = max(0, status['oxygen_level'] - daily_decay['oxygen'] * day)
            water_future = max(0, status['water_reserve'] - daily_decay['water'] * day)
            medical_future = max(0, status['medical_safety'] - daily_decay['medical'] * day)
            
            predicted_index = (
                food_future * 0.2 +
                medical_future * 0.3 +
                energy_future * 0.2 +
                oxygen_future * 0.2 +
                water_future * 0.1
            )
            predictions.append(round(max(0, predicted_index), 1))
        
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
            "estimated_survival_days": estimated_survival_days,
            "logs": event_log
        }
    
    def adjust_parameters(self, adjustments):
        """手动调整系统参数（用户自定义输入）"""
        state, logs = get_persistent_state()
        
        # 可调整的参数列表
        valid_params = [
            'food_stability', 'energy_level', 'medical_safety', 'oxygen_level',
            'protein_level', 'water_reserve', 'humidity', 'pressure',
            'backup_power_hours', 'co2_level', 'radiation_level'
        ]
        
        adjusted = []
        for key, value in adjustments.items():
            if key in valid_params:
                try:
                    old_value = state.get(key, 0)
                    state[key] = float(value)
                    adjusted.append(f"{key}: {old_value:.1f} -> {value:.1f}")
                except (ValueError, TypeError):
                    pass
        
        if adjusted:
            # 记录日志
            log_entry = {
                'timestamp': datetime.datetime.utcnow().isoformat(),
                'log_type': 'INFO',
                'message': f'用户手动调整参数: {", ".join(adjusted)}',
                'ai_decision': 'AI已接受用户输入并重新计算系统状态'
            }
            logs.insert(0, log_entry)
            
            # 重新计算相关指标
            state['base_stability'] = (state['energy_level'] + state['food_stability'] + state['medical_safety']) / 3
            state['environment_score'] = (state['oxygen_level'] + state['humidity'] * 2 + state['pressure']) / 3
            state['survival_index'] = (
                state['food_stability'] * 0.2 +
                state['medical_safety'] * 0.3 +
                state['energy_level'] * 0.2 +
                state['oxygen_level'] * 0.2 +
                state['water_reserve'] * 0.1
            )
        
        return {
            'success': True,
            'adjusted': adjusted,
            'new_status': self.get_current_status()
        }
    
    # ==================== 食物资源管理 ====================
    
    def add_food_item(self, item_data):
        """添加食物到库存"""
        state, logs = get_persistent_state()
        
        new_item = {
            'id': len(state['food_inventory']) + 1,
            'name': item_data.get('name', '未知食物'),
            'quantity': float(item_data.get('quantity', 0)),
            'expiry_date': item_data.get('expiry_date', ''),
            'nutrition_type': item_data.get('nutrition_type', 'protein'),  # protein/carb/fat/vitamin
            'added_date': datetime.datetime.utcnow().isoformat(),
            'status': 'normal'
        }
        
        state['food_inventory'].append(new_item)
        
        # 更新食物稳定性（增量更新，避免覆盖原有衰减）
        added_quantity = new_item['quantity']
        stability_increase = added_quantity / 10.0  # 每10单位=1%稳定性
        state['food_stability'] = min(100, state['food_stability'] + stability_increase)
        
        log_entry = {
            'timestamp': datetime.datetime.utcnow().isoformat(),
            'log_type': 'INFO',
            'message': f'添加食物: {new_item["name"]} x{new_item["quantity"]}',
            'ai_decision': 'AI已更新食物库存并重新计算预测'
        }
        logs.insert(0, log_entry)
        
        return {'success': True, 'item': new_item, 'updated_status': self.get_current_status()}
    
    def remove_food_item(self, item_id, reason=''):
        """移除食物"""
        state, logs = get_persistent_state()
        
        removed = None
        remaining = []
        for item in state['food_inventory']:
            if item['id'] == item_id:
                removed = item
            else:
                remaining.append(item)
        
        if removed:
            state['food_inventory'] = remaining
            
            # 重新计算食物稳定性（基于剩余库存）
            total_quantity = sum(item['quantity'] for item in remaining)
            state['food_stability'] = min(100, total_quantity / 10.0)
            
            log_entry = {
                'timestamp': datetime.datetime.utcnow().isoformat(),
                'log_type': 'WARNING',
                'message': f'移除食物: {removed["name"]} (原因: {reason})',
                'ai_decision': 'AI已记录食物消耗并更新稳定性'
            }
            logs.insert(0, log_entry)
            return {'success': True, 'removed': removed}
        
        return {'success': False, 'error': '物品不存在'}
    
    def update_consumption_rate(self, rate, activity_level='normal'):
        """更新消耗速率"""
        state, _ = get_persistent_state()
        state['consumption_rate'] = float(rate)
        state['prediction_params']['activity_level'] = activity_level
        return {'success': True, 'new_rate': rate}
    
    def toggle_emergency_ration(self, enabled, percentage=100):
        """切换紧急配给模式"""
        state, logs = get_persistent_state()
        state['emergency_ration_mode'] = enabled
        state['ration_percentage'] = int(percentage)
        
        mode_text = '启用' if enabled else '关闭'
        log_entry = {
            'timestamp': datetime.datetime.utcnow().isoformat(),
            'log_type': 'WARNING' if enabled else 'INFO',
            'message': f'{mode_text}紧急配给模式 (配给率: {percentage}%)',
            'ai_decision': 'AI已调整配给策略'
        }
        logs.insert(0, log_entry)
        
        return {'success': True, 'mode': enabled, 'percentage': percentage}
    
    # ==================== 医疗冷链管理 ====================
    
    def add_medical_item(self, item_data):
        """添加医疗物品"""
        state, logs = get_persistent_state()
        
        new_item = {
            'id': len(state['medical_items']) + 1,
            'type': item_data.get('type', 'medicine'),  # vaccine/medicine/sample
            'name': item_data.get('name', '未知物品'),
            'quantity': float(item_data.get('quantity', 0)),
            'storage_temp': float(item_data.get('storage_temp', -70)),
            'urgency': item_data.get('urgency', 'normal'),  # low/normal/high/critical
            'added_date': datetime.datetime.utcnow().isoformat()
        }
        
        state['medical_items'].append(new_item)
        
        # 更新医疗安全性（增量更新，避免覆盖原有衰减）
        added_quantity = new_item['quantity']
        safety_increase = added_quantity / 5.0  # 每5单位=1%安全性
        state['medical_safety'] = min(100, state['medical_safety'] + safety_increase)
        
        log_entry = {
            'timestamp': datetime.datetime.utcnow().isoformat(),
            'log_type': 'INFO',
            'message': f'添加医疗物品: {new_item["name"]} ({new_item["type"]})',
            'ai_decision': 'AI已更新医疗库存并重新计算系统状态和预测'
        }
        logs.insert(0, log_entry)
        
        return {'success': True, 'item': new_item, 'updated_status': self.get_current_status()}
    
    def remove_medical_item(self, item_id, reason=''):
        """移除医疗物品"""
        state, logs = get_persistent_state()
        
        removed = None
        remaining = []
        for item in state['medical_items']:
            if item['id'] == item_id:
                removed = item
            else:
                remaining.append(item)
        
        if removed:
            state['medical_items'] = remaining
            
            # 重新计算医疗安全性（基于剩余库存）
            total_quantity = sum(item['quantity'] for item in remaining)
            state['medical_safety'] = min(100, total_quantity / 5.0)
            
            log_entry = {
                'timestamp': datetime.datetime.utcnow().isoformat(),
                'log_type': 'WARNING',
                'message': f'移除医疗物品: {removed["name"]} (原因: {reason})',
                'ai_decision': 'AI已更新医疗库存'
            }
            logs.insert(0, log_entry)
            return {'success': True, 'removed': removed}
        
        return {'success': False, 'error': '物品不存在'}
    
    def update_medical_temp_range(self, min_temp, max_temp):
        """更新医疗温度范围"""
        state, _ = get_persistent_state()
        state['medical_temp_range'] = {'min': float(min_temp), 'max': float(max_temp)}
        return {'success': True, 'range': state['medical_temp_range']}
    
    def set_medical_priority(self, priority_level):
        """设置医疗优先级"""
        state, _ = get_persistent_state()
        state['medical_priority_level'] = priority_level
        return {'success': True, 'priority': priority_level}
    
    # ==================== 能源管理 ====================
    
    def update_energy_distribution(self, distribution):
        """更新能源分配比例"""
        state, logs = get_persistent_state()
        
        # 验证总和是否为100
        total = sum(distribution.values())
        if abs(total - 100) > 0.1:
            return {'success': False, 'error': f'分配比例总和必须为100%，当前为{total}%'}
        
        state['energy_distribution'] = distribution
        
        # 不再直接修改energy_level，避免累积效应
        # energy_level的衰减由simulate_step()统一处理
        # 这里只记录分配比例，供simulate_step参考
        
        medical_alloc = distribution.get('medical', 30)
        food_alloc = distribution.get('food', 25)
        env_alloc = distribution.get('environment', 25)
        other_alloc = distribution.get('other', 20)
        
        log_entry = {
            'timestamp': datetime.datetime.utcnow().isoformat(),
            'log_type': 'INFO',
            'message': f'更新能源分配: 医疗{medical_alloc}%, 食物{food_alloc}%, 环境{env_alloc}%, 其他{other_alloc}%',
            'ai_decision': 'AI已记录新的能源分配策略'
        }
        logs.insert(0, log_entry)
        
        return {'success': True, 'distribution': distribution, 'updated_status': self.get_current_status()}
    
    def set_energy_saving_mode(self, mode):
        """设置节能模式"""
        state, logs = get_persistent_state()
        valid_modes = ['normal', 'moderate', 'aggressive', 'critical']
        if mode not in valid_modes:
            return {'success': False, 'error': f'无效模式，可选: {valid_modes}'}
        
        state['energy_saving_mode'] = mode
        
        log_entry = {
            'timestamp': datetime.datetime.utcnow().isoformat(),
            'log_type': 'INFO',
            'message': f'切换节能模式: {mode}',
            'ai_decision': 'AI已调整能源策略'
        }
        logs.insert(0, log_entry)
        
        return {'success': True, 'mode': mode}
    
    # ==================== 环境控制 ====================
    
    def update_env_targets(self, targets):
        """更新环境目标值"""
        state, logs = get_persistent_state()
        
        # 更新环境目标
        old_targets = state['env_targets'].copy()
        state['env_targets'].update(targets)
        
        # 如果更新了氧气、温度或湿度，重新计算环境分数
        if any(key in targets for key in ['oxygen', 'temperature', 'humidity']):
            state['environment_score'] = (
                state['oxygen_level'] + 
                state['humidity'] * 2 + 
                state['pressure']
            ) / 3
            
            log_entry = {
                'timestamp': datetime.datetime.utcnow().isoformat(),
                'log_type': 'INFO',
                'message': f'更新环境目标: {targets}',
                'ai_decision': 'AI已根据新的环境目标重新计算系统状态和预测'
            }
            logs.insert(0, log_entry)
            
            return {'success': True, 'targets': state['env_targets'], 'updated_status': self.get_current_status()}
        
        return {'success': True, 'targets': state['env_targets']}
    
    def update_env_alerts(self, alerts):
        """更新环境警报阈值"""
        state, _ = get_persistent_state()
        state['env_alerts'].update(alerts)
        return {'success': True, 'alerts': state['env_alerts']}
    
    def set_ventilation_mode(self, mode, cycle_time=30):
        """设置通风模式"""
        state, _ = get_persistent_state()
        state['ventilation_mode'] = mode  # auto/manual
        state['ventilation_cycle'] = int(cycle_time)
        return {'success': True, 'mode': mode, 'cycle': cycle_time}
    
    # ==================== AI预测与决策 ====================
    
    def update_prediction_params(self, params):
        """更新预测参数"""
        state, _ = get_persistent_state()
        state['prediction_params'].update(params)
        return {'success': True, 'params': state['prediction_params']}
    
    def set_ai_automation_level(self, level):
        """设置AI自动化级别"""
        state, logs = get_persistent_state()
        valid_levels = ['manual', 'semi-auto', 'full-auto']
        if level not in valid_levels:
            return {'success': False, 'error': f'无效级别，可选: {valid_levels}'}
        
        state['ai_automation_level'] = level
        
        log_entry = {
            'timestamp': datetime.datetime.utcnow().isoformat(),
            'log_type': 'INFO',
            'message': f'AI自动化级别设置为: {level}',
            'ai_decision': 'AI控制权限已更新'
        }
        logs.insert(0, log_entry)
        
        return {'success': True, 'level': level}
    
    def set_ai_preferences(self, risk_tolerance, priority):
        """设置AI偏好"""
        state, _ = get_persistent_state()
        state['ai_risk_tolerance'] = int(risk_tolerance)
        state['ai_priority_preference'] = priority
        return {'success': True, 'risk_tolerance': risk_tolerance, 'priority': priority}
    
    def update_food_warnings(self, expiry_days, min_stock):
        """更新食物预警设置"""
        state, logs = get_persistent_state()
        state['food_expiry_warning_days'] = int(expiry_days)
        state['food_min_stock_warning'] = int(min_stock)
        return {'success': True}
    
    def update_food_zones(self, zone1, zone2, zone3):
        """更新食物温度区域"""
        state, _ = get_persistent_state()
        state['food_temperature_zones'] = {'zone1': float(zone1), 'zone2': float(zone2), 'zone3': float(zone3)}
        return {'success': True}
    
    def update_charging_strategy(self, solar_hours, backup_threshold):
        """更新充电策略"""
        state, _ = get_persistent_state()
        state['solar_charging_hours'] = int(solar_hours)
        state['backup_power_threshold'] = int(backup_threshold)
        return {'success': True}
    
    def update_low_battery_response(self, shutdown_sequence, retained_functions):
        """更新低电量响应配置"""
        state, logs = get_persistent_state()
        state['low_battery_shutdown_sequence'] = shutdown_sequence
        state['low_battery_response'] = retained_functions
        log_entry = {
            'timestamp': datetime.datetime.utcnow().isoformat(),
            'log_type': 'INFO',
            'message': f'低电量响应配置更新: 保留{retained_functions}',
            'ai_decision': 'AI已更新低电量响应策略'
        }
        logs.insert(0, log_entry)
        return {'success': True}
    
    def update_env_alerts_config(self, co2_max, oxygen_alert, temp_alert):
        """更新环境警报配置"""
        state, _ = get_persistent_state()
        state['env_alerts']['co2_max'] = float(co2_max)
        state['env_alerts']['oxygen_min'] = float(oxygen_alert)
        if temp_alert and '-' in temp_alert:
            parts = temp_alert.split('-')
            state['env_alerts']['temp_min'] = float(parts[0])
            state['env_alerts']['temp_max'] = float(parts[1])
        return {'success': True}
    
    def update_ventilation(self, mode, interval):
        """更新通风控制"""
        state, _ = get_persistent_state()
        state['ventilation_mode'] = mode
        state['ventilation_cycle'] = int(interval)
        return {'success': True}
    
    def update_emergency_response(self, leak_response, purification_priority):
        """更新应急响应方案"""
        state, logs = get_persistent_state()
        state['emergency_oxygen_leak_response'] = leak_response
        state['emergency_air_purification_priority'] = purification_priority
        log_entry = {
            'timestamp': datetime.datetime.utcnow().isoformat(),
            'log_type': 'INFO',
            'message': f'应急响应方案更新: 泄漏{leak_response}，净化{purification_priority}',
            'ai_decision': 'AI已更新应急响应方案'
        }
        logs.insert(0, log_entry)
        return {'success': True}
    
    def update_task_parameters(self, crew_count, duration, activity_level, resupply_interval):
        """更新任务参数"""
        state, logs = get_persistent_state()
        old_crew = state['crew_count']
        
        # 如果乘员数量变化，同步更新crew_members列表
        new_count = int(crew_count)
        current_count = len(state['crew_members'])
        
        if new_count > current_count:
            # 添加默认宇航员
            for i in range(current_count, new_count):
                state['crew_members'].append({
                    'id': i + 1,
                    'name': f'宇航员{chr(65 + i)}',
                    'weight': 70,
                    'age': 35,
                    'health_status': 'good',
                    'special_needs': [],
                    'calorie_needs': 2500,
                    'diet_requirements': [],
                    'allergies': []
                })
        elif new_count < current_count:
            # 移除多余宇航员
            state['crew_members'] = state['crew_members'][:new_count]
        
        state['crew_count'] = len(state['crew_members'])  # 始终与crew_members同步
        state['task_duration'] = int(duration)
        state['activity_level'] = activity_level
        state['resupply_interval'] = int(resupply_interval)
        
        if old_crew != state['crew_count']:
            log_entry = {
                'timestamp': datetime.datetime.utcnow().isoformat(),
                'log_type': 'INFO',
                'message': f'任务参数更新: {old_crew}人→{state["crew_count"]}人，任务{duration}天',
                'ai_decision': 'AI已根据乘员变化重新计算资源消耗预测'
            }
            logs.insert(0, log_entry)
        
        status = self.get_current_status()
        log_entry = {
            'timestamp': datetime.datetime.utcnow().isoformat(),
            'log_type': 'INFO',
            'message': f'任务参数已更新 | 环境: 生存指数 {status["survival_index"]:.1f}%',
            'ai_decision': 'AI已根据新参数重新计算预测'
        }
        logs.insert(0, log_entry)
        return {'success': True}
    
    def update_emergency_config(self, triggers, actions, confirmation):
        """更新紧急协议配置"""
        state, logs = get_persistent_state()
        state['emergency_triggers'].update(triggers)
        state['emergency_actions'] = actions
        state['emergency_confirmation'] = confirmation
        
        status = self.get_current_status()
        log_entry = {
            'timestamp': datetime.datetime.utcnow().isoformat(),
            'log_type': 'INFO',
            'message': f'紧急协议配置已更新 | 环境: 生存指数 {status["survival_index"]:.1f}%, 能源 {status["energy_level"]:.1f}%',
            'ai_decision': 'AI已更新紧急协议配置'
        }
        logs.insert(0, log_entry)
        return {'success': True}
    
    def run_simulation(self, scenario, severity, strategy):
        """运行场景模拟"""
        state, logs = get_persistent_state()
        
        scenario_text = {
            'oxygen-leak': '氧气泄漏',
            'power-failure': '能源故障',
            'cold-chain-break': '冷链中断',
            'hull-damage': '舱体损伤'
        }.get(scenario, scenario)
        
        # 模拟影响
        if scenario == 'oxygen-leak':
            state['oxygen_level'] = max(0, state['oxygen_level'] - float(severity) * 2)
        elif scenario == 'power-failure':
            state['energy_level'] = max(0, state['energy_level'] - float(severity) * 3)
        elif scenario == 'cold-chain-break':
            state['medical_safety'] = max(0, state['medical_safety'] - float(severity) * 2)
        elif scenario == 'hull-damage':
            state['pressure'] = max(80, state['pressure'] - float(severity) * 1)
            state['survival_index'] -= float(severity)
        
        status = self.get_current_status()
        log_entry = {
            'timestamp': datetime.datetime.utcnow().isoformat(),
            'log_type': 'WARNING',
            'message': f'模拟运行: {scenario_text} (严重程度{severity}) | 环境: 生存指数 {status["survival_index"]:.1f}%, 氧气 {status["oxygen_level"]:.1f}%',
            'ai_decision': f'AI已执行{strategy}策略模拟'
        }
        logs.insert(0, log_entry)
        return {'success': True, 'status': status}
    
    def update_system_settings(self, refresh_rate, display_mode):
        """更新系统设置"""
        state, logs = get_persistent_state()
        state['display_settings']['refresh_rate'] = int(refresh_rate)
        state['display_settings']['chart_options'] = display_mode
        
        status = self.get_current_status()
        log_entry = {
            'timestamp': datetime.datetime.utcnow().isoformat(),
            'log_type': 'INFO',
            'message': f'系统设置已更新 | 环境: 生存指数 {status["survival_index"]:.1f}%',
            'ai_decision': 'AI已应用新的系统配置'
        }
        logs.insert(0, log_entry)
        return {'success': True}
    
    def update_nutrition_settings(self, calories, diet, allergies):
        """更新营养需求设置"""
        state, _ = get_persistent_state()
        state['daily_calorie_needs'] = int(calories)
        state['diet_requirements'] = diet
        state['crew_allergies'] = allergies
        return {'success': True}
    
    def update_activity_schedule(self, schedule, rest_hours, activity_adjustment):
        """更新活动日程安排"""
        state, logs = get_persistent_state()
        state['daily_schedule'] = schedule
        state['rest_hours'] = float(rest_hours)
        state['activity_adjustment'] = activity_adjustment
        log_entry = {
            'timestamp': datetime.datetime.utcnow().isoformat(),
            'log_type': 'INFO',
            'message': f'日程安排更新: 休息{rest_hours}小时，{activity_adjustment}模式',
            'ai_decision': 'AI已更新活动日程并调整资源消耗预测'
        }
        logs.insert(0, log_entry)
        return {'success': True}
    
    # ==================== 紧急协议 ====================
    
    def configure_emergency_protocol(self, protocol_data):
        """配置紧急协议"""
        state, logs = get_persistent_state()
        
        protocol = {
            'id': len(state['emergency_protocols']) + 1,
            'name': protocol_data.get('name', '未命名协议'),
            'trigger_conditions': protocol_data.get('triggers', {}),
            'actions': protocol_data.get('actions', []),
            'delay_seconds': int(protocol_data.get('delay', 0)),
            'enabled': True
        }
        
        state['emergency_protocols'].append(protocol)
        
        log_entry = {
            'timestamp': datetime.datetime.utcnow().isoformat(),
            'log_type': 'INFO',
            'message': f'配置紧急协议: {protocol["name"]}',
            'ai_decision': 'AI已注册新协议'
        }
        logs.insert(0, log_entry)
        
        return {'success': True, 'protocol': protocol}
    
    def trigger_emergency_manual(self, level='warning'):
        """手动触发紧急协议"""
        state, logs = get_persistent_state()
        
        log_entry = {
            'timestamp': datetime.datetime.utcnow().isoformat(),
            'log_type': 'CRITICAL',
            'message': f'⚠️ 手动触发紧急协议 (等级: {level})',
            'ai_decision': 'AI正在执行紧急响应流程'
        }
        logs.insert(0, log_entry)
        
        # 根据等级调整状态
        if level == 'critical':
            state['survival_index'] = max(0, state['survival_index'] - 20)
            state['energy_level'] = max(0, state['energy_level'] - 15)
        elif level == 'warning':
            state['survival_index'] = max(0, state['survival_index'] - 10)
        
        return {
            'success': True,
            'level': level,
            'new_status': self.get_current_status()
        }
    
    # ==================== 宇航员管理 ====================
    
    def add_crew_member(self, member_data):
        """添加宇航员"""
        state, logs = get_persistent_state()
        
        new_member = {
            'id': len(state['crew_members']) + 1,
            'name': member_data.get('name', '未知'),
            'weight': float(member_data.get('weight', 70)),
            'age': int(member_data.get('age', 30)),
            'health_status': member_data.get('health_status', 'good'),
            'special_needs': member_data.get('special_needs', []),
            'calorie_needs': int(member_data.get('calorie_needs', 2500)),
            'diet_requirements': member_data.get('diet_requirements', []),
            'allergies': member_data.get('allergies', [])
        }
        
        state['crew_members'].append(new_member)
        state['crew_count'] = len(state['crew_members'])
        
        # 乘员数量影响资源消耗率，重新计算预计生存天数
        crew_count = state['crew_count']
        food_consumption_rate = 2.0 * crew_count / 4.0
        water_consumption_rate = 1.5 * crew_count / 4.0
        
        log_entry = {
            'timestamp': datetime.datetime.utcnow().isoformat(),
            'log_type': 'INFO',
            'message': f'添加宇航员: {new_member["name"]} (当前乘员数: {crew_count})',
            'ai_decision': f'AI已更新人员配置并重新计算资源消耗预测 (食物消耗率: {food_consumption_rate:.2f}/天, 水消耗率: {water_consumption_rate:.2f}/天)'
        }
        logs.insert(0, log_entry)
        
        return {'success': True, 'member': new_member, 'updated_status': self.get_current_status()}
    
    def remove_crew_member(self, member_id):
        """移除宇航员"""
        state, logs = get_persistent_state()
        
        removed = None
        remaining = []
        for member in state['crew_members']:
            if member['id'] == member_id:
                removed = member
            else:
                remaining.append(member)
        
        if removed:
            state['crew_members'] = remaining
            state['crew_count'] = len(remaining)
            
            log_entry = {
                'timestamp': datetime.datetime.utcnow().isoformat(),
                'log_type': 'WARNING',
                'message': f'移除宇航员: {removed["name"]}',
                'ai_decision': 'AI已更新人员配置'
            }
            logs.insert(0, log_entry)
            
            return {'success': True, 'removed': removed}
        
        return {'success': False, 'error': '宇航员不存在'}
    
    # ==================== 通信与日志 ====================
    
    def add_manual_log(self, log_data):
        """添加手动日志"""
        state, _ = get_persistent_state()
        
        new_log = {
            'id': len(state['manual_logs']) + 1,
            'timestamp': datetime.datetime.utcnow().isoformat(),
            'type': log_data.get('type', 'observation'),  # event/observation/anomaly
            'content': log_data.get('content', ''),
            'author': log_data.get('author', '系统')
        }
        
        state['manual_logs'].insert(0, new_log)
        
        return {'success': True, 'log': new_log}
    
    def generate_custom_report(self, report_type='daily', depth='standard', focus_areas=None):
        """生成自定义报告"""
        state, _ = get_persistent_state()
        
        if focus_areas is None:
            focus_areas = ['survival', 'resources']
        
        status = self.get_current_status()
        
        report = f"=== {report_type.upper()} REPORT ===\n"
        report += f"生成时间: {datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}\n"
        report += f"深度: {depth}\n\n"
        
        if 'survival' in focus_areas:
            report += f"生存指数: {status['survival_index']:.1f}%\n"
            report += f"预计生存天数: {status['estimated_survival_days']}天\n"
            report += f"任务天数: {status['mission_day']}\n\n"
        
        if 'resources' in focus_areas:
            report += f"食物稳定性: {status['food_stability']:.1f}%\n"
            report += f"能源水平: {status['energy_level']:.1f}%\n"
            report += f"医疗安全性: {status['medical_safety']:.1f}%\n"
            report += f"氧气水平: {status['oxygen_level']:.1f}%\n\n"
        
        if 'crew' in focus_areas:
            report += f"宇航员人数: {status['crew_count']}\n"
            report += f"人员列表: {', '.join([m['name'] for m in state['crew_members']])}\n\n"
        
        return {'success': True, 'report': report}

# 全局实例
engine = AISurvivalEngine()
