"""
深空AI生存系统 - Flask一体化版本（Vercel兼容）
参考: https://github.com/si21sio74kei-cmyk/food-ai-v3
"""
import sys
import os
from flask import Flask, render_template, jsonify, request
from datetime import datetime
from functools import wraps
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv

# 加载.env文件
load_dotenv()

# 添加当前目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# 导入AI引擎
from ai_engine import engine as ai_engine

# 导入太空数据API
try:
    from backend.space_data_api import space_api
    SPACE_API_AVAILABLE = True
except ImportError:
    SPACE_API_AVAILABLE = False
    print("警告: space_data_api模块未找到，太空数据功能将不可用")

app = Flask(__name__, 
            template_folder='templates',
            static_folder='templates',
            static_url_path='')

# ==================== 速率限制配置 ====================
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

# ==================== 输入验证装饰器 ====================

def validate_json(*required_fields):
    """验证JSON请求是否包含必需字段"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            data = request.get_json()
            if not data:  # 处理 None 和 {}
                return jsonify({'success': False, 'error': '请求必须包含JSON数据'}), 400
            
            missing = [field for field in required_fields if field not in data]
            if missing:
                return jsonify({'success': False, 'error': f'缺少必需字段: {", ".join(missing)}'}), 400
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def validate_range(field_name, min_val=None, max_val=None):
    """验证数值字段范围"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            data = request.get_json() or {}
            value = data.get(field_name)
            
            if value is not None:
                try:
                    value = float(value)
                    if min_val is not None and value < min_val:
                        return jsonify({'success': False, 'error': f'{field_name}不能小于{min_val}'}), 400
                    if max_val is not None and value > max_val:
                        return jsonify({'success': False, 'error': f'{field_name}不能大于{max_val}'}), 400
                except (ValueError, TypeError):
                    return jsonify({'success': False, 'error': f'{field_name}必须是有效数字'}), 400
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Vercel Serverless架构：每次请求时自动执行模拟
# ★★★ 已移除 @app.before_request 自动模拟，避免每次访问页面都调用AI消耗Token ★★★
# 现在只保留前端定时调用（每分钟1次）

# ==================== 页面路由 ====================

@app.route('/')
def index():
    """主页"""
    return render_template('index.html')

# ==================== API路由 ====================

@app.route('/api/survival-status')
def get_survival_status():
    """获取生存状态"""
    status = ai_engine.get_current_status()
    
    return jsonify({
        "mission_day": status['mission_day'],
        "survival_index": round(status['survival_index'], 1),
        "crew_count": status['crew_count'],
        "food_stability": round(status['food_stability'], 1),
        "energy_level": round(status['energy_level'], 1),
        "medical_safety": round(status['medical_safety'], 1),
        "environment_score": round(status['environment_score'], 1),
        "base_stability": round(status['base_stability'], 1),
        "estimated_survival_days": status['estimated_survival_days'],
        # 添加前端图表所需的额外字段
        "water_reserve": round(status['water_reserve'], 1),
        "oxygen_level": round(status['oxygen_level'], 1),
        "protein_level": round(status['protein_level'], 1),
        "humidity": round(status['humidity'], 1),
        "pressure": round(status['pressure'], 1),
        "temperature": round(status.get('temperature', 22.0), 1),
        "radiation_level": round(status['radiation_level'], 1),
        "backup_power_hours": round(status['backup_power_hours'], 1),
        "emergency_mode": status.get('emergency_mode', False),
        "predictions": status.get('predictions', [70, 60, 50, 40]),
        "diet_advice": status.get('diet_advice', '标准配给')
    })

@app.route('/api/food-inventory')
def get_food_inventory():
    """获取食物库存"""
    inventory = ai_engine.get_food_inventory()
    return jsonify(inventory)

@app.route('/api/medical-status')
def get_medical_status():
    """获取医疗状态"""
    medical = ai_engine.get_medical_status()
    return jsonify(medical)

@app.route('/api/energy-status')
def get_energy_status():
    """获取能源状态"""
    energy = ai_engine.get_energy_status()
    return jsonify(energy)

@app.route('/api/environment-status')
def get_environment_status():
    """获取环境状态"""
    env = ai_engine.get_environment_status()
    return jsonify(env)

