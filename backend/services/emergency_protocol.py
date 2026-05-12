import random

class EmergencyProtocol:
    """紧急协议服务 - 处理各种深空紧急情况"""
    
    @staticmethod
    def trigger_solar_storm(status):
        """太阳风暴协议"""
        actions = []
        
        # 辐射水平飙升
        status.radiation_level = random.uniform(50, 95)
        
        # 启动地下储藏模式
        status.food_stability -= 5
        actions.append("已启动地下储藏模式")
        
        # 优先保障医疗资源
        status.medical_safety = min(100, status.medical_safety + 5)
        status.medical_temp = max(-80, status.medical_temp - 2)
        actions.append("已优先保障医疗冷链")
        
        # 降低非关键系统
        status.energy_level -= 3
        actions.append("已降低非必要系统功耗")
        
        return {
            "protocol": "SOLAR_STORM",
            "actions": actions,
            "message": "检测到强太阳辐射风暴，已启动防护协议"
        }
    
    @staticmethod
    def trigger_oxygen_leak(status):
        """氧气泄漏协议"""
        actions = []
        
        # 氧气快速下降
        status.oxygen_level -= 15
        
        # 启动备用氧气系统
        if status.energy_level > 20:
            status.energy_level -= 10
            status.oxygen_level += 10
            actions.append("已启动备用氧气系统")
        else:
            actions.append("警告：能源不足，无法启动备用氧气")
        
        # 降低人员活动
        status.crew_count = max(1, status.crew_count - 2)
        actions.append("已减少乘员活动")
        
        return {
            "protocol": "OXYGEN_LEAK",
            "actions": actions,
            "message": "检测到氧气泄漏，已启动紧急供氧"
        }
    
    @staticmethod
    def trigger_energy_crisis(status):
        """能源危机协议"""
        actions = []
        
        # 立即进入最低功耗模式
        status.food_stability -= 10
        actions.append("已关闭食物区冷却系统")
        
        # 优先保障生命维持
        status.medical_safety = min(100, status.medical_safety + 3)
        actions.append("已优先保障医疗系统")
        
        # 关闭所有非必要设备
        actions.append("已关闭通讯导航系统")
        actions.append("已关闭AI核心非关键功能")
        
        # 启用备用电源
        if status.backup_power_hours > 0:
            status.backup_power_hours -= 2
            status.energy_level += 15
            actions.append("已启用备用电源")
        
        return {
            "protocol": "ENERGY_CRISIS",
            "actions": actions,
            "message": "能源危机，已启动最低功耗模式"
        }
    
    @staticmethod
    def trigger_cold_chain_failure(status):
        """冷链故障协议"""
        actions = []
        
        # 医疗冷链温度上升
        status.medical_temp += 10
        
        # 尝试修复
        if status.energy_level > 30:
            status.energy_level -= 15
            status.medical_temp -= 5
            actions.append("已启动冷链紧急修复")
        else:
            actions.append("警告：能源不足，无法修复冷链")
        
        # 转移关键物资
        status.medical_safety -= 8
        actions.append("已转移关键医疗物资")
        
        return {
            "protocol": "COLD_CHAIN_FAILURE",
            "actions": actions,
            "message": "医疗冷链故障，已启动应急预案"
        }
    
    @staticmethod
    def trigger_hull_breach(status):
        """舱体破损协议"""
        actions = []
        
        # 舱压下降
        status.pressure -= 10
        
        # 隔离破损区域
        actions.append("已隔离破损舱段")
        
        # 启动应急密封
        if status.energy_level > 20:
            status.energy_level -= 8
            status.pressure += 5
            actions.append("已启动应急密封系统")
        
        # 降低人员数量
        status.crew_count = max(1, status.crew_count - 1)
        actions.append("已转移乘员至安全区域")
        
        return {
            "protocol": "HULL_BREACH",
            "actions": actions,
            "message": "舱体破损，已启动密封应急协议"
        }
