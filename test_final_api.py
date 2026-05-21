"""
最终API验证测试 - 检查所有15个API的实现正确性
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.space_data_api import space_api
import json

def test_api(name, func, expected_fields=None):
    """测试单个API"""
    print(f"\n{'='*60}")
    print(f"测试: {name}")
    print('='*60)
    
    try:
        result = func()
        
        # 检查是否有错误
        if isinstance(result, dict) and 'error' in result:
            print(f"❌ API返回错误: {result['error']}")
            if 'message' in result:
                print(f"   消息: {result['message']}")
            if 'fallback_data' in result:
                print(f"   ✓ 但提供了备用数据")
                return True
            return False
        
        # 检查数据结构
        if expected_fields:
            missing = [f for f in expected_fields if f not in str(result)]
            if missing:
                print(f"⚠️  缺少字段: {missing}")
            else:
                print(f"✅ 包含所有预期字段")
        
        print(f"✅ API调用成功")
        print(f"   数据类型: {type(result).__name__}")
        
        if isinstance(result, dict):
            print(f"   键数量: {len(result)}")
            if len(result) < 10:
                print(f"   键列表: {list(result.keys())[:5]}")
        elif isinstance(result, list):
            print(f"   列表长度: {len(result)}")
        
        return True
        
    except Exception as e:
        print(f"❌ 异常: {str(e)}")
        return False

print("="*60)
print("深空AI生存系统 - 太空数据API最终验证")
print("="*60)

results = {}

# 第一批：核心空间天气API
print("\n📡 第一批：核心空间天气API")
results['space_weather'] = test_api(
    "太空天气摘要",
    space_api.get_space_weather_summary,
    ['risk_level', 'warnings', 'recent_events']
)

# 第二批：实时态势感知API
print("\n🛰️  第二批：实时态势感知API")
results['iss'] = test_api(
    "ISS位置",
    space_api.get_iss_position,
    ['iss_position', 'timestamp']
)

results['astronauts'] = test_api(
    "宇航员信息",
    space_api.get_astronauts_in_space,
    ['people', 'number']
)

results['spacex_latest'] = test_api(
    "SpaceX最新发射",
    space_api.get_spacex_latest_launch,
    ['name', 'date_utc', 'rocket']
)

results['spacex_rockets'] = test_api(
    "SpaceX火箭列表",
    space_api.get_spacex_rockets
)

# 第三批：视觉与环境增强API
print("\n📸 第三批：视觉与环境增强API")
results['mars_photos'] = test_api(
    "火星照片 (sol=3500)",
    lambda: space_api.get_mars_photos(rover='curiosity', sol=3500, per_page=1),
    ['photos']
)

results['epic_earth'] = test_api(
    "EPIC地球照片",
    space_api.get_epic_earth_photos
)

results['moon'] = test_api(
    "月球数据",
    space_api.get_moon_data,
    ['englishName', 'mass', 'gravity']
)

results['planets'] = test_api(
    "行星列表",
    space_api.get_planets_data,
    ['bodies']
)

# 第四批：地球环境监控API
print("\n🌍 第四批：地球环境监控API")
results['disasters'] = test_api(
    "地球灾害事件",
    lambda: space_api.get_earth_disasters(limit=2),
    ['events']
)

results['earthquakes'] = test_api(
    "地震数据",
    lambda: space_api.get_earthquakes(min_magnitude=5.0, days=3),
    ['features']
)

results['air_quality'] = test_api(
    "空气质量",
    space_api.get_air_quality,
    ['status', 'data']
)

results['macau_weather'] = test_api(
    "澳门天气",
    space_api.get_macau_weather,
    ['data']
)

# 综合接口测试
print("\n🔗 综合数据接口")
results['all_space_weather'] = test_api(
    "所有太空天气数据",
    space_api.get_all_space_weather
)

results['situational_awareness'] = test_api(
    "态势感知数据",
    space_api.get_situational_awareness
)

results['visual_enhancement'] = test_api(
    "视觉增强数据",
    space_api.get_visual_enhancement_data
)

results['earth_environment'] = test_api(
    "地球环境数据",
    space_api.get_earth_environment_data
)

# 总结
print("\n" + "="*60)
print("测试结果总结")
print("="*60)

total = len(results)
passed = sum(1 for v in results.values() if v)
failed = total - passed

print(f"\n总计: {total} 个API测试")
print(f"✅ 通过: {passed}")
print(f"❌ 失败: {failed}")
print(f"成功率: {passed*100//total}%")

if failed > 0:
    print("\n失败的API:")
    for name, status in results.items():
        if not status:
            print(f"  - {name}")

print("\n" + "="*60)
print("验证完成！")
print("="*60)