@app.route('/api/ai-logs')
def get_ai_logs():
    """获取AI日志"""
    logs = ai_engine.get_recent_logs(limit=20)
    return jsonify(logs)

@app.route('/api/generate-report', methods=['POST'])
def generate_report():
    """生成AI报告"""
    data = request.get_json() or {}
    report_type = data.get('type', 'daily')
    report = ai_engine.generate_report(report_type)
    return jsonify(report)

@app.route('/api/emergency-protocol', methods=['POST'])
def emergency_protocol():
    """触发紧急协议"""
    data = request.get_json() or {}
    level = data.get('level', 'warning')
    result = ai_engine.trigger_emergency(level)
    return jsonify(result)

@app.route('/api/adjust-parameters', methods=['POST'])
def adjust_parameters():
    """手动调整系统参数（用户自定义输入）"""
    data = request.get_json() or {}
    result = ai_engine.adjust_parameters(data)
    return jsonify(result)

# ==================== 食物资源管理 API ====================

@app.route('/api/food/add', methods=['POST'])
@validate_json('name', 'quantity')
@validate_range('quantity', min_val=0)
def add_food():
    """添加食物"""
    data = request.get_json()
    result = ai_engine.add_food_item(data)
    return jsonify(result)

@app.route('/api/food/remove/<int:item_id>', methods=['POST'])
def remove_food(item_id):
    """移除食物"""
    data = request.get_json() or {}
    reason = data.get('reason', '')
    result = ai_engine.remove_food_item(item_id, reason)
    return jsonify(result)

@app.route('/api/food/consumption', methods=['POST'])
def update_consumption():
    """更新消耗速率"""
    data = request.get_json() or {}
    rate = data.get('rate', 1.0)
    activity_level = data.get('activity_level', 'normal')
    result = ai_engine.update_consumption_rate(rate, activity_level)
    return jsonify(result)

@app.route('/api/food/emergency-ration', methods=['POST'])
def toggle_emergency_ration():
    """切换紧急配给模式"""
    data = request.get_json() or {}
    enabled = data.get('enabled', False)
    percentage = data.get('percentage', 100)
    result = ai_engine.toggle_emergency_ration(enabled, percentage)
    return jsonify(result)

@app.route('/api/food/warnings', methods=['POST'])
def update_food_warnings_api():
    """更新食物预警设置"""
    data = request.get_json() or {}
    result = ai_engine.update_food_warnings(data.get('expiry_days', 7), data.get('min_stock', 20))
    return jsonify(result)

@app.route('/api/food/zones', methods=['POST'])
def update_food_zones_api():
    """更新食物温度区域"""
    data = request.get_json() or {}
    result = ai_engine.update_food_zones(
        data.get('zone1', -18), data.get('zone2', 4), data.get('zone3', -70)
    )
    return jsonify(result)

# ==================== 医疗冷链管理 API ====================

@app.route('/api/medical')
def get_medical_items():
    """获取医疗物品列表"""
    status = ai_engine.get_current_status()
    return jsonify({
        'medical_items': status.get('medical_items', []),
        'medical_safety': status.get('medical_safety', 100),
        'medical_temp_range': status.get('medical_temp_range', {'min': -80, 'max': -60}),
        'medical_priority_level': status.get('medical_priority_level', 'high')
    })

@app.route('/api/medical/add', methods=['POST'])
@validate_json('name', 'quantity')
@validate_range('quantity', min_val=0)
def add_medical():
    """添加医疗物品"""
    data = request.get_json()
    result = ai_engine.add_medical_item(data)
    return jsonify(result)

@app.route('/api/medical/remove/<int:item_id>', methods=['POST'])
def remove_medical(item_id):
    """移除医疗物品"""
    data = request.get_json() or {}
    reason = data.get('reason', '手动移除')
    result = ai_engine.remove_medical_item(item_id, reason)
    return jsonify(result)

@app.route('/api/medical/temp-range', methods=['POST'])
def update_medical_temp():
    """更新医疗温度范围"""
    data = request.get_json() or {}
    min_temp = data.get('min', -80)
    max_temp = data.get('max', -60)
    result = ai_engine.update_medical_temp_range(min_temp, max_temp)
    return jsonify(result)

@app.route('/api/medical/priority', methods=['POST'])
def set_medical_priority():
    """设置医疗优先级"""
    data = request.get_json() or {}
    priority = data.get('priority', 'high')
    result = ai_engine.set_medical_priority(priority)
    return jsonify(result)

