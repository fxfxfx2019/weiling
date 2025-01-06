"""
FastAPI 应用实例
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.events import startup_handler, shutdown_handler
from app.api.auth import router as auth_router
from app.api.user import router as user_router

# 创建 FastAPI 应用实例
app = FastAPI(
    title="Weiling API",
    description="Weiling API documentation",
    version="1.0.0"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册事件处理器
app.add_event_handler("startup", startup_handler)
app.add_event_handler("shutdown", shutdown_handler)

# 注册路由
app.include_router(auth_router, prefix="/api/auth", tags=["认证"])
app.include_router(user_router, prefix="/api/user", tags=["用户"]) 