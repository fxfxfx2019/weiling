"""
用户 API 测试
"""
import pytest
from httpx import AsyncClient

async def test_register_user_success(client):
    """测试用户注册成功"""
    response = await client.post("/api/auth/register", json={
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "password123",
        "nickname": "新用户"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "newuser"
    assert data["email"] == "newuser@example.com"
    assert "password" not in data

async def test_register_user_duplicate(client):
    """测试重复用户注册"""
    # 第一次注册
    await client.post("/api/auth/register", json={
        "username": "duplicate",
        "email": "duplicate@example.com",
        "password": "password123",
        "nickname": "重复用户"
    })
    
    # 重复注册
    response = await client.post("/api/auth/register", json={
        "username": "duplicate",
        "email": "duplicate@example.com",
        "password": "password123",
        "nickname": "重复用户"
    })
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"].lower()

async def test_register_user_invalid_data(client):
    """测试无效数据注册"""
    # 测试无效邮箱
    response = await client.post("/api/auth/register", json={
        "username": "invalid",
        "email": "invalid-email",
        "password": "password123",
        "nickname": "无效用户"
    })
    assert response.status_code == 422

    # 测试密码过短
    response = await client.post("/api/auth/register", json={
        "username": "invalid",
        "email": "invalid@example.com",
        "password": "123",
        "nickname": "无效用户"
    })
    assert response.status_code == 422

async def test_login_user_success(client):
    """测试用户登录成功"""
    # 先注册用户
    await client.post("/api/auth/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123",
        "nickname": "测试用户"
    })
    
    # 测试登录
    response = await client.post("/api/auth/login", json={
        "username": "testuser",
        "password": "password123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"

async def test_login_user_invalid(client):
    """测试无效登录"""
    # 测试错误密码
    response = await client.post("/api/auth/login", json={
        "username": "test_user",
        "password": "wrong_password"
    })
    assert response.status_code == 401
    
    # 测试不存在的用户
    response = await client.post("/api/auth/login", json={
        "username": "nonexistent",
        "password": "password123"
    })
    assert response.status_code == 401

async def test_get_user_me_success(client, user_token):
    """测试获取当前用户信息成功"""
    response = await client.get(
        "/api/user/me",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "test_user"
    assert data["email"] == "test@example.com"
    assert data["nickname"] == "测试用户"

async def test_get_user_me_invalid_token(client):
    """测试无效令牌获取用户信息"""
    response = await client.get(
        "/api/user/me",
        headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == 401

async def test_update_user_me_success(client, user_token):
    """测试更新当前用户信息成功"""
    response = await client.put(
        "/api/user/me",
        headers={"Authorization": f"Bearer {user_token}"},
        json={
            "nickname": "更新的昵称",
            "email": "updated@example.com"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["nickname"] == "更新的昵称"
    assert data["email"] == "updated@example.com"

async def test_update_user_me_invalid_data(client, user_token):
    """测试无效数据更新用户信息"""
    # 测试无效邮箱
    response = await client.put(
        "/api/user/me",
        headers={"Authorization": f"Bearer {user_token}"},
        json={
            "email": "invalid-email"
        }
    )
    assert response.status_code == 422

async def test_refresh_token_success(client):
    """测试刷新令牌成功"""
    # 先登录获取令牌
    login_response = await client.post("/api/auth/login", json={
        "username": "test_user",
        "password": "test123"
    })
    refresh_token = login_response.json()["refresh_token"]
    
    # 使用刷新令牌获取新的访问令牌
    response = await client.post(
        "/api/auth/refresh",
        json={"refresh_token": refresh_token}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

async def test_refresh_token_invalid(client):
    """测试无效的刷新令牌"""
    response = await client.post(
        "/api/auth/refresh",
        json={"refresh_token": "invalid_token"}
    )
    assert response.status_code == 401 