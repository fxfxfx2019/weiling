"""
用户相关的数据模型
"""
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class UserBase(BaseModel):
    """用户基础模型"""
    username: str = Field(..., min_length=3, max_length=20)
    email: EmailStr
    nickname: str = Field(..., min_length=2, max_length=20)

class UserCreate(UserBase):
    """用户创建模型"""
    password: str = Field(..., min_length=6, max_length=20)

class UserUpdate(BaseModel):
    """用户更新模型"""
    email: Optional[EmailStr] = None
    nickname: Optional[str] = Field(None, min_length=2, max_length=20)
    password: Optional[str] = Field(None, min_length=6, max_length=20)

class User(UserBase):
    """用户模型"""
    id: str = Field(alias="_id")
    is_admin: bool = False
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }
        populate_by_name = True 