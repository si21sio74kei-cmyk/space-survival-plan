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
from services.ai_engine import engine as ai_engine

app = Flask(__name__, 
            template_folder='frontend',
            static_folder='frontend',
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

# ==================== 本地运行 ====================

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
