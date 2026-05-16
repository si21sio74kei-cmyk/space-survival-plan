"""
太空梦想计划 - 系统验证测试脚本
全面检查所有核心功能是否正常
"""
import sys
import os

def test_imports():
    """测试所有导入"""
    print("=" * 60)
    print("测试1: 导入检查")
    print("=" * 60)
    
    try:
        import flask
        print("✅ Flask 导入成功")
    except ImportError as e:
        print(f"❌ Flask 导入失败: {e}")
        return False
    
    try:
        import openai
        print("✅ OpenAI 导入成功")
    except ImportError as e:
        print(f"❌ OpenAI 导入失败: {e}")
        return False
    
    try:
        import sqlalchemy
        print("✅ SQLAlchemy 导入成功")
    except ImportError as e:
        print(f"❌ SQLAlchemy 导入失败: {e}")
        return False
    
    print()
    return True

def test_config():
    """测试配置加载"""
    print("=" * 60)
    print("测试2: 配置检查")
    print("=" * 60)
    
    try:
        from config import DEEPSEEK_API_KEY
        print("✅ 根目录 config.py 加载成功")
        if DEEPSEEK_API_KEY:
            print("✅ DEEPSEEK_API_KEY 已配置")
        else:
            print("⚠️ DEEPSEEK_API_KEY 未配置（AI功能将不可用）")
    except Exception as e:
        print(f"❌ 配置加载失败: {e}")
        return False
    
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
        from backend.config import DEEPSEEK_API_KEY as BACKEND_KEY
        print("✅ Backend config.py 加载成功")
    except Exception as e:
        print(f"❌ Backend配置加载失败: {e}")
        return False
    
    print()
    return True

def test_ai_engine():
    """测试AI引擎"""
    print("=" * 60)
    print("测试3: AI引擎检查")
    print("=" * 60)
    
    try:
        # 确保导入的是根目录的ai_engine
        import importlib.util
        spec = importlib.util.spec_from_file_location("root_ai_engine", os.path.join(os.path.dirname(__file__), 'ai_engine.py'))
        root_ai_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(root_ai_module)
        engine = root_ai_module.engine
        
        print("✅ 根目录 AI Engine 加载成功")
        
        # 测试获取状态
        status = engine.get_current_status()
        if isinstance(status, dict):
            print(f"✅ 获取状态成功 - 任务天数: {status['mission_day']}, 生存指数: {status['survival_index']:.1f}%")
        else:
            print(f"✅ 获取状态成功 - 任务天数: {status.mission_day}, 生存指数: {status.survival_index:.1f}%")
        
        # 测试食物库存
        food = engine.get_food_inventory()
        print(f"✅ 获取食物库存成功 - 稳定性: {food['food_stability']:.1f}%")
        
        # 测试医疗状态
        medical = engine.get_medical_status()
        print(f"✅ 获取医疗状态成功 - 安全性: {medical['medical_safety']:.1f}%")
        
        # 测试能源状态
        energy = engine.get_energy_status()
        print(f"✅ 获取能源状态成功 - 能源水平: {energy['energy_level']:.1f}%")
        
        # 测试环境状态
        env = engine.get_environment_status()
        print(f"✅ 获取环境状态成功 - 氧气: {env['oxygen_level']:.1f}%")
        
    except Exception as e:
        print(f"❌ AI引擎测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print()
    return True

def test_backend_ai_engine():
    """测试Backend AI引擎"""
    print("=" * 60)
    print("测试4: Backend AI引擎检查")
    print("=" * 60)
    
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
        from backend.ai_engine import engine as backend_engine
        print("✅ Backend AI Engine 加载成功")
        
        # 测试获取状态
        status = backend_engine.get_current_status()
        print(f"✅ 获取状态成功 - 任务天数: {status.mission_day}, 生存指数: {status.survival_index:.1f}%")
        
    except Exception as e:
        print(f"❌ Backend AI引擎测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print()
    return True

def test_flask_app():
    """测试Flask应用"""
    print("=" * 60)
    print("测试5: Flask应用检查")
    print("=" * 60)
    
    try:
        from app import app
        print("✅ Flask App 加载成功")
        
        # 检查路由数量
        route_count = len(app.url_map._rules)
        print(f"✅ 注册了 {route_count} 个路由")
        
        # 检查关键路由是否存在
        required_routes = [
            '/',
            '/api/survival-status',
            '/api/food-inventory',
            '/api/medical-status',
            '/api/energy-status',
            '/api/environment-status',
            '/api/ai-logs',
            '/api/generate-report',
            '/api/simulate_step'
        ]
        
        registered_rules = [rule.rule for rule in app.url_map._rules]
        missing_routes = []
        
        for route in required_routes:
            if route in registered_rules:
                print(f"✅ 路由 {route} 已注册")
            else:
                print(f"❌ 路由 {route} 缺失")
                missing_routes.append(route)
        
        if missing_routes:
            print(f"\n⚠️ 缺少 {len(missing_routes)} 个关键路由")
            return False
        
    except Exception as e:
        print(f"❌ Flask应用测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print()
    return True

def test_database_models():
    """测试数据库模型"""
    print("=" * 60)
    print("测试6: 数据库模型检查")
    print("=" * 60)
    
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
        from backend.models import SurvivalStatus, ResourceLog, Base, engine
        print("✅ 数据库模型加载成功")
        
        # 检查表是否创建
        tables = Base.metadata.tables.keys()
        print(f"✅ 创建了 {len(tables)} 个表: {', '.join(tables)}")
        
    except Exception as e:
        print(f"❌ 数据库模型测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print()
    return True

def main():
    """运行所有测试"""
    print("\n")
    print("太空梦想计划 - 系统验证测试")
    print("=" * 60)
    print()
    
    results = []
    
    # 运行所有测试
    results.append(("导入检查", test_imports()))
    results.append(("配置检查", test_config()))
    results.append(("AI引擎检查", test_ai_engine()))
    results.append(("Backend AI引擎检查", test_backend_ai_engine()))
    results.append(("Flask应用检查", test_flask_app()))
    results.append(("数据库模型检查", test_database_models()))
    
    # 汇总结果
    print("=" * 60)
    print("测试结果汇总")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "通过" if result else "失败"
        print(f"{test_name}: {status}")
    
    print()
    print(f"总计: {passed}/{total} 测试通过")
    
    if passed == total:
        print("\n所有测试通过！系统运行正常！")
        return 0
    else:
        print(f"\n{total - passed} 个测试失败，请检查上述错误信息")
        return 1

if __name__ == '__main__':
    sys.exit(main())
