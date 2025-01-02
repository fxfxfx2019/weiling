"""
JWT处理模块
"""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from fastapi import HTTPException, status
from app.config import settings
from pydantic import BaseModel

class JWTTokenPayload(BaseModel):
    """JWT令牌载荷"""
    sub: str  # 用户标识（用户名）
    exp: datetime  # 过期时间
    iat: datetime  # 签发时间
    type: str  # 令牌类型：access 或 refresh
    jti: str  # JWT ID，用于令牌唯一标识

class JWTHandler:
    """JWT处理器"""
    
    def __init__(self):
        self.secret_key = settings.JWT_SECRET_KEY
        self.algorithm = settings.JWT_ALGORITHM
        self.access_token_expire_minutes = settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        self.refresh_token_expire_days = 7  # 刷新令牌7天有效期
    
    def create_access_token(self, subject: str) -> str:
        """
        创建访问令牌
        :param subject: 用户标识（通常是用户名）
        :return: JWT访问令牌
        """
        return self._create_token(
            subject=subject,
            token_type="access",
            expires_delta=timedelta(minutes=self.access_token_expire_minutes)
        )
    
    def create_refresh_token(self, subject: str) -> str:
        """
        创建刷新令牌
        :param subject: 用户标识（通常是用户名）
        :return: JWT刷新令牌
        """
        return self._create_token(
            subject=subject,
            token_type="refresh",
            expires_delta=timedelta(days=self.refresh_token_expire_days)
        )
    
    def _create_token(
        self,
        subject: str,
        token_type: str,
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """
        创建JWT令牌
        :param subject: 用户标识
        :param token_type: 令牌类型
        :param expires_delta: 过期时间增量
        :return: JWT令牌
        """
        if expires_delta is None:
            expires_delta = timedelta(minutes=15)
            
        now = datetime.utcnow()
        expires = now + expires_delta
        
        to_encode = {
            "sub": subject,
            "exp": expires,
            "iat": now,
            "type": token_type,
            "jti": f"{subject}-{now.timestamp()}"  # 创建唯一的token标识
        }
        
        return jwt.encode(
            to_encode,
            self.secret_key,
            algorithm=self.algorithm
        )
    
    def verify_token(self, token: str, token_type: str = "access") -> Dict[str, Any]:
        """
        验证JWT令牌
        :param token: JWT令牌
        :param token_type: 期望的令牌类型
        :return: 解码后的载荷
        """
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm]
            )
            
            # 验证令牌类型
            if payload.get("type") != token_type:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="无效的令牌类型",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            # 验证令牌是否过期
            exp = datetime.fromtimestamp(payload.get("exp"))
            if datetime.utcnow() >= exp:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="令牌已过期",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            return payload
            
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="无效的认证凭据",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    def refresh_access_token(self, refresh_token: str) -> str:
        """
        使用刷新令牌获取新的访问令牌
        :param refresh_token: 刷新令牌
        :return: 新的访问令牌
        """
        # 验证刷新令牌
        payload = self.verify_token(refresh_token, token_type="refresh")
        
        # 创建新的访问令牌
        return self.create_access_token(subject=payload["sub"])

# 创建全局JWT处理器实例
jwt_handler = JWTHandler() 