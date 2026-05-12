import os
import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 使用绝对路径确保数据库文件在正确的位置
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "survival_system.db")
DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class SurvivalStatus(Base):
    __tablename__ = "survival_status"

    id = Column(Integer, primary_key=True, index=True)
    mission_day = Column(Integer, default=1)
    survival_index = Column(Float, default=100.0)
    food_stability = Column(Float, default=100.0)
    medical_safety = Column(Float, default=100.0)
    energy_level = Column(Float, default=100.0)
    oxygen_level = Column(Float, default=100.0)
    co2_level = Column(Float, default=0.04)
    radiation_level = Column(Float, default=0.0)
    protein_level = Column(Float, default=100.0)
    water_reserve = Column(Float, default=100.0)
    medical_temp = Column(Float, default=-70.0)  # 医疗冷链温度
    humidity = Column(Float, default=45.0)
    pressure = Column(Float, default=101.3)
    backup_power_hours = Column(Float, default=48.0)
    crew_count = Column(Integer, default=4)
    last_updated = Column(DateTime, default=datetime.datetime.utcnow)

class ResourceLog(Base):
    __tablename__ = "resource_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    log_type = Column(String)  # INFO, WARNING, CRITICAL
    message = Column(String)
    ai_decision = Column(String, nullable=True)

Base.metadata.create_all(bind=engine)
