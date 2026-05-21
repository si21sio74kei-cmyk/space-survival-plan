"""
深度检查所有15个太空/地球数据API的正确性
对比用户提供的表格，验证接口地址、参数和数据解析逻辑
"""
import requests
import json
from datetime import datetime

# 颜色输出
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_header(text):
    print(f"\n{Colors.BLUE}{'='*80}{Colors.END}")
    print(f"{Colors.BLUE}{text.center(76)}{Colors.END}")
    print(f"{Colors.BLUE}{'='*80}{Colors.END}\n")

def print_result(api_num, name, status, details=""):
    color = Colors.GREEN if status == "✓" else (Colors.YELLOW if status == "⚠" else Colors.RED)
    print(f"{color}[{api_num}] {name}: {status}{Colors.END}")
    if details:
        print(f"      {details}")

def test_api(url, params=None, timeout=10, expected_status=200):
    """测试API是否可访问"""
    try:
        response = requests.get(url, params=params, timeout=timeout)
        return {
            'success': response.status_code == expected_status,
            'status_code': response.status_code,
            'data': response.json() if response.status_code == expected_status else None,
            'error': None if response.status_code == expected_status else f"HTTP {response.status_code}"
        }
    except Exception as e:
        return {
            'success': False,
            'status_code': None,
            'data': None,
            'error': str(e)
        }

print_header("开始深度检查15个API接口")

results = []

# ==================== API 1: 火星照片数据 API ====================
print_header("API 1: 火星照片数据 API")
url1 = "https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos"
params1 = {'sol': 1000, 'api_key': 'DEMO_KEY', 'page': 1, 'per_page': 1}
result1 = test_api(url1, params1)
if result1['success']:
    data = result1['data']
    has_photos = isinstance(data, dict) and 'photos' in data
    print_result(1, "接口地址", "✓", f"返回数据包含photos字段: {has_photos}")
    if has_photos and len(data['photos']) > 0:
        photo = data['photos'][0]
        fields = ['id', 'img_src', 'rover', 'camera', 'earth_date', 'sol']
        missing = [f for f in fields if f not in photo]
        if not missing:
            print_result(1, "数据结构", "✓", f"包含所有必需字段")
        else:
            print_result(1, "数据结构", "⚠", f"缺少字段: {missing}")
else:
    print_result(1, "接口可用性", "✗", result1['error'])

# 检查代码实现
print("\n检查后端实现...")
try:
    from backend.space_data_api import space_api
    mars_data = space_api.get_mars_photos(rover='curiosity', sol=1000, per_page=1)
    if isinstance(mars_data, dict) and 'photos' in mars_data:
        print_result(1, "后端方法", "✓", "get_mars_photos() 正常工作")
    else:
        print_result(1, "后端方法", "⚠", f"返回数据类型异常: {type(mars_data)}")
except Exception as e:
    print_result(1, "后端方法", "✗", str(e))

# ==================== API 2: 月球数据 API ====================
print_header("API 2: 月球数据 API")
url2 = "https://api.le-systeme-solaire.net/rest/bodies/moon"
result2 = test_api(url2)
if result2['success']:
    data = result2['data']
    required_fields = ['mass', 'density', 'gravity', 'meanRadius', 'sideralOrbit', 'sideralRotation']
    missing = [f for f in required_fields if f not in data]
    if not missing:
        print_result(2, "数据结构", "✓", f"包含所有天体物理参数")
    else:
        print_result(2, "数据结构", "⚠", f"缺少字段: {missing}")
    print_result(2, "接口地址", "✓", "正确")
else:
    print_result(2, "接口可用性", "✗", result2['error'])

# ==================== API 3: NASA 地球灾害数据 API ====================
print_header("API 3: NASA 地球灾害数据 API")
url3 = "https://eonet.gsfc.nasa.gov/api/v3/events"
params3 = {'limit': 5, 'days': 7}
result3 = test_api(url3, params3)
if result3['success']:
    data = result3['data']
    has_events = isinstance(data, dict) and 'events' in data
    print_result(3, "接口地址", "✓", f"返回数据包含events字段: {has_events}")
    if has_events and len(data['events']) > 0:
        event = data['events'][0]
        fields = ['id', 'title', 'geometry']
        missing = [f for f in fields if f not in event]
        if not missing:
            print_result(3, "数据结构", "✓", "包含事件基本信息")
        else:
            print_result(3, "数据结构", "⚠", f"缺少字段: {missing}")
else:
    print_result(3, "接口可用性", "✗", result3['error'])

