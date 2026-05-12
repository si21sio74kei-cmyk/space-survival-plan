class FoodManager:
    """食物管理服务 - 负责食物消耗、新鲜度衰减和配给调整"""
    
    @staticmethod
    def calculate_consumption(food_level, crew_count):
        """
        计算食物消耗
        :param food_level: 当前食物水平
        :param crew_count: 乘员数量
        :return: 消耗量
        """
        # 每人每天消耗约0.5%
        consumption_rate = 0.5 * crew_count / 4.0
        return consumption_rate
    
    @staticmethod
    def check_freshness_decay(food_stability, time_elapsed_days=1):
        """
        计算新鲜度衰减
        :param food_stability: 当前新鲜度
        :param time_elapsed_days: 经过的天数
        :return: 衰减后的新鲜度
        """
        # 每天自然衰减0.2%
        decay_rate = 0.2 * time_elapsed_days
        return max(0, food_stability - decay_rate)
    
    @staticmethod
    def adjust_ration(status, ai_advice):
        """
        根据AI建议调整配给
        :param status: 当前状态
        :param ai_advice: AI建议
        :return: 配给建议
        """
        diet_advice = "标准配给"
        
        # 根据食物状态调整
        if status.food_stability < 30:
            diet_advice = "紧急配给模式：每日热量摄入降低20%"
            status.crew_count = max(1, status.crew_count - 1)
        elif status.food_stability < 50:
            diet_advice = "低能耗营养模式：减少高蛋白摄入，增加合成碳水比例"
        elif status.protein_level < 40:
            diet_advice = "蛋白质限制模式：优化蛋白质分配，优先保障医疗"
        else:
            diet_advice = "标准配给模式"
        
        return diet_advice
    
    @staticmethod
    def check_food_warnings(status):
        """
        检查食物系统警告
        :return: 警告列表
        """
        warnings = []
        
        if status.food_stability < 20:
            warnings.append("严重警告：食物储备极低，请立即补充")
        elif status.food_stability < 40:
            warnings.append("警告：食物储备不足，建议调整配给")
        
        if status.protein_level < 30:
            warnings.append("警告：蛋白质储备偏低")
        
        if status.water_reserve < 30:
            warnings.append("严重警告：水资源严重不足")
        elif status.water_reserve < 50:
            warnings.append("警告：水资源储备偏低")
        
        return warnings