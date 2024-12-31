"""
配置模块
"""
from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # MongoDB配置
    MONGODB_URL: str = "mongodb://localhost:27017"
    MONGODB_DB_NAME: str = "weiling"
    
    # JWT配置
    JWT_SECRET_KEY: str = "your-super-secret-key-here"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # OpenAI配置
    OPENAI_API_KEY: Optional[str] = None
    
    # Redis配置
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: str = ""
    
    # AI配置
    ai_number_format: str = "{domain}-{personality}-{theme}-{level}{number:03d}"
    ai_name_format: str = "{domain}之{personality}-{theme}"
    
    # 缓存配置
    cache_ttl: int = 3600
    
    # 标签配置
    max_tags_basic: int = 3
    max_tags_advanced: int = 5
    
    class Config:
        env_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env")
        env_file_encoding = "utf-8"

settings = Settings() 