# ==================== API 4: ISS 实时位置 API ====================
print_header("API 4: ISS 实时位置 API")
url4 = "http://api.open-notify.org/iss-now.json"
result4 = test_api(url4)
if result4['success']:
    data = result4['data']
    has_position = isinstance(data, dict) and 'iss_position' in data
    if has_position:
        pos = data['iss_position']
        has_coords = 'latitude' in pos and 'longitude' in pos
        print_result(4, "数据结构", "✓" if has_coords else "⚠", 
                    f"包含经纬度坐标: {has_coords}")
    print_result(4, "接口地址", "✓", "正确（无需API Key）")
else:
    print_result(4, "接口可用性", "✗", result4['error'])

# ==================== API 5: 当前太空宇航员 API ====================
print_header("API 5: 当前太空宇航员 API")
url5 = "http://api.open-notify.org/astros.json"
result5 = test_api(url5)
if result5['success']:
    data = result5['data']
    has_people = isinstance(data, dict) and 'people' in data and 'number' in data
    if has_people:
        print_result(5, "数据结构", "✓", f"当前有 {data['number']} 名宇航员在太空")
    print_result(5, "接口地址", "✓", "正确（无需API Key）")
else:
    print_result(5, "接口可用性", "✗", result5['error'])

# ==================== API 6: NASA 太阳风暴 API ====================
print_header("API 6: NASA 太阳风暴 API (DONKI CME)")
url6 = "https://api.nasa.gov/DONKI/CME"
start_date = (datetime.utcnow().replace(day=1)).strftime('%Y-%m-%d')
end_date = datetime.utcnow().strftime('%Y-%m-%d')
params6 = {'startDate': start_date, 'endDate': end_date, 'api_key': 'DEMO_KEY'}
result6 = test_api(url6, params6)
if result6['success']:
    data = result6['data']
    is_list = isinstance(data, list)
    print_result(6, "接口地址", "✓", f"返回数组类型: {is_list}")
    if is_list and len(data) > 0:
        cme = data[0]
        fields = ['activityID', 'startTime', 'linkage']
        missing = [f for f in fields if f not in cme]
        if not missing:
            print_result(6, "数据结构", "✓", "包含CME事件信息")
        else:
            print_result(6, "数据结构", "⚠", f"缺少字段: {missing}")
else:
    print_result(6, "接口可用性", "✗", result6['error'])

# ==================== API 7: NASA 太空辐射数据 API ====================
print_header("API 7: NASA 太空辐射数据 API (DONKI RBE)")
url7 = "https://api.nasa.gov/DONKI/RBE"
params7 = {'startDate': start_date, 'endDate': end_date, 'api_key': 'DEMO_KEY'}
result7 = test_api(url7, params7)
if result7['success']:
    data = result7['data']
    is_list = isinstance(data, list)
    print_result(7, "接口地址", "✓", f"返回数组类型: {is_list}")
else:
    print_result(7, "接口可用性", "✗", result7['error'])

# ==================== API 8: NASA 实时太阳耀斑 API ====================
print_header("API 8: NASA 实时太阳耀斑 API (DONKI FLR)")
url8 = "https://api.nasa.gov/DONKI/FLR"
params8 = {'startDate': start_date, 'endDate': end_date, 'api_key': 'DEMO_KEY'}
result8 = test_api(url8, params8)
if result8['success']:
    data = result8['data']
    is_list = isinstance(data, list)
    print_result(8, "接口地址", "✓", f"返回数组类型: {is_list}")
    if is_list and len(data) > 0:
        flare = data[0]
        has_class = 'classType' in flare
        print_result(8, "数据结构", "✓" if has_class else "⚠", 
                    f"包含耀斑等级: {has_class}")
else:
    print_result(8, "接口可用性", "✗", result8['error'])

# ==================== API 9: 全球地震数据 API ====================
print_header("API 9: 全球地震数据 API (USGS)")
url9 = "https://earthquake.usgs.gov/fdsnws/event/1/query"
params9 = {'format': 'geojson', 'minmagnitude': 5.0, 'starttime': start_date}
result9 = test_api(url9, params9)
if result9['success']:
    data = result9['data']
    is_geojson = isinstance(data, dict) and 'features' in data and 'type' in data
    print_result(9, "接口地址", "✓", f"返回GeoJSON格式: {is_geojson}")
    if is_geojson and len(data['features']) > 0:
        feature = data['features'][0]
        has_props = 'properties' in feature and 'geometry' in feature
        print_result(9, "数据结构", "✓" if has_props else "⚠", 
                    f"包含属性和几何信息: {has_props}")
else:
    print_result(9, "接口可用性", "✗", result9['error'])

