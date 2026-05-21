"""
深空AI生存系统 - Phase 1 & 2 功能测试
测试内容:
1. 统一后端文件 space_survival_system.py 是否正常工作
2. AI规则决策引擎是否生效
3. 紧急模式是否正确触发
"""
import sys
import os

# 添加当前目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from ai_engine import engine as ai_engine

def test_phase1_backend():
    """测试Phase 1: 后端主文件"""
    print("=" * 60)
    print("Phase 1: 测试后端主文件")
    print("=" * 60)
    
    # 测试获取状态
    status = ai_engine.get_current_status()
    print(f"✅ 成功获取状态: Mission Day {status['mission_day']}")
    print(f"   生存指数: {status['survival_index']:.1f}%")
    print(f"   能源: {status['energy_level']:.1f}%")
    print(f"   食物: {status['food_stability']:.1f}%")
    print(f"   氧气: {status['oxygen_level']:.1f}%")
    print()

def test_phase2_ai_rules():
    """测试Phase 2: AI规则决策引擎"""
    print("=" * 60)
    print("Phase 2: 测试AI规则决策引擎")
    print("=" * 60)
    
    # 测试1: 正常状态
    print("\n[测试1] 正常状态模拟...")
    result = ai_engine.simulate_step()
    print(f"✅ Day {result['mission_day']} 模拟完成")
    print(f"   紧急模式: {'是' if result['emergency_mode'] else '否'}")
    
    # 测试2: 低能源触发规则1
    print("\n[测试2] 低能源场景 (Energy < 40)...")
    ai_engine.adjust_parameters({'energy_level': 35})
    result = ai_engine.simulate_step()
    print(f"✅ Day {result['mission_day']} 模拟完成")
    print(f"   能源: {result['energy_level']:.1f}%")
    print(f"   紧急模式: {'是' if result['emergency_mode'] else '否'}")
    if result.get('logs'):
        print(f"   AI日志条数: {len(result['logs'])}")
        for log in result['logs'][-3:]:
            # logs可能是字符串列表或字典列表
            if isinstance(log, dict):
                print(f"   - {log.get('message', log)}")
            else:
                print(f"   - {log}")
    
    # 测试3: 高辐射触发规则2
    print("\n[测试3] 高辐射场景 (Radiation > 70)...")
    ai_engine.adjust_parameters({'radiation_level': 75})
    result = ai_engine.simulate_step()
    print(f"✅ Day {result['mission_day']} 模拟完成")
    print(f"   辐射: {result['radiation_level']:.1f}%")
    print(f"   医疗安全: {result['medical_safety']:.1f}%")
    if result.get('logs'):
        print(f"   AI日志条数: {len(result['logs'])}")
        for log in result['logs'][-3:]:
            if isinstance(log, dict):
                print(f"   - {log.get('message', log)}")
            else:
                print(f"   - {log}")
    
    # 测试4: 低蛋白质触发规则3
    print("\n[测试4] 低蛋白质场景 (Protein < 20)...")
    ai_engine.adjust_parameters({'protein_level': 15})
    result = ai_engine.simulate_step()
    print(f"✅ Day {result['mission_day']} 模拟完成")
    print(f"   蛋白质: {result['protein_level']:.1f}%")
    if result.get('logs'):
        print(f"   AI日志条数: {len(result['logs'])}")
        for log in result['logs'][-3:]:
            if isinstance(log, dict):
                print(f"   - {log.get('message', log)}")
            else:
                print(f"   - {log}")
    
    # 测试5: 低氧气触发规则4
    print("\n[测试5] 低氧气场景 (Oxygen < 30)...")
    ai_engine.adjust_parameters({'oxygen_level': 25})
    result = ai_engine.simulate_step()
    print(f"✅ Day {result['mission_day']} 模拟完成")
    print(f"   氧气: {result['oxygen_level']:.1f}%")
    print(f"   乘员数: {result['crew_count']}")
    if result.get('logs'):
        print(f"   AI日志条数: {len(result['logs'])}")
        for log in result['logs'][-3:]:
            if isinstance(log, dict):
                print(f"   - {log.get('message', log)}")
            else:
                print(f"   - {log}")
    
    # 测试6: 紧急模式触发
    print("\n[测试6] 紧急模式触发 (Oxygen < 15)...")
    ai_engine.adjust_parameters({'oxygen_level': 12, 'energy_level': 8})
    result = ai_engine.simulate_step()
    print(f"✅ Day {result['mission_day']} 模拟完成")
    print(f"   氧气: {result['oxygen_level']:.1f}%")
    print(f"   能源: {result['energy_level']:.1f}%")
    print(f"   🚨 紧急模式: {'是 ✅' if result['emergency_mode'] else '否 ❌'}")
    if result.get('logs'):
        emergency_logs = [log for log in result['logs'] if 'EMERGENCY' in (log if isinstance(log, str) else log.get('message', ''))]
        print(f"   紧急日志条数: {len(emergency_logs)}")
        for log in emergency_logs:
            if isinstance(log, dict):
                print(f"   - {log.get('message', log)}")
            else:
                print(f"   - {log}")

def test_simulation_speed():
    """测试仿真速度计算"""
    print("\n" + "=" * 60)
    print("附加测试: 仿真速度计算")
    print("=" * 60)
    
    speeds = [1, 5, 10]
    for speed in speeds:
        interval_ms = 1000 / (speed * 24)
        interval_sec = interval_ms / 1000
        print(f"\n速度 {speed}x:")
        print(f"  - 每次间隔: {interval_ms:.2f}ms ({interval_sec:.3f}秒)")
        print(f"  - 1小时模拟时间: {interval_sec:.3f}秒")
        print(f"  - 1天(24小时)模拟时间: {interval_sec * 24:.2f}秒")

if __name__ == '__main__':
    print("\n🚀 开始深空AI生存系统 Phase 1 & 2 测试\n")
    
    try:
        test_phase1_backend()
        test_phase2_ai_rules()
        test_simulation_speed()
        
        print("\n" + "=" * 60)
        print("✅ 所有测试完成!")
        print("=" * 60)
        print("\n下一步:")
        print("1. 运行 space_survival_system.py 启动服务器")
        print("2. 打开浏览器访问 http://localhost:5000")
        print("3. 点击左侧导航栏的 '仿真实验 Simulation'")
        print("4. 设置初始参数并选择仿真速度")
        print("5. 点击 '开始实验 START' 观察实时仿真")
        print("6. 尝试将资源降至临界值,观察紧急模式UI效果")
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
