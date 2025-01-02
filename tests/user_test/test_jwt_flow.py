"""
测试JWT认证流程
"""
import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:8000/api/user"

def test_jwt_flow():
    """测试JWT完整流程"""
    # 1. 注册新用户
    register_data = {
        "username": f"jwt_test_{int(datetime.now().timestamp())}",
        "email": f"jwt_test_{int(datetime.now().timestamp())}@example.com",
        "password": "Test123456"
    }
    
    print("\n1. 测试用户注册")
    print(f"请求数据: {json.dumps(register_data, indent=2, ensure_ascii=False)}")
    
    response = requests.post(f"{BASE_URL}/register", json=register_data)
    print(f"响应状态码: {response.status_code}")
    print(f"响应数据: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    assert response.status_code == 200, "注册失败"
    
    # 2. 用户登录，获取访问令牌和刷新令牌
    login_data = {
        "username": register_data["username"],
        "password": register_data["password"]
    }
    
    print("\n2. 测试用户登录")
    print(f"请求数据: {json.dumps(login_data, indent=2, ensure_ascii=False)}")
    
    response = requests.post(
        f"{BASE_URL}/login",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    print(f"响应状态码: {response.status_code}")
    print(f"响应数据: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    assert response.status_code == 200, "登录失败"
    tokens = response.json()
    access_token = tokens["access_token"]
    refresh_token = tokens["refresh_token"]
    
    # 3. 使用访问令牌获取用户信息
    print("\n3. 测试访问受保护的资源（获取用户信息）")
    response = requests.get(
        f"{BASE_URL}/profile",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    print(f"响应状态码: {response.status_code}")
    print(f"响应数据: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    assert response.status_code == 200, "获取用户信息失败"
    
    # 4. 使用刷新令牌获取新的访问令牌
    print("\n4. 测试刷新访问令牌")
    refresh_data = {"refresh_token": refresh_token}
    print(f"请求数据: {json.dumps(refresh_data, indent=2, ensure_ascii=False)}")
    
    response = requests.post(
        f"{BASE_URL}/refresh",
        json=refresh_data
    )
    print(f"响应状态码: {response.status_code}")
    print(f"响应数据: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    assert response.status_code == 200, "刷新令牌失败"
    new_access_token = response.json()["access_token"]
    
    # 5. 使用新的访问令牌获取用户信息
    print("\n5. 测试使用新的访问令牌")
    response = requests.get(
        f"{BASE_URL}/profile",
        headers={"Authorization": f"Bearer {new_access_token}"}
    )
    print(f"响应状态码: {response.status_code}")
    print(f"响应数据: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    assert response.status_code == 200, "使用新的访问令牌失败"
    
    # 6. 测试令牌错误的情况
    print("\n6. 测试使用错误的访问令牌")
    response = requests.get(
        f"{BASE_URL}/profile",
        headers={"Authorization": "Bearer wrong_token"}
    )
    print(f"响应状态码: {response.status_code}")
    print(f"响应数据: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    assert response.status_code == 401, "错误的令牌应该返回401"

if __name__ == "__main__":
    print("=== JWT认证流程测试 ===")
    try:
        test_jwt_flow()
        print("\n所有测试通过！")
    except AssertionError as e:
        print(f"\n测试失败: {str(e)}")
    except Exception as e:
        print(f"\n测试出错: {str(e)}") 