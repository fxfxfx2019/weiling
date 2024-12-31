"""
唯灵(weiling) - AI互动系统后端
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import Settings

app = FastAPI(
    title="唯灵API",
    description="唯灵(weiling) - AI互动系统后端API",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中需要指定具体的源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 加载配置
app.state.settings = Settings()

# 添加调试信息
print("=== Settings Debug Info ===")
print(f"Settings type: {type(app.state.settings)}")
print(f"Settings content: {app.state.settings.model_dump()}")
print("========================")

# MongoDB连接
@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(app.state.settings.MONGODB_URL)
    app.mongodb = app.mongodb_client[app.state.settings.MONGODB_DB_NAME]

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()

# 导入路由
from app.user.routes import router as user_router
from app.ai.routes import router as ai_router
from app.conversation.routes import router as conversation_router
from app.memory.routes import router as memory_router
from app.settings.routes import router as settings_router

# 注册路由
app.include_router(user_router, prefix="/api/user", tags=["用户"])
app.include_router(ai_router, prefix="/api/ai", tags=["AI"])
app.include_router(conversation_router, prefix="/api/conversation", tags=["对话"])
app.include_router(memory_router, prefix="/api/memory", tags=["记忆"])
app.include_router(settings_router, prefix="/api/settings", tags=["设置"]) 