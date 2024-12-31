"""
用户模型
"""
from pydantic import BaseModel, EmailStr, Field, GetJsonSchemaHandler, validator
from typing import Optional, Any, Annotated
from datetime import datetime
from bson import ObjectId
from typing_extensions import Annotated
import re

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: Any, handler: GetJsonSchemaHandler
    ) -> dict[str, Any]:
        """自定义JSON Schema"""
        return {"type": "string"}

PydanticObjectId = Annotated[PyObjectId, Field(default_factory=PyObjectId)]

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    is_member: bool = False

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=20, pattern="^[a-zA-Z0-9_-]+$")
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=50)
    avatar: Optional[str] = None
    bind_status: bool = False
    sub_ai_id: Optional[str] = None

    @validator('username')
    def validate_username(cls, v):
        if not re.match("^[a-zA-Z0-9_-]+$", v):
            raise ValueError("用户名只能包含字母、数字、下划线和连字符")
        return v

    @validator('password')
    def validate_password(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError("密码必须包含至少一个大写字母")
        if not any(c.islower() for c in v):
            raise ValueError("密码必须包含至少一个小写字母")
        if not any(c.isdigit() for c in v):
            raise ValueError("密码必须包含至少一个数字")
        return v

    @validator('email')
    def validate_email_domain(cls, v):
        # 可以添加特定的邮箱域名验证
        allowed_domains = ['gmail.com', 'outlook.com', 'qq.com', '163.com', 'example.com']
        domain = v.split('@')[1].lower()
        if domain not in allowed_domains:
            raise ValueError(f"不支持的邮箱域名。支持的域名: {', '.join(allowed_domains)}")
        return v

class UserInDB(UserBase):
    id: PydanticObjectId = Field(alias="_id")
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_encoders = {ObjectId: str}
        populate_by_name = True

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=20, pattern="^[a-zA-Z0-9_-]+$")
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=6, max_length=50)
    avatar: Optional[str] = None

    @validator('username')
    def validate_username(cls, v):
        if v is not None and not re.match("^[a-zA-Z0-9_-]+$", v):
            raise ValueError("用户名只能包含字母、数字、下划线和连字符")
        return v

    @validator('password')
    def validate_password(cls, v):
        if v is not None:
            if not any(c.isupper() for c in v):
                raise ValueError("密码必须包含至少一个大写字母")
            if not any(c.islower() for c in v):
                raise ValueError("密码必须包含至少一个小写字母")
            if not any(c.isdigit() for c in v):
                raise ValueError("密码必须包含至少一个数字")
        return v

class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    avatar: Optional[str] = None
    bind_status: bool = False
    sub_ai_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    status: str = "active"
    version: int = 1

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str

class PasswordChange(BaseModel):
    """密码修改"""
    current_password: str = Field(..., min_length=6, max_length=50)
    new_password: str = Field(..., min_length=6, max_length=50)
    confirm_password: str = Field(..., min_length=6, max_length=50)
    
    @validator('new_password')
    def validate_new_password(cls, v, values):
        if 'current_password' in values and v == values['current_password']:
            raise ValueError("新密码不能与当前密码相同")
        if not any(c.isupper() for c in v):
            raise ValueError("密码必须包含至少一个大写字母")
        if not any(c.islower() for c in v):
            raise ValueError("密码必须包含至少一个小写字母")
        if not any(c.isdigit() for c in v):
            raise ValueError("密码必须包含至少一个数字")
        return v
    
    @validator('confirm_password')
    def validate_confirm_password(cls, v, values):
        if 'new_password' in values and v != values['new_password']:
            raise ValueError("两次输入的新密码不一致")
        return v 