"""
用户相关的路由
"""
from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.database import get_db, UserService
from app.core.auth import get_current_active_user
from app.core.security import get_password_hash
from app.models.user import User, UserUpdate

router = APIRouter()

async def get_user_service(db: AsyncIOMotorDatabase = Depends(get_db)) -> UserService:
    """获取用户服务"""
    return UserService(db)

@router.get("/me", response_model=User)
async def get_current_user_info(
    current_user: User = Depends(get_current_active_user)
):
    """获取当前用户信息"""
    return current_user

@router.put("/me", response_model=User)
async def update_current_user(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    user_service: UserService = Depends(get_user_service)
):
    """更新当前用户信息"""
    try:
        # 验证更新数据
        update_data = user_data.model_dump(exclude_unset=True)
        
        # 如果要更新用户名，检查是否已存在
        if "username" in update_data and update_data["username"] != current_user.username:
            if await user_service.find_by_username(update_data["username"]):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="用户名已存在"
                )
                
        # 如果要更新邮箱，检查是否已存在
        if "email" in update_data and update_data["email"] != current_user.email:
            if await user_service.find_by_email(update_data["email"]):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="邮箱已存在"
                )
        
        # 如果要更新密码，生成新的哈希值
        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
        
        # 更新用户信息
        user_id = current_user.model_dump(by_alias=True)["_id"]
        updated_user = await user_service.update_user(user_id, update_data)
        
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
            
        return User(**updated_user)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="更新用户信息失败"
        ) 