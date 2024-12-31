"""
测试用户API
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000/api"

def test_user_flow():
    # 1. 注册新用户
    register_data = {
        "username": f"testuser_{int(datetime.now().timestamp())}",  # 使用时间戳确保用户名唯一
        "email": f"test_{int(datetime.now().timestamp())}@example.com",
        "password": "Test123456"
    }
    
    print("\n1. 测试用户注册")
    print(f"请求数据: {json.dumps(register_data, indent=2, ensure_ascii=False)}")
    
    response = requests.post(f"{BASE_URL}/user/register", json=register_data)
    print(f"响应状态码: {response.status_code}")
    print(f"响应数据: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    assert response.status_code == 200, "注册失败"
    
    # 2. 用户登录
    login_data = {
        "username": register_data["username"],
        "password": register_data["password"]
    }
    
    print("\n2. 测试用户登录")
    print(f"请求数据: {json.dumps(login_data, indent=2, ensure_ascii=False)}")
    
    response = requests.post(
        f"{BASE_URL}/user/login",
        data=login_data,  # 注意：登录接口使用form-data格式
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    print(f"响应状态码: {response.status_code}")
    print(f"响应数据: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    assert response.status_code == 200, "登录失败"
    token = response.json()["access_token"]
    
    # 3. 修改密码
    change_password_data = {
        "current_password": register_data["password"],
        "new_password": "NewTest123456",
        "confirm_password": "NewTest123456"
    }
    
    print("\n3. 测试密码修改")
    print(f"请求数据: {json.dumps(change_password_data, indent=2, ensure_ascii=False)}")
    
    response = requests.post(
        f"{BASE_URL}/user/password/change",
        json=change_password_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    print(f"响应状态码: {response.status_code}")
    print(f"响应数据: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    assert response.status_code == 200, "密码修改失败"
    
    # 4. 使用新密码登录验证
    login_data["password"] = change_password_data["new_password"]
    
    print("\n4. 测试新密码登录")
    print(f"请求数据: {json.dumps(login_data, indent=2, ensure_ascii=False)}")
    
    response = requests.post(
        f"{BASE_URL}/user/login",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    print(f"响应状态码: {response.status_code}")
    print(f"响应数据: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    assert response.status_code == 200, "新密码登录失败"

if __name__ == "__main__":
    try:
        test_user_flow()
        print("\n所有测试通过！")
    except AssertionError as e:
        print(f"\n测试失败: {str(e)}")
    except Exception as e:
        print(f"\n测试出错: {str(e)}") 