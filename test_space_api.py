"""
太空数据API测试脚本
测试所有15个API接口是否正常工作
"""
import requests
import json
import time

BASE_URL = "http://localhost:5000"

def test_api(endpoint, name):
    """测试单个API端点"""
    print(f"\n{'='*60}")
    print(f"测试: {name}")
    print(f"端点: {endpoint}")
    print('='*60)
    
    try:
        response = requests.get(f"{BASE_URL}{endpoint}", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, dict) and 'error' in data:
                print(f"❌ 失败: {data['error']}")
                return False
            else:
                print(f"✅ 成功!")
                # 显示部分数据预览
                if isinstance(data, dict):
                    print(f"   数据类型: dict, 键数量: {len(data)}")
                    for key in list(data.keys())[:3]:
                        value = data[key]
                        if isinstance(value, (str, int, float)):
                            print(f"   - {key}: {value}")
                        elif isinstance(value, list):
                            print(f"   - {key}: [{len(value)} items]")
                elif isinstance(data, list):
                    print(f"   数据类型: list, 长度: {len(data)}")
                    if len(data) > 0:
                        print(f"   第一项预览: {json.dumps(data[0], ensure_ascii=False)[:100]}...")
                return True
        else:
            print(f"❌ HTTP错误: {response.status_code}")
            print(f"   响应: {response.text[:200]}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ 超时")
        return False
    except Exception as e:
        print(f"❌ 异常: {str(e)}")
        return False

def main():
    print("\n" + "="*60)
    print("深空AI生存系统 - 太空数据API测试")
    print("="*60)
    
    tests = [
        # 第一批：核心空间天气API
        ("/api/space-weather/summary", "太空天气摘要"),
        ("/api/space-weather/storms", "太阳风暴数据"),
        ("/api/space-weather/radiation", "辐射数据"),
        ("/api/space-weather/flares", "太阳耀斑数据"),
        
        # 第二批：实时态势感知
        ("/api/iss/position", "ISS位置"),
        ("/api/astronauts", "在轨宇航员"),
        ("/api/spacex/latest", "SpaceX最新发射"),
        ("/api/spacex/rockets", "SpaceX火箭数据"),
        
        # 第三批：视觉增强
        ("/api/mars/photos?rover=curiosity&sol=1000&per_page=5", "火星照片"),
        ("/api/earth/photos", "地球照片(EPIC)"),
        ("/api/moon", "月球数据"),
        ("/api/planets", "行星数据"),
        
        # 第四批：地球环境
        ("/api/earth/disasters?limit=5", "地球自然灾害"),
        ("/api/earthquakes?min_magnitude=5.0&days=7", "地震数据"),
        ("/api/air-quality?location=beijing", "空气质量"),
        ("/api/weather/macau", "澳门天气"),
    ]
    
    results = []
    for endpoint, name in tests:
        result = test_api(endpoint, name)
        results.append((name, result))
        time.sleep(0.5)  # 避免请求过快
    
    # 汇总结果
    print("\n" + "="*60)
    print("测试结果汇总")
    print("="*60)
    
    success_count = sum(1 for _, r in results if r)
    total_count = len(results)
    
    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{status} - {name}")
    
    print(f"\n总计: {success_count}/{total_count} 通过")
    
    if success_count == total_count:
        print("\n🎉 所有API测试通过！")
    else:
        print(f"\n⚠️  {total_count - success_count} 个API测试失败，请检查网络连接或API密钥配置")
    
    return success_count == total_count

if __name__ == "__main__":
    print("\n提示: 请先启动Flask应用 (python app.py)")
    input("按Enter键开始测试...")
    main()
