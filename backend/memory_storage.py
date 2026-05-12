"""
深空AI生存系统 - 内存存储引擎（Vercel兼容版）
替代SQLite数据库，使用内存存储所有状态
"""
import datetime
import random

class MemoryStorage:
    """内存存储引擎 - 替代SQLite，兼容Vercel Serverless"""
    
    def __init__(self):
        # 初始化系统状态
        self._status = {
            'id': 1,
            'mission_day': 1,
            'survival_index': 98.0,
            'food_stability': 95.0,
            'medical_safety': 98.0,
            'energy_level': 92.0,
            'oxygen_level': 99.0,
            'co2_level': 0.04,
            'radiation_level': 0.0,
            'protein_level': 100.0,
            'water_reserve': 100.0,
            'medical_temp': -70.0,
            'humidity': 45.0,
            'pressure': 101.3,
            'backup_power_hours': 48.0,
            'crew_count': 4,
            'last_updated': datetime.datetime.utcnow()
        }
        
        # 日志记录
        self._logs = []
        
        # 添加初始日志
        self._add_log("INFO", "系统初始化完成，开始深空生存任务", "AI启动深空生存监控系统")
    
    def _add_log(self, log_type, message, ai_decision=None):
        """添加日志记录"""
        self._logs.append({
            'timestamp': datetime.datetime.utcnow(),
            'log_type': log_type,
            'message': message,
            'ai_decision': ai_decision
        })
        
        # 只保留最近50条日志
        if len(self._logs) > 50:
            self._logs = self._logs[-50:]
    
    def get_status(self):
        """获取当前状态（返回副本，避免直接修改）"""
        return self._status.copy()
    
    def update_status(self, updates):
        """更新状态"""
        self._status.update(updates)
        self._status['last_updated'] = datetime.datetime.utcnow()
    
    def get_logs(self, limit=20):
        """获取最近的日志"""
        return self._logs[-limit:]
    
    def add_log(self, log_type, message, ai_decision=None):
        """添加日志"""
        self._add_log(log_type, message, ai_decision)

# 全局单例实例
memory_storage = MemoryStorage()
