"""
令牌相关的模型
"""
from pydantic import BaseModel, Field

class Token(BaseModel):
    """令牌模型"""
    access_token: str = Field(..., description="访问令牌")
    refresh_token: str = Field(..., description="刷新令牌")
    token_type: str = Field(..., description="令牌类型")

class TokenRefresh(BaseModel):
    """令牌刷新模型"""
    refresh_token: str = Field(..., description="刷新令牌") 