# ==================== 能源管理 API ====================

@app.route('/api/energy/distribution', methods=['POST'])
def update_energy_dist():
    """更新能源分配"""
    data = request.get_json() or {}
    result = ai_engine.update_energy_distribution(data)
    return jsonify(result)

@app.route('/api/energy/saving-mode', methods=['POST'])
def set_energy_saving():
    """设置节能模式"""
    data = request.get_json() or {}
    mode = data.get('mode', 'normal')
    result = ai_engine.set_energy_saving_mode(mode)
    return jsonify(result)

@app.route('/api/energy/charging-strategy', methods=['POST'])
def update_charging_strategy_api():
    """更新充电策略"""
    data = request.get_json() or {}
    result = ai_engine.update_charging_strategy(
        data.get('solar_hours', 8), data.get('backup_threshold', 30)
    )
    return jsonify(result)

@app.route('/api/energy/low-battery-response', methods=['POST'])
def update_low_battery_response_api():
    """更新低电量响应配置"""
    data = request.get_json() or {}
    result = ai_engine.update_low_battery_response(
        data.get('shutdown_sequence', ''), data.get('retained_functions', [])
    )
    return jsonify(result)

# ==================== 环境控制 API ====================

@app.route('/api/environment/targets', methods=['POST'])
def update_env_targets():
    """更新环境目标值"""
    data = request.get_json() or {}
    result = ai_engine.update_env_targets(data)
    return jsonify(result)

@app.route('/api/environment/alerts', methods=['POST'])
def update_env_alerts():
    """更新环境警报阈值"""
    data = request.get_json() or {}
    result = ai_engine.update_env_alerts(data)
    return jsonify(result)

@app.route('/api/environment/ventilation', methods=['POST'])
def set_ventilation():
    """设置通风模式"""
    data = request.get_json() or {}
    mode = data.get('mode', 'auto')
    cycle = data.get('cycle', 30)
    result = ai_engine.set_ventilation_mode(mode, cycle)
    return jsonify(result)

@app.route('/api/environment/alerts-config', methods=['POST'])
def update_env_alerts_config_api():
    """更新环境警报配置"""
    data = request.get_json() or {}
    result = ai_engine.update_env_alerts_config(
        data.get('co2_max', 0.5), data.get('oxygen_alert', 19.5), data.get('temp_alert', '')
    )
    return jsonify(result)

@app.route('/api/environment/ventilation-config', methods=['POST'])
def update_ventilation_config_api():
    """更新通风控制配置"""
    data = request.get_json() or {}
    result = ai_engine.update_ventilation(
        data.get('mode', 'auto'), data.get('interval', 30)
    )
    return jsonify(result)

@app.route('/api/environment/emergency-response', methods=['POST'])
def update_emergency_response_api():
    """更新应急响应方案"""
    data = request.get_json() or {}
    result = ai_engine.update_emergency_response(
        data.get('leak_response', 'isolate'), data.get('purification_priority', 'co2')
    )
    return jsonify(result)

# ==================== AI预测与决策 API ====================

@app.route('/api/ai/prediction-params', methods=['POST'])
def update_prediction_params():
    """更新预测参数"""
    data = request.get_json() or {}
    result = ai_engine.update_prediction_params(data)
    return jsonify(result)

@app.route('/api/ai/automation-level', methods=['POST'])
def set_ai_automation():
    """设置AI自动化级别"""
    data = request.get_json() or {}
    level = data.get('level', 'semi-auto')
    result = ai_engine.set_ai_automation_level(level)
    return jsonify(result)

@app.route('/api/ai/preferences', methods=['POST'])
def set_ai_prefs():
    """设置AI偏好"""
    data = request.get_json() or {}
    risk_tolerance = data.get('risk_tolerance', 50)
    priority = data.get('priority', 'survival')
    result = ai_engine.set_ai_preferences(risk_tolerance, priority)
    return jsonify(result)

@app.route('/api/ai/task-parameters', methods=['POST'])
def update_task_parameters_api():
    """更新任务参数"""
    data = request.get_json() or {}
    result = ai_engine.update_task_parameters(
        data.get('crew_count', 4), data.get('duration', 365),
        data.get('activity_level', 'normal'), data.get('resupply_interval', 90)
    )
    return jsonify(result)

