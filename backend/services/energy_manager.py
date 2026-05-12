class EnergyManager:
    """能源管理服务 - 负责能源衰减计算、低功耗模式和阈值检查"""
    
    @staticmethod
    def calculate_decay(current_energy, time_elapsed_hours=1.0):
        """
        计算能源衰减
        :param current_energy: 当前能源水平
        :param time_elapsed_hours: 经过的小时数
        :return: 衰减后的能源水平
        """
        # 基础衰减率：每小时0.5%
        base_decay_rate = 0.5
        
        # 根据当前负载调整衰减率
        if current_energy > 70:
            decay_rate = base_decay_rate * 1.2  # 高负载
        elif current_energy > 30:
            decay_rate = base_decay_rate  # 正常负载
        else:
            decay_rate = base_decay_rate * 0.8  # 低功耗
        
        decay = decay_rate * time_elapsed_hours
        return max(0, current_energy - decay)
    
    @staticmethod
    def apply_low_power_mode(status):
        """
        应用低功耗模式
        降低次级系统功耗，优先保障关键系统
        """
        actions = []
        
        # 降低食物区冷却精度
        if status.food_stability > 20:
            status.food_stability -= 2.0
            actions.append("已降低食物区冷却精度")
        
        # 减少非关键区域照明
        actions.append("已关闭非必要照明系统")
        
        # 降低环境控制系统功耗
        status.humidity = max(30, status.humidity - 5)
        actions.append("已降低环控系统功耗")
        
        # 节省能源
        status.energy_level += 5.0
        actions.append("已切换至低功耗模式")
        
        return actions
    
    @staticmethod
    def check_thresholds(status):
        """
        检查能源阈值并触发相应动作
        :return: 触发的事件列表
        """
        events = []
        
        if status.energy_level < 10:
            events.append({
                "type": "CRITICAL",
                "message": "能源危机：剩余能源低于10%，立即启动紧急协议"
            })
        elif status.energy_level < 20:
            events.append({
                "type": "WARNING",
                "message": "能源警告：剩余能源低于20%，建议启动低功耗模式"
            })
        elif status.energy_level < 30:
            events.append({
                "type": "INFO",
                "message": "能源提示：剩余能源低于30%，已降低非关键系统功耗"
            })
        elif status.energy_level < 40:
            events.append({
                "type": "INFO",
                "message": "能源联动：已降低次级冷却系统精度"
            })
        
        return events
    
    @staticmethod
    def calculate_backup_time(status):
        """
        计算备用电源可支撑时间
        """
        if status.energy_level <= 0:
            return status.backup_power_hours
        return 0
