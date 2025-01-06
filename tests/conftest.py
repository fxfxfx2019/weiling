"""
测试配置文件
"""
import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = str(Path(__file__).parent.parent)
sys.path.insert(0, project_root)

import pytest
import asyncio
from datetime import datetime
from fastapi.testclient import TestClient
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.security import create_access_token, get_password_hash
from app import create_app
from app.config import Settings

# 测试环境配置
class TestSettings(Settings):
    """测试配置"""
    MONGODB_URL: str = "mongodb://localhost:27017"
    MONGODB_DB_NAME: str = "weiling_test"
    JWT_SECRET_KEY: str = "test-secret-key"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60

settings = TestSettings()

@pytest.fixture(scope="session")
def event_loop():
    """创建事件循环"""
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
def app():
    """创建测试应用实例"""
    app = create_app()
    
    # 修改数据库连接为测试数据库
    app.mongodb_client = AsyncIOMotorClient(settings.MONGODB_URL)
    app.mongodb = app.mongodb_client[settings.MONGODB_DB_NAME]
    
    # 创建启动完成事件
    app.state.startup_complete = asyncio.Event()
    app.state.startup_complete.set()
    
    return app

@pytest.fixture
def client(app):
    """创建测试客户端"""
    with TestClient(app) as client:
        yield client

@pytest.fixture
def user_token():
    """创建测试用户token"""
    return create_access_token(
        data={
            "sub": "test_user",
            "is_admin": False
        },
        expires_delta=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

@pytest.fixture(autouse=True, scope="function")
async def setup_db(app):
    """设置测试数据库"""
    # 清空测试数据库中的所有集合
    collections = await app.mongodb.list_collection_names()
    for collection in collections:
        await app.mongodb[collection].delete_many({})
    
    # 创建测试用户
    current_time = datetime.utcnow()
    await app.mongodb.users.insert_one({
        "username": "test_user",
        "email": "test@example.com",
        "hashed_password": get_password_hash("test123"),
        "nickname": "测试用户",
        "is_admin": False,
        "is_active": True,
        "created_at": current_time,
        "updated_at": current_time
    })
    
    yield
    
    # 测试后清理数据
    collections = await app.mongodb.list_collection_names()
    for collection in collections:
        await app.mongodb[collection].delete_many({}) 