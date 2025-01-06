"""
安全模块
"""
from datetime import datetime, timedelta
from typing import Optional, Tuple
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt, ExpiredSignatureError
from passlib.context import CryptContext
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.config import Settings
from app.models.user import User
from app.core.database import get_db

# 密码加密上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 认证方案
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """获取密码哈希值"""
    return pwd_context.hash(password)

def create_token(
    data: dict,
    token_type: str = "access",
    expires_delta: Optional[timedelta] = None
) -> str:
    """创建令牌"""
    settings = Settings()
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        if token_type == "access":
            expire = datetime.utcnow() + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        else:  # refresh token
            expire = datetime.utcnow() + timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS)
    
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": token_type
    })
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt

def create_tokens(data: dict) -> Tuple[str, str]:
    """创建访问令牌和刷新令牌"""
    settings = Settings()
    access_token = create_token(
        data,
        token_type="access",
        expires_delta=timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    refresh_token = create_token(
        data,
        token_type="refresh",
        expires_delta=timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS)
    )
    return access_token, refresh_token

async def verify_token(
    token: str,
    token_type: str,
    db: AsyncIOMotorDatabase
) -> Optional[User]:
    """验证令牌"""
    settings = Settings()
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        
        # 验证令牌类型
        if payload.get("type") != token_type:
            return None
            
        username: str = payload.get("sub")
        if username is None:
            return None
        
        # 从数据库获取用户信息
        user = await db.users.find_one({"username": username})
        if user is None:
            return None
            
        # 转换ObjectId为字符串
        user["_id"] = str(user["_id"])
        return User(**user)
        
    except ExpiredSignatureError:
        # 令牌过期
        return None
    except JWTError:
        # 令牌无效
        return None

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncIOMotorDatabase = Depends(get_db)
) -> User:
    """获取当前用户"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无效的认证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    user = await verify_token(token, "access", db)
    if user is None:
        raise credentials_exception
        
    return user

async def refresh_access_token(
    refresh_token: str,
    db: AsyncIOMotorDatabase
) -> Optional[str]:
    """刷新访问令牌"""
    user = await verify_token(refresh_token, "refresh", db)
    if user is None:
        return None
        
    # 创建新的访问令牌
    access_token = create_token(
        {"sub": user.username},
        token_type="access"
    )
    return access_token 