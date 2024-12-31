"""
用户路由
"""
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, status, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from typing import List
from app.user.models import UserCreate, UserResponse, UserUpdate, Token
from app.user.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    get_current_user
)
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register(request: Request, user: UserCreate):
    """用户注册"""
    db: AsyncIOMotorDatabase = request.app.mongodb
    
    # 检查用户名是否已存在
    if await db.users.find_one({"username": user.username}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名已存在"
        )
    
    # 检查邮箱是否已存在
    if await db.users.find_one({"email": user.email}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="邮箱已被注册"
        )
    
    # 创建新用户
    now = datetime.utcnow()
    user_dict = user.model_dump()
    user_dict["hashed_password"] = get_password_hash(user_dict.pop("password"))
    user_dict["created_at"] = now
    user_dict["updated_at"] = now
    user_dict["status"] = "active"
    user_dict["version"] = 1
    
    result = await db.users.insert_one(user_dict)
    
    # 获取创建的用户
    created_user = await db.users.find_one({"_id": result.inserted_id})
    created_user["id"] = str(created_user.pop("_id"))
    return UserResponse(**created_user)

@router.post("/login", response_model=Token)
async def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    """用户登录（支持用户名或邮箱登录）"""
    db: AsyncIOMotorDatabase = request.app.mongodb
    
    # 查找用户（支持用户名或邮箱）
    user = await db.users.find_one({
        "$or": [
            {"username": form_data.username},
            {"email": form_data.username}
        ]
    })
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名/邮箱或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 验证密码
    if not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名/邮箱或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 检查用户状态
    if user["status"] != "active":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="账户已被禁用",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 创建访问令牌
    access_token_expires = timedelta(
        minutes=request.app.state.settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
    )
    access_token = create_access_token(
        data={"sub": user["username"]},  # 统一使用username作为token的subject
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/profile", response_model=UserResponse)
async def get_profile(request: Request, current_user: dict = Depends(get_current_user)):
    """获取用户个人信息"""
    db: AsyncIOMotorDatabase = request.app.mongodb
    user = await db.users.find_one({"username": current_user.username})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    user["id"] = str(user.pop("_id"))
    return UserResponse(**user)

@router.put("/profile", response_model=UserResponse)
async def update_profile(
    request: Request,
    user_update: UserUpdate,
    current_user: dict = Depends(get_current_user)
):
    """更新用户个人信息"""
    db: AsyncIOMotorDatabase = request.app.mongodb
    
    # 准备更新数据
    update_data = user_update.model_dump(exclude_unset=True)
    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(
            update_data.pop("password")
        )
    update_data["updated_at"] = datetime.utcnow()
    update_data["version"] = await db.users.count_documents(
        {"username": current_user.username}
    ) + 1
    
    # 更新用户信息
    result = await db.users.update_one(
        {"username": current_user.username},
        {"$set": update_data}
    )
    
    if result.modified_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    # 获取更新后的用户信息
    updated_user = await db.users.find_one(
        {"username": current_user.username}
    )
    updated_user["id"] = str(updated_user.pop("_id"))
    return UserResponse(**updated_user) 