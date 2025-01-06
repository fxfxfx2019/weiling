"""
数据库相关功能
"""
from typing import Optional, Dict, Any
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from fastapi import Depends

class Database:
    """数据库连接管理"""
    client = None
    database = None

# 全局数据库实例
db = Database()

async def get_db() -> AsyncIOMotorDatabase:
    """获取数据库连接"""
    return db.database

class BaseService:
    """基础服务类"""
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = None  # 子类需要设置具体的集合

    def _process_document(self, document: Dict[str, Any]) -> Dict[str, Any]:
        """处理文档，转换 ObjectId 为字符串"""
        if document and "_id" in document:
            document["_id"] = str(document["_id"])
        return document

    async def find_one(self, filter: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """查找单个文档"""
        if "_id" in filter and isinstance(filter["_id"], str):
            filter["_id"] = ObjectId(filter["_id"])
        result = await self.collection.find_one(filter)
        return self._process_document(result) if result else None

    async def insert_one(self, document: Dict[str, Any]) -> Dict[str, Any]:
        """插入单个文档"""
        # 添加时间戳
        document["created_at"] = datetime.utcnow()
        document["updated_at"] = document["created_at"]
        
        result = await self.collection.insert_one(document)
        created = await self.find_one({"_id": result.inserted_id})
        return created

    async def update_one(self, filter: Dict[str, Any], update: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """更新单个文档"""
        # 添加更新时间
        if "$set" in update:
            update["$set"]["updated_at"] = datetime.utcnow()
        else:
            update["$set"] = {"updated_at": datetime.utcnow()}
            
        if "_id" in filter and isinstance(filter["_id"], str):
            filter["_id"] = ObjectId(filter["_id"])
            
        await self.collection.update_one(filter, update)
        return await self.find_one(filter)

class UserService(BaseService):
    """用户服务类"""
    def __init__(self, db: AsyncIOMotorDatabase):
        super().__init__(db)
        self.collection = self.db.users

    async def find_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """通过用户名查找用户"""
        return await self.find_one({"username": username})

    async def find_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """通过邮箱查找用户"""
        return await self.find_one({"email": email})

    async def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """创建用户"""
        return await self.insert_one(user_data)

    async def update_user(self, user_id: str, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """更新用户信息"""
        return await self.update_one({"_id": user_id}, {"$set": update_data}) 