# ==================== API 10: 澳门实时天气 API (腾讯) ====================
print_header("API 10: 澳门实时天气 API (腾讯)")
url10 = "https://wis.qq.com/weather/common"
params10 = {
    'source': 'pc',
    'weather_type': 'observe|forecast_24h|air',
    'province': '澳门',
    'city': '澳门'
}
result10 = test_api(url10, params10, timeout=15)
if result10['success']:
    data = result10['data']
    # 腾讯天气API返回结构特殊，需要检查是否有data字段
    has_data = isinstance(data, dict) and ('data' in data or 'observe' in data)
    print_result(10, "接口地址", "✓" if has_data else "⚠", 
                f"返回数据结构: {list(data.keys())[:5] if isinstance(data, dict) else '非字典'}")
else:
    print_result(10, "接口可用性", "✗", result10['error'])

# ==================== API 11: 全球空气质量 API ====================
print_header("API 11: 全球空气质量 API (WAQI)")
url11 = "https://api.waqi.info/feed/here/"
params11 = {'token': 'demo'}
result11 = test_api(url11, params11)
if result11['success']:
    data = result11['data']
    has_status = isinstance(data, dict) and 'status' in data
    if has_status and data['status'] == 'ok':
        has_aqi = 'data' in data and 'aqi' in data['data']
        print_result(11, "数据结构", "✓" if has_aqi else "⚠", 
                    f"AQI数据可用: {has_aqi}")
    else:
        print_result(11, "API状态", "⚠", f"status={data.get('status', 'unknown')}")
    print_result(11, "接口地址", "✓", "正确")
else:
    print_result(11, "接口可用性", "✗", result11['error'])

# ==================== API 12: SpaceX 最新任务 API ====================
print_header("API 12: SpaceX 最新任务 API")
url12 = "https://api.spacexdata.com/v4/launches/latest"
result12 = test_api(url12)
if result12['success']:
    data = result12['data']
    required_fields = ['id', 'name', 'date_utc', 'rocket', 'success']
    missing = [f for f in required_fields if f not in data]
    if not missing:
        print_result(12, "数据结构", "✓", "包含所有发射任务字段")
    else:
        print_result(12, "数据结构", "⚠", f"缺少字段: {missing}")
    print_result(12, "接口地址", "✓", "正确")
else:
    print_result(12, "接口可用性", "✗", result12['error'])

# ==================== API 13: SpaceX 火箭数据 API ====================
print_header("API 13: SpaceX 火箭数据 API")
url13 = "https://api.spacexdata.com/v4/rockets"
result13 = test_api(url13)
if result13['success']:
    data = result13['data']
    is_list = isinstance(data, list)
    print_result(13, "接口地址", "✓", f"返回数组类型: {is_list}")
    if is_list and len(data) > 0:
        rocket = data[0]
        fields = ['id', 'name', 'height', 'mass', 'thrust_sea_level']
        missing = [f for f in fields if f not in rocket]
        if not missing:
            print_result(13, "数据结构", "✓", "包含火箭物理参数")
        else:
            print_result(13, "数据结构", "⚠", f"缺少字段: {missing}")
else:
    print_result(13, "接口可用性", "✗", result13['error'])

# ==================== API 14: NASA EPIC 地球照片 API ====================
print_header("API 14: NASA EPIC 地球照片 API")
today = datetime.utcnow().strftime('%Y-%m-%d')
url14 = f"https://epic.gsfc.nasa.gov/api/natural/date/{today}"
result14 = test_api(url14)
if result14['success']:
    data = result14['data']
    is_list = isinstance(data, list)
    print_result(14, "接口地址", "✓", f"返回数组类型: {is_list}")
    if is_list and len(data) > 0:
        photo = data[0]
        has_fields = 'identifier' in photo and 'date' in photo
        print_result(14, "数据结构", "✓" if has_fields else "⚠", 
                    f"包含照片元数据: {has_fields}")
else:
    print_result(14, "接口可用性", "✗", result14['error'])

# ==================== API 15: 行星列表 API ====================
print_header("API 15: 行星列表 API")
url15 = "https://api.le-systeme-solaire.net/rest/bodies/"
params15 = {'filter[]': 'isPlanet,eq,true'}
result15 = test_api(url15, params15)
if result15['success']:
    data = result15['data']
    has_bodies = isinstance(data, dict) and 'bodies' in data
    if has_bodies:
        planets = data['bodies']
        print_result(15, "数据结构", "✓", f"返回 {len(planets)} 颗行星")
        if len(planets) >= 8:
            planet_names = [p['englishName'] for p in planets if 'englishName' in p]
            print_result(15, "行星数量", "✓", f"包含: {', '.join(planet_names[:4])}...")
    print_result(15, "接口地址", "✓", "正确")
else:
    print_result(15, "接口可用性", "✗", result15['error'])

# ==================== 总结 ====================
print_header("检查总结")
print(f"\n{Colors.GREEN}✓ = 正常  ⚠ = 警告  ✗ = 错误{Colors.END}\n")
print("所有15个API的接口地址已核对完毕。")
print("建议运行实际的后端服务进行完整功能测试。\n")
