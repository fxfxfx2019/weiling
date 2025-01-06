"""
认证相关的路由
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.database import get_db, UserService
from app.core.auth import (
    authenticate_user,
    create_user_tokens,
    refresh_token as refresh_user_token
)
from app.core.security import get_password_hash
from app.models.user import User, UserCreate
from app.models.token import Token, TokenRefresh

router = APIRouter()

async def get_user_service(db: AsyncIOMotorDatabase = Depends(get_db)) -> UserService:
    """获取用户服务"""
    return UserService(db)

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """用户登录"""
    try:
        print(f"收到登录请求: username={form_data.username}")
        # 验证用户
        user = await authenticate_user(form_data.username, form_data.password, db)
        if not user:
            print("用户验证失败")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户名或密码错误"
            )
        
        print("用户验证成功，创建令牌")
        # 创建令牌
        tokens = await create_user_tokens(user)
        print("令牌创建成功")
        return tokens
    except HTTPException:
        raise
    except Exception as e:
        print(f"登录过程发生异常: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="登录过程发生错误"
        )

@router.post("/refresh", response_model=Token)
async def refresh_token(
    token_data: TokenRefresh,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """刷新访问令牌"""
    try:
        print("收到令牌刷新请求")
        tokens = await refresh_user_token(token_data.refresh_token, db)
        if not tokens:
            print("刷新令牌无效")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="无效的刷新令牌"
            )
        print("令牌刷新成功")
        return tokens
    except HTTPException:
        raise
    except Exception as e:
        print(f"刷新令牌过程发生异常: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="刷新令牌失败"
        )

@router.post("/register", response_model=User)
async def register(
    user_data: UserCreate,
    user_service: UserService = Depends(get_user_service)
):
    """用户注册"""
    try:
        print(f"收到注册请求: username={user_data.username}")
        # 检查用户名是否已存在
        if await user_service.find_by_username(user_data.username):
            print("用户名已存在")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="用户名已存在"
            )
        
        # 检查邮箱是否已存在
        if await user_service.find_by_email(user_data.email):
            print("邮箱已存在")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="邮箱已存在"
            )
        
        # 创建用户
        print("创建新用户")
        user_dict = user_data.model_dump()
        user_dict["hashed_password"] = get_password_hash(user_dict.pop("password"))
        user_dict["is_admin"] = False
        user_dict["is_active"] = True
        
        created_user = await user_service.create_user(user_dict)
        print(f"用户创建成功: {created_user}")
        return User(**created_user)
    except HTTPException:
        raise
    except Exception as e:
        print(f"注册过程发生异常: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="注册过程发生错误"
        ) 