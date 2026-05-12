"""
深空AI生存系统 - Flask一体化版本（Vercel兼容）
参考: https://github.com/si21sio74kei-cmyk/food-ai-v3
"""
import sys
import os
from flask import Flask, render_template, jsonify, request
from datetime import datetime

# 添加当前目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# 导入AI引擎
from ai_engine import engine as ai_engine

app = Flask(__name__, 
            template_folder='templates',
            static_folder='templates',
            static_url_path='')

# Vercel Serverless架构：每次请求时自动执行模拟
@app.before_request
def auto_simulate():
    """每次API请求前自动执行系统模拟（Vercel兼容）"""
    if request.path.startswith('/api/'):
        try:
            ai_engine.simulate_step()
        except Exception as e:
            print(f"Auto-simulate error: {e}")

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
        "estimated_survival_days": status['estimated_survival_days']
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
def add_food():
    """添加食物"""
    data = request.get_json() or {}
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

# ==================== 医疗冷链管理 API ====================

@app.route('/api/medical/add', methods=['POST'])
def add_medical():
    """添加医疗物品"""
    data = request.get_json() or {}
    result = ai_engine.add_medical_item(data)
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

# ==================== 紧急协议 API ====================

@app.route('/api/emergency/configure', methods=['POST'])
def configure_emergency():
    """配置紧急协议"""
    data = request.get_json() or {}
    result = ai_engine.configure_emergency_protocol(data)
    return jsonify(result)

@app.route('/api/emergency/trigger-manual', methods=['POST'])
def trigger_emergency_manual():
    """手动触发紧急协议"""
    data = request.get_json() or {}
    level = data.get('level', 'warning')
    result = ai_engine.trigger_emergency_manual(level)
    return jsonify(result)

# ==================== 宇航员管理 API ====================

@app.route('/api/crew/add', methods=['POST'])
def add_crew():
    """添加宇航员"""
    data = request.get_json() or {}
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
    state, _ = ai_engine.__class__.__bases__[0].__dict__.get('get_persistent_state', lambda: ([], []))()
    # 简化处理，直接返回状态中的crew_members
    from ai_engine import get_persistent_state
    state, _ = get_persistent_state()
    return jsonify(state['crew_members'])

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

# ==================== 本地运行 ====================

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
