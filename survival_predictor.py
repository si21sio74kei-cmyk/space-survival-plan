class SurvivalPredictor:
    """生存预测服务 - 基于当前资源计算预计生存天数和时间线"""
    
    @staticmethod
    def predict_survival_days(status):
        """
        基于当前资源计算预计生存天数
        公式：min(食物可维持天数, 能源可维持天数, 氧气可维持天数, 水可维持天数)
        考虑乘员消耗率
        """
        crew_count = max(1, status.crew_count)
        
        # 食物可维持天数（假设每天消耗2%）
        food_days = status.food_stability / (2.0 * crew_count / 4.0)
        
        # 能源可维持天数（假设每天消耗1%）
        energy_days = status.energy_level / 1.0
        
        # 氧气可维持天数（假设每天消耗0.5%）
        oxygen_days = status.oxygen_level / 0.5
        
        # 水可维持天数（假设每天消耗1.5%）
        water_days = status.water_reserve / (1.5 * crew_count / 4.0)
        
        # 取最小值作为预计生存天数
        estimated_days = min(food_days, energy_days, oxygen_days, water_days)
        
        return max(0, round(estimated_days, 1))
    
    @staticmethod
    def predict_timeline(status):
        """
        返回30/60/90/120天的预测值
        基于当前衰减率预测未来状态
        """
        crew_count = max(1, status.crew_count)
        
        # 计算每日衰减率
        daily_decay = {
            'food': 2.0 * crew_count / 4.0,
            'energy': 1.0,
            'oxygen': 0.5,
            'water': 1.5 * crew_count / 4.0,
            'medical': 0.3
        }
        
        # 预测各时间点的生存指数
        predictions = []
        for day in [30, 60, 90, 120]:
            # 计算各资源在目标天数的剩余量
            food_future = max(0, status.food_stability - daily_decay['food'] * day)
            energy_future = max(0, status.energy_level - daily_decay['energy'] * day)
            oxygen_future = max(0, status.oxygen_level - daily_decay['oxygen'] * day)
            water_future = max(0, status.water_reserve - daily_decay['water'] * day)
            medical_future = max(0, status.medical_safety - daily_decay['medical'] * day)
            
            # 计算预测的生存指数
            predicted_index = (
                food_future * 0.2 +
                medical_future * 0.3 +
                energy_future * 0.2 +
                oxygen_future * 0.2 +
                water_future * 0.1
            )
            
            predictions.append(round(max(0, predicted_index), 1))
        
        return predictions
    
    @staticmethod
    def generate_analysis_report(status):
        """生成生存状态分析报告"""
        survival_days = SurvivalPredictor.predict_survival_days(status)
        timeline = SurvivalPredictor.predict_timeline(status)
        
        report = {
            "estimated_survival_days": survival_days,
            "timeline_predictions": {
                "day_30": timeline[0],
                "day_60": timeline[1],
                "day_90": timeline[2],
                "day_120": timeline[3]
            },
            "critical_resources": [],
            "warnings": []
        }
        
        # 识别关键资源
        if status.food_stability < 30:
            report["critical_resources"].append("食物")
            report["warnings"].append("食物储备严重不足")
        if status.energy_level < 30:
            report["critical_resources"].append("能源")
            report["warnings"].append("能源水平危险")
        if status.oxygen_level < 50:
            report["critical_resources"].append("氧气")
            report["warnings"].append("氧气浓度偏低")
        if status.water_reserve < 40:
            report["critical_resources"].append("水资源")
            report["warnings"].append("水资源储备不足")
        
        return report
