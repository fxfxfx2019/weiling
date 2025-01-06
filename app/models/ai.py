"""
AI 模型定义
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from bson import ObjectId

class AIBase(BaseModel):
    """AI基础模型"""
    number: str = Field(..., description="AI编号")
    name: str = Field(..., description="AI名称")
    domain: str = Field(..., description="领域")
    personality: str = Field(..., description="性格特征")
    theme: str = Field(..., description="主题特征")
    level: str = Field(..., description="等级")
    avatar: Optional[str] = Field(None, description="头像URL")
    description: Optional[str] = Field(None, description="描述")
    tags: List[str] = Field(default=[], description="标签")
    
class AICreate(AIBase):
    """创建AI时的模型"""
    owner_id: Optional[str] = Field(None, description="拥有者ID")
    
class AIAdoption(BaseModel):
    """AI领养申请模型"""
    user_id: str = Field(..., description="申请用户ID")
    ai_id: str = Field(..., description="AI ID")
    reason: str = Field(..., description="申请理由")
    status: str = Field(default="pending", description="申请状态")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class AI(AIBase):
    """AI完整模型"""
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id", description="AI ID")
    owner_id: Optional[str] = Field(None, description="拥有者ID")
    status: str = Field(default="available", description="AI状态")
    adoption_count: int = Field(default=0, description="被领养次数")
    interaction_count: int = Field(default=0, description="互动次数")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_interaction: Optional[datetime] = Field(None, description="最后互动时间")
    version: int = Field(default=1, description="版本号")
    is_active: bool = Field(default=True, description="是否激活")

    class Config:
        """配置"""
        populate_by_name = True
        json_encoders = {
            ObjectId: str
        }
        
class AIUpdate(BaseModel):
    """AI更新模型"""
    name: Optional[str] = Field(None, description="AI名称")
    domain: Optional[str] = Field(None, description="领域")
    personality: Optional[str] = Field(None, description="性格特征")
    theme: Optional[str] = Field(None, description="主题特征")
    level: Optional[str] = Field(None, description="等级")
    avatar: Optional[str] = Field(None, description="头像URL")
    description: Optional[str] = Field(None, description="描述")
    tags: Optional[List[str]] = Field(None, description="标签")
    status: Optional[str] = Field(None, description="AI状态")

class AIInteraction(BaseModel):
    """AI互动记录模型"""
    ai_id: str = Field(..., description="AI ID")
    user_id: str = Field(..., description="用户ID")
    content: str = Field(..., description="互动内容")
    type: str = Field(..., description="互动类型")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    response: Optional[str] = Field(None, description="AI响应")
    
class AIMemory(BaseModel):
    """AI记忆模型"""
    ai_id: str = Field(..., description="AI ID")
    user_id: str = Field(..., description="用户ID")
    content: str = Field(..., description="记忆内容")
    type: str = Field(..., description="记忆类型")
    importance: int = Field(default=1, description="重要程度")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_recalled: Optional[datetime] = Field(None, description="最后回忆时间")
    recall_count: int = Field(default=0, description="回忆次数") 