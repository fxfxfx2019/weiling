"""
用户服务层
处理用户相关的业务逻辑
"""
from datetime import datetime
from typing import Optional, Dict, Any

from app.core.database import BaseService
from app.core.security import get_password_hash, verify_password

class UserService(BaseService):
    """用户服务"""
    
    def __init__(self, db):
        super().__init__(db, "users")
    
    async def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """创建新用户"""
        # 检查用户名是否已存在
        if await self.find_one({"username": user_data["username"]}):
            raise ValueError("Username already exists")
        
        # 检查邮箱是否已存在
        if await self.find_one({"email": user_data["email"]}):
            raise ValueError("Email already exists")
        
        # 处理用户数据
        current_time = datetime.utcnow()
        user_dict = {
            "username": user_data["username"],
            "email": user_data["email"],
            "nickname": user_data["nickname"],
            "hashed_password": get_password_hash(user_data["password"]),
            "is_active": True,
            "is_admin": False,
            "created_at": current_time,
            "updated_at": current_time
        }
        
        # 创建用户
        result = await self.insert_one(user_dict)
        user_dict["_id"] = str(result.inserted_id)
        del user_dict["hashed_password"]
        
        return user_dict
    
    async def authenticate_user(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """验证用户"""
        user = await self.find_one({"username": username})
        if not user:
            return None
        
        if not verify_password(password, user["hashed_password"]):
            return None
        
        return user
    
    async def update_user(self, user_id: str, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """更新用户信息"""
        # 处理更新数据
        update_dict = {
            "updated_at": datetime.utcnow()
        }
        
        if "email" in update_data:
            # 检查新邮箱是否已被使用
            existing = await self.find_one({
                "email": update_data["email"],
                "_id": {"$ne": user_id}
            })
            if existing:
                raise ValueError("Email already exists")
            update_dict["email"] = update_data["email"]
        
        if "nickname" in update_data:
            update_dict["nickname"] = update_data["nickname"]
        
        if "password" in update_data:
            update_dict["hashed_password"] = get_password_hash(update_data["password"])
        
        # 更新用户
        result = await self.update_one(
            {"_id": user_id},
            {"$set": update_dict}
        )
        
        if result:
            user = await self.find_one({"_id": user_id})
            if user:
                del user["hashed_password"]
                return user
        
        return None 