# ==================== 紧急协议 API ====================

@app.route('/api/emergency/configure', methods=['POST'])
def configure_emergency():
    """配置紧急协议"""
    data = request.get_json() or {}
    result = ai_engine.configure_emergency_protocol(data)
    return jsonify(result)

@app.route('/api/emergency/trigger-manual', methods=['POST'])
@limiter.limit("10 per minute")  # 紧急协议限制每分钟10次
def trigger_emergency_manual():
    """手动触发紧急协议"""
    data = request.get_json() or {}
    level = data.get('level', 'warning')
    result = ai_engine.trigger_emergency_manual(level)
    return jsonify(result)

@app.route('/api/emergency/simulate', methods=['POST'])
def simulate_emergency_scenario():
    """模拟灾难场景"""
    data = request.get_json() or {}
    scenario = data.get('scenario', 'oxygen-leak')
    severity = data.get('severity', 5)
    strategy = data.get('strategy', 'survival-first')
    result = ai_engine.run_simulation(scenario, severity, strategy)
    return jsonify(result)

@app.route('/api/simulate_step', methods=['POST'])
@limiter.limit("30 per minute")  # 模拟步骤限制每分钟30次
def manual_simulate_step():
    """手动触发模拟步骤（用于前端定时调用）"""
    try:
        result = ai_engine.simulate_step()
        # simulate_step() 返回的就是最新状态
        return jsonify({
            'success': True,
            'state': result,
            'message': f'Day {result["mission_day"]} simulation completed'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/system/settings', methods=['POST'])
def update_system_settings_api():
    """更新系统设置"""
    data = request.get_json() or {}
    refresh_rate = data.get('refresh_rate', 3)
    display_mode = data.get('display_mode', 'detailed')
    result = ai_engine.update_system_settings(refresh_rate, display_mode)
    return jsonify(result)

# ==================== 宇航员管理 API ====================

@app.route('/api/crew/add', methods=['POST'])
@validate_json('name')
@validate_range('weight', min_val=30, max_val=150)
@validate_range('age', min_val=18, max_val=65)
def add_crew():
    """添加宇航员"""
    data = request.get_json()
    result = ai_engine.add_crew_member(data)
    return jsonify(result)

@app.route('/api/crew/remove/<int:member_id>', methods=['POST'])
def remove_crew(member_id):
    """移除宇航员"""
    result = ai_engine.remove_crew_member(member_id)
    return jsonify(result)

@app.route('/api/crew/list')
def list_crew():
    """获取宇航员列表"""
    from ai_engine import get_persistent_state
    state, _ = get_persistent_state()
    return jsonify(state['crew_members'])

@app.route('/api/crew/nutrition', methods=['POST'])
def update_nutrition_api():
    """更新营养需求设置"""
    data = request.get_json() or {}
    result = ai_engine.update_nutrition_settings(
        data.get('calories', 2500), data.get('diet', ''), data.get('allergies', '')
    )
    return jsonify(result)

@app.route('/api/crew/schedule', methods=['POST'])
def update_schedule_api():
    """更新活动日程安排"""
    data = request.get_json() or {}
    result = ai_engine.update_activity_schedule(
        data.get('schedule', ''), data.get('rest_hours', 8), data.get('activity_adjustment', 'normal')
    )
    return jsonify(result)

# ==================== 通信与日志 API ====================

@app.route('/api/logs/add', methods=['POST'])
def add_log():
    """添加手动日志"""
    data = request.get_json() or {}
    result = ai_engine.add_manual_log(data)
    return jsonify(result)

@app.route('/api/reports/custom', methods=['POST'])
def generate_custom_report():
    """生成自定义报告"""
    data = request.get_json() or {}
    report_type = data.get('type', 'daily')
    depth = data.get('depth', 'standard')
    focus_areas = data.get('focus_areas', ['survival', 'resources'])
    result = ai_engine.generate_custom_report(report_type, depth, focus_areas)
    return jsonify(result)

# ==================== 太空与地球数据 API ====================

@app.route('/api/space-weather')
def get_space_weather():
    """获取太空天气数据（第一批：太阳风暴、辐射、耀斑）"""
    if not SPACE_API_AVAILABLE:
        return jsonify({'error': '太空数据API不可用'}), 503
    
    try:
        data = space_api.get_all_space_weather()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/space-weather/summary')
def get_space_weather_summary():
    """获取太空天气摘要"""
    if not SPACE_API_AVAILABLE:
        return jsonify({'error': '太空数据API不可用'}), 503
    
    try:
        summary = space_api.get_space_weather_summary()
        return jsonify(summary)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/space-weather/storms')
def get_solar_storms():
    """获取太阳风暴数据"""
    if not SPACE_API_AVAILABLE:
        return jsonify({'error': '太空数据API不可用'}), 503
    
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    try:
        data = space_api.get_solar_storms(start_date, end_date)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/space-weather/radiation')
def get_radiation_data():
    """获取辐射数据"""
    if not SPACE_API_AVAILABLE:
        return jsonify({'error': '太空数据API不可用'}), 503
    
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    try:
        data = space_api.get_radiation_data(start_date, end_date)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/space-weather/flares')
def get_solar_flares():
    """获取太阳耀斑数据"""
    if not SPACE_API_AVAILABLE:
        return jsonify({'error': '太空数据API不可用'}), 503
    
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    try:
        data = space_api.get_solar_flares(start_date, end_date)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/situational-awareness')
def get_situational_awareness():
    """获取实时态势感知数据（第二批：ISS、宇航员、SpaceX）"""
    if not SPACE_API_AVAILABLE:
        return jsonify({'error': '太空数据API不可用'}), 503
    
    try:
        data = space_api.get_situational_awareness()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/iss/position')
def get_iss_position():
    """获取ISS实时位置"""
    if not SPACE_API_AVAILABLE:
        return jsonify({'error': '太空数据API不可用'}), 503
    
    try:
        data = space_api.get_iss_position()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/astronauts')
def get_astronauts():
    """获取当前在太空的宇航员"""
    if not SPACE_API_AVAILABLE:
        return jsonify({'error': '太空数据API不可用'}), 503
    
    try:
        data = space_api.get_astronauts_in_space()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/spacex/latest')
def get_spacex_latest():
    """获取SpaceX最新发射任务"""
    if not SPACE_API_AVAILABLE:
        return jsonify({'error': '太空数据API不可用'}), 503
    
    try:
        data = space_api.get_spacex_latest_launch()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/spacex/rockets')
def get_spacex_rockets():
    """获取SpaceX火箭数据"""
    if not SPACE_API_AVAILABLE:
        return jsonify({'error': '太空数据API不可用'}), 503
    
    try:
        data = space_api.get_spacex_rockets()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/visual-enhancement')
def get_visual_enhancement():
    """获取视觉增强数据（第三批：火星照片、地球照片、月球/行星）"""
    if not SPACE_API_AVAILABLE:
        return jsonify({'error': '太空数据API不可用'}), 503
    
    try:
        data = space_api.get_visual_enhancement_data()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/mars/photos')
def get_mars_photos():
    """获取火星车照片"""
    if not SPACE_API_AVAILABLE:
        return jsonify({'error': '太空数据API不可用'}), 503
    
    rover = request.args.get('rover', 'curiosity')
    sol = request.args.get('sol', 1000, type=int)
    camera = request.args.get('camera')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 25, type=int)
    
    try:
        data = space_api.get_mars_photos(rover, sol, camera, page, per_page)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/earth/photos')
def get_earth_photos():
    """获取NASA EPIC地球照片"""
    if not SPACE_API_AVAILABLE:
        return jsonify({'error': '太空数据API不可用'}), 503
    
    date = request.args.get('date')
    
    try:
        data = space_api.get_epic_earth_photos(date)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/moon')
def get_moon_data():
    """获取月球数据"""
    if not SPACE_API_AVAILABLE:
        return jsonify({'error': '太空数据API不可用'}), 503
    
    try:
        data = space_api.get_moon_data()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/planets')
def get_planets():
    """获取行星数据"""
    if not SPACE_API_AVAILABLE:
        return jsonify({'error': '太空数据API不可用'}), 503
    
    try:
        data = space_api.get_planets_data()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/earth-environment')
def get_earth_environment():
    """获取地球环境监控数据（第四批：灾害、地震、空气质量、天气）"""
    if not SPACE_API_AVAILABLE:
        return jsonify({'error': '太空数据API不可用'}), 503
    
    try:
        data = space_api.get_earth_environment_data()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/earth/disasters')
def get_earth_disasters():
    """获取地球自然灾害事件"""
    if not SPACE_API_AVAILABLE:
        return jsonify({'error': '太空数据API不可用'}), 503
    
    limit = request.args.get('limit', 20, type=int)
    days = request.args.get('days', 7, type=int)
    
    try:
        data = space_api.get_earth_disasters(limit, days)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/earthquakes')
def get_earthquakes():
    """获取全球地震数据"""
    if not SPACE_API_AVAILABLE:
        return jsonify({'error': '太空数据API不可用'}), 503
    
    min_magnitude = request.args.get('min_magnitude', 5.0, type=float)
    days = request.args.get('days', 7, type=int)
    
    try:
        data = space_api.get_earthquakes(min_magnitude, days)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/air-quality')
def get_air_quality():
    """获取空气质量数据"""
    if not SPACE_API_AVAILABLE:
        return jsonify({'error': '太空数据API不可用'}), 503
    
    location = request.args.get('location', 'here')
    token = request.args.get('token', 'demo')
    
    try:
        data = space_api.get_air_quality(location, token)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/weather/macau')
def get_macau_weather():
    """获取澳门天气"""
    if not SPACE_API_AVAILABLE:
        return jsonify({'error': '太空数据API不可用'}), 503
    
    try:
        data = space_api.get_macau_weather()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/space-data/health')
def check_space_data_health():
    """检查所有太空数据API的健康状态"""
    if not SPACE_API_AVAILABLE:
        return jsonify({'error': '太空数据API模块未加载'}), 503
    
    import signal
    
    def timeout_handler(signum, frame):
        raise TimeoutError("API call timed out")
    
    health_status = {}
    apis_to_check = [
        ('space_weather_summary', lambda: space_api.get_space_weather_summary()),
        ('iss_position', space_api.get_iss_position),
        ('astronauts', space_api.get_astronauts_in_space),
        ('spacex_latest', space_api.get_spacex_latest_launch),
        ('spacex_rockets', space_api.get_spacex_rockets),
        ('mars_photos', lambda: space_api.get_mars_photos(per_page=1)),
        ('epic_earth', lambda: space_api.get_epic_earth_photos()),
        ('moon_data', space_api.get_moon_data),
        ('planets_data', space_api.get_planets_data),
        ('earth_disasters', lambda: space_api.get_earth_disasters(limit=1)),
        ('earthquakes', lambda: space_api.get_earthquakes(min_magnitude=5.0, days=1)),
        ('air_quality', lambda: space_api.get_air_quality()),
        ('macau_weather', space_api.get_macau_weather),
    ]
    
    for name, func in apis_to_check:
        try:
            # Windows不支持signal.SIGALRM，使用try-except
            try:
                signal.signal(signal.SIGALRM, timeout_handler)
                signal.alarm(5)  # 5秒超时
            except (AttributeError, ValueError):
                pass  # Windows系统跳过
            
            result = func()
            
            try:
                signal.alarm(0)  # 取消超时
            except (AttributeError, ValueError):
                pass
            
            # 检查是否返回错误信息
            if isinstance(result, dict) and 'error' in result:
                health_status[name] = {
                    'status': 'error',
                    'error': result['error'],
                    'data_available': False
                }
            else:
                health_status[name] = {
                    'status': 'ok',
                    'data_available': result is not None,
                    'data_type': type(result).__name__
                }
        except TimeoutError:
            health_status[name] = {
                'status': 'timeout',
                'error': 'API调用超时（>5秒）',
                'data_available': False
            }
        except Exception as e:
            health_status[name] = {
                'status': 'error',
                'error': str(e),
                'data_available': False
            }
    
    # 统计健康状况
    total = len(health_status)
    ok_count = sum(1 for v in health_status.values() if v['status'] == 'ok')
    error_count = total - ok_count
    
    return jsonify({
        'timestamp': datetime.utcnow().isoformat(),
        'summary': {
            'total': total,
            'ok': ok_count,
            'error': error_count,
            'health_rate': f"{ok_count}/{total} ({ok_count*100//total}%)"
        },
        'apis': health_status
    })

# ==================== 本地运行 ====================

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
