"""
用户路由
"""
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, status, Depends, Request, UploadFile, File
from fastapi.security import OAuth2PasswordRequestForm
from typing import List
from pydantic import BaseModel
from app.user.models import UserCreate, UserResponse, UserUpdate, Token, PasswordChange
from app.user.security import (
    get_password_hash,
    verify_password,
    get_current_user
)
from app.user.jwt_handler import jwt_handler
from app.user.avatar import save_uploaded_avatar, generate_avatar
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId

class RefreshToken(BaseModel):
    refresh_token: str

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
    """用户登录"""
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
    
    # 创建访问令牌和刷新令牌
    access_token = jwt_handler.create_access_token(subject=user["username"])
    refresh_token = jwt_handler.create_refresh_token(subject=user["username"])
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/refresh", response_model=Token)
async def refresh_token(token_data: RefreshToken):
    """刷新访问令牌"""
    try:
        # 验证刷新令牌并获取新的访问令牌
        new_access_token = jwt_handler.refresh_access_token(token_data.refresh_token)
        return {
            "access_token": new_access_token,
            "refresh_token": token_data.refresh_token,  # 返回原有的刷新令牌
            "token_type": "bearer"
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="无效的刷新令牌"
        )

@router.get("/profile", response_model=UserResponse)
async def get_profile(request: Request, current_user: dict = Depends(get_current_user)):
    """获取用户信息"""
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

@router.post("/avatar/upload", response_model=UserResponse)
async def upload_avatar(
    request: Request,
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    """上传头像"""
    db: AsyncIOMotorDatabase = request.app.mongodb
    
    # 验证文件类型
    if not file.content_type.startswith('image/'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="只能上传图片文件"
        )
    
    # 保存头像
    avatar_path = await save_uploaded_avatar(file, current_user.username)
    
    # 更新用户头像
    result = await db.users.update_one(
        {"username": current_user.username},
        {"$set": {
            "avatar": avatar_path,
            "updated_at": datetime.utcnow()
        }}
    )
    
    if result.modified_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    # 获取更新后的用户信息
    updated_user = await db.users.find_one({"username": current_user.username})
    updated_user["id"] = str(updated_user.pop("_id"))
    return UserResponse(**updated_user)

@router.post("/avatar/generate", response_model=UserResponse)
async def generate_random_avatar(
    request: Request,
    current_user: dict = Depends(get_current_user)
):
    """生成随机头像"""
    db: AsyncIOMotorDatabase = request.app.mongodb
    
    # 生成头像
    avatar_path = generate_avatar(current_user.username)
    
    # 更新用户头像
    result = await db.users.update_one(
        {"username": current_user.username},
        {"$set": {
            "avatar": avatar_path,
            "updated_at": datetime.utcnow()
        }}
    )
    
    if result.modified_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    # 获取更新后的用户信息
    updated_user = await db.users.find_one({"username": current_user.username})
    updated_user["id"] = str(updated_user.pop("_id"))
    return UserResponse(**updated_user)

@router.post("/password/change")
async def change_password(
    request: Request,
    password_change: PasswordChange,
    current_user: dict = Depends(get_current_user)
):
    """修改密码"""
    db: AsyncIOMotorDatabase = request.app.mongodb
    
    # 获取用户信息
    user = await db.users.find_one({"username": current_user.username})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    # 验证当前密码
    if not verify_password(password_change.current_password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="当前密码错误"
        )
    
    # 更新密码
    hashed_password = get_password_hash(password_change.new_password)
    result = await db.users.update_one(
        {"username": current_user.username},
        {
            "$set": {
                "hashed_password": hashed_password,
                "updated_at": datetime.utcnow()
            }
        }
    )
    
    if result.modified_count == 0:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="密码更新失败"
        )
    
    return {"message": "密码修改成功"} 