"""
应用配置
"""
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """应用配置类"""
    # MongoDB 配置
    MONGODB_URL: str = "mongodb://localhost:27017"
    MONGODB_DB_NAME: str = "weiling"
    
    # JWT 配置
    JWT_SECRET_KEY: str = "GkwMGGikJs5tGo2mnb-0_rPxY58P5fbTn26mXKn_Sr0"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7  # 刷新令牌7天过期

settings = Settings() 