"""
认证相关的功能
"""
from typing import Optional, Dict
from fastapi import Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.database import get_db
from app.core.security import (
    verify_password,
    get_current_user,
    create_tokens,
    refresh_access_token
)
from app.models.user import User
from app.models.token import Token

class AuthError(Exception):
    """认证错误"""
    def __init__(self, detail: str):
        self.detail = detail

async def authenticate_user(
    username: str,
    password: str,
    db: AsyncIOMotorDatabase
) -> Optional[User]:
    """验证用户"""
    try:
        print(f"尝试验证用户: {username}")
        user = await db.users.find_one({"username": username})
        
        if not user:
            print(f"用户不存在: {username}")
            raise AuthError("用户名或密码错误")
            
        print(f"找到用户: {user}")
        print(f"验证密码: 输入={password}, 存储={user.get('hashed_password', 'None')}")
            
        if not verify_password(password, user["hashed_password"]):
            print("密码验证失败")
            raise AuthError("用户名或密码错误")
            
        if not user.get("is_active", True):
            print("用户已被禁用")
            raise AuthError("用户已被禁用")
            
        print("用户验证成功")
        user["_id"] = str(user["_id"])
        return User(**user)
    except AuthError as e:
        print(f"认证错误: {e.detail}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.detail
        )
    except Exception as e:
        print(f"认证过程发生异常: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="认证过程发生错误"
        )

async def create_user_tokens(user: User) -> Dict[str, str]:
    """创建用户令牌"""
    try:
        print(f"为用户创建令牌: {user.username}")
        access_token, refresh_token = create_tokens({"sub": user.username})
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
    except Exception as e:
        print(f"创建令牌失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="创建令牌失败"
        )

async def get_current_active_user(
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
) -> User:
    """获取当前活跃用户"""
    try:
        print(f"获取活跃用户: {current_user.username}")
        user = await db.users.find_one({"username": current_user.username})
        if not user:
            print("用户不存在")
            raise AuthError("用户不存在")
            
        if not user.get("is_active", True):
            print("用户已被禁用")
            raise AuthError("用户已被禁用")
            
        print("获取活跃用户成功")
        user["_id"] = str(user["_id"])
        return User(**user)
    except AuthError as e:
        print(f"获取活跃用户错误: {e.detail}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.detail
        )
    except Exception as e:
        print(f"获取用户信息失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取用户信息失败"
        )

async def get_current_admin_user(
    current_user: User = Depends(get_current_active_user)
) -> User:
    """获取当前管理员用户"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="需要管理员权限"
        )
    return current_user

async def refresh_token(
    refresh_token: str,
    db: AsyncIOMotorDatabase
) -> Optional[Dict[str, str]]:
    """刷新令牌"""
    try:
        print("尝试刷新令牌")
        new_access_token = await refresh_access_token(refresh_token, db)
        if not new_access_token:
            print("无效的刷新令牌")
            raise AuthError("无效的刷新令牌")
            
        print("令牌刷新成功")
        return {
            "access_token": new_access_token,
            "token_type": "bearer"
        }
    except AuthError as e:
        print(f"刷新令牌错误: {e.detail}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.detail
        )
    except Exception as e:
        print(f"刷新令牌失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="刷新令牌失败"
        ) 