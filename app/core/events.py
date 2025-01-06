"""
应用事件处理
"""
import logging
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.database import db
from app.config import settings

logger = logging.getLogger(__name__)

async def startup_handler():
    """应用启动时的处理函数"""
    try:
        # 连接 MongoDB
        client = AsyncIOMotorClient(settings.MONGODB_URL)
        db.client = client
        db.database = client[settings.MONGODB_DB_NAME]
        
        # 创建索引
        await create_indexes()
        
        logger.info("应用启动成功")
    except Exception as e:
        logger.error(f"应用启动失败: {str(e)}")
        raise

async def shutdown_handler():
    """应用关闭时的处理函数"""
    try:
        # 关闭 MongoDB 连接
        if hasattr(db, "client"):
            db.client.close()
            
        logger.info("应用关闭成功")
    except Exception as e:
        logger.error(f"应用关闭失败: {str(e)}")
        raise

async def create_indexes():
    """创建数据库索引"""
    try:
        # 用户集合索引
        await db.database.users.create_index("username", unique=True)
        await db.database.users.create_index("email", unique=True)
        
        logger.info("数据库索引创建成功")
    except Exception as e:
        logger.error(f"创建索引失败: {str(e)}")
        raise 