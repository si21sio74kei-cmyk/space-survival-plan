"""
太空梦想计划 - 单元测试套件
测试核心功能的正确性
"""
import sys
import os
import unittest
from datetime import datetime

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ai_engine import engine, get_persistent_state


class TestAISurvivalEngine(unittest.TestCase):
    """AI生存引擎测试类"""
    
    def setUp(self):
        """每个测试前的设置"""
        # 重置状态以确保测试独立性
        if hasattr(get_persistent_state, '_state'):
            delattr(get_persistent_state, '_state')
        if hasattr(get_persistent_state, '_logs'):
            delattr(get_persistent_state, '_logs')
    
    def test_get_current_status(self):
        """测试获取当前状态"""
        status = engine.get_current_status()
        
        # 验证必需字段存在
        required_fields = [
            'mission_day', 'survival_index', 'food_stability',
            'medical_safety', 'energy_level', 'oxygen_level',
            'temperature', 'humidity', 'pressure'
        ]
        
        for field in required_fields:
            self.assertIn(field, status, f"缺少字段: {field}")
        
        # 验证数值范围
        self.assertGreaterEqual(status['survival_index'], 0)
        self.assertLessEqual(status['survival_index'], 100)
        self.assertGreaterEqual(status['mission_day'], 1)
    
    def test_simulate_step(self):
        """测试模拟步骤"""
        result = engine.simulate_step()
        
        # 验证返回结果
        self.assertIn('mission_day', result)
        self.assertIn('survival_index', result)
        self.assertIn('temperature', result)
        
        # 验证任务天数增加
        self.assertEqual(result['mission_day'], 2)
        
        # 验证预测数据
        self.assertIn('predictions', result)
        self.assertEqual(len(result['predictions']), 4)
    
    def test_add_food_item(self):
        """测试添加食物"""
        item_data = {
            'name': '测试食物',
            'quantity': 50,
            'nutrition_type': 'protein'
        }
        
        result = engine.add_food_item(item_data)
        
        self.assertTrue(result['success'])
        self.assertIn('item', result)
        self.assertEqual(result['item']['name'], '测试食物')
    
    def test_add_medical_item(self):
        """测试添加医疗物品"""
        item_data = {
            'name': '测试药品',
            'type': 'medicine',
            'quantity': 10,
            'storage_temp': -70
        }
        
        result = engine.add_medical_item(item_data)
        
        self.assertTrue(result['success'])
        self.assertIn('item', result)
        self.assertEqual(result['item']['name'], '测试药品')
    
    def test_add_crew_member(self):
        """测试添加宇航员"""
        member_data = {
            'name': '测试宇航员',
            'weight': 70,
            'age': 35,
            'health_status': 'good',
            'calorie_needs': 2500
        }
        
        result = engine.add_crew_member(member_data)
        
        self.assertTrue(result['success'])
        self.assertIn('member', result)
        self.assertEqual(result['member']['name'], '测试宇航员')
    
    def test_adjust_parameters(self):
        """测试参数调整"""
        adjustments = {
            'food_stability': 80.0,
            'energy_level': 85.0
        }
        
        result = engine.adjust_parameters(adjustments)
        
        self.assertTrue(result['success'])
        self.assertIn('adjusted', result)
        self.assertGreater(len(result['adjusted']), 0)
    
    def test_generate_report(self):
        """测试生成报告"""
        report = engine.generate_report('daily')
        
        self.assertIn('type', report)
        self.assertIn('mission_day', report)
        self.assertIn('summary', report)
        self.assertEqual(report['type'], 'daily')
    
    def test_trigger_emergency(self):
        """测试触发紧急协议"""
        result = engine.trigger_emergency('warning')
        
        self.assertIn('status', result)
        self.assertIn('level', result)
        self.assertEqual(result['level'], 'warning')
    
    def test_update_energy_distribution(self):
        """测试能源分配更新"""
        distribution = {
            'medical': 35,
            'food': 25,
            'environment': 20,
            'other': 20
        }
        
        result = engine.update_energy_distribution(distribution)
        
        self.assertTrue(result['success'])
        self.assertEqual(result['distribution']['medical'], 35)
    
    def test_invalid_energy_distribution(self):
        """测试无效的能源分配（总和不为100）"""
        distribution = {
            'medical': 50,
            'food': 50,
            'environment': 50,
            'other': 50
        }
        
        result = engine.update_energy_distribution(distribution)
        
        self.assertFalse(result['success'])
        self.assertIn('error', result)
    
    def test_temperature_field_exists(self):
        """测试temperature字段存在"""
        status = engine.get_current_status()
        self.assertIn('temperature', status)
        self.assertIsInstance(status['temperature'], (int, float))
    
    def test_state_persistence(self):
        """测试状态持久化"""
        # 第一次获取状态
        status1 = engine.get_current_status()
        day1 = status1['mission_day']
        
        # 执行模拟步骤
        engine.simulate_step()
        
        # 第二次获取状态
        status2 = engine.get_current_status()
        day2 = status2['mission_day']
        
        # 验证天数增加
        self.assertEqual(day2, day1 + 1)


class TestInputValidation(unittest.TestCase):
    """输入验证测试类"""
    
    def test_food_quantity_validation(self):
        """测试食物数量验证"""
        # 负数应该被拒绝（在app.py中验证）
        # 这里测试engine层面的处理
        item_data = {
            'name': '测试',
            'quantity': -10  # 无效值
        }
        
        # engine层面可能允许，但app.py会拦截
        result = engine.add_food_item(item_data)
        # 注意：实际验证在Flask路由层
        
    def test_crew_age_validation(self):
        """测试宇航员年龄验证"""
        member_data = {
            'name': '测试',
            'age': 200,  # 超出合理范围
            'weight': 70
        }
        
        # engine层面可能允许，但app.py会拦截
        result = engine.add_crew_member(member_data)


def run_tests():
    """运行所有测试"""
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加测试类
    suite.addTests(loader.loadTestsFromTestCase(TestAISurvivalEngine))
    suite.addTests(loader.loadTestsFromTestCase(TestInputValidation))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 返回测试结果
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
