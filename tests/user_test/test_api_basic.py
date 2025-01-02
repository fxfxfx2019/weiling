"""
基础API测试
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def test_user_flow():
    """测试用户基本功能流程"""
    # 生成测试用户数据
    timestamp = int(datetime.now().timestamp()) % 10000  # 限制时间戳长度
    test_user = {
        "username": f"basic_{timestamp}",  # 缩短用户名
        "email": f"basic_{timestamp}@example.com",
        "password": "Test123456"
    }
    
    # 1. 注册测试用户
    print("\n=== 注册测试用户 ===")
    register_response = requests.post(
        f"{BASE_URL}/api/user/register",
        json=test_user
    )
    print("状态码:", register_response.status_code)
    print("响应:", register_response.text)
    
    assert register_response.status_code == 200, "注册失败"
    
    # 2. 使用用户名登录
    print("\n=== 使用用户名登录测试 ===")
    username_login_data = {
        "username": test_user["username"],
        "password": test_user["password"]
    }
    username_response = requests.post(
        f"{BASE_URL}/api/user/login",
        data=username_login_data
    )
    print("状态码:", username_response.status_code)
    print("响应:", username_response.text)
    
    assert username_response.status_code == 200, "用户名登录失败"
    username_token = username_response.json()["access_token"]
    
    # 3. 使用邮箱登录
    print("\n=== 使用邮箱登录测试 ===")
    email_login_data = {
        "username": test_user["email"],
        "password": test_user["password"]
    }
    email_response = requests.post(
        f"{BASE_URL}/api/user/login",
        data=email_login_data
    )
    print("状态码:", email_response.status_code)
    print("响应:", email_response.text)
    
    assert email_response.status_code == 200, "邮箱登录失败"
    email_token = email_response.json()["access_token"]
    
    # 4. 使用用户名登录的token获取用户信息
    print("\n=== 使用用户名登录token获取用户信息 ===")
    username_profile_response = requests.get(
        f"{BASE_URL}/api/user/profile",
        headers={
            "Authorization": f"Bearer {username_token}",
            "accept": "application/json"
        }
    )
    print("状态码:", username_profile_response.status_code)
    print("响应:", username_profile_response.text)
    
    assert username_profile_response.status_code == 200, "获取用户信息失败"
    
    # 5. 使用邮箱登录的token获取用户信息
    print("\n=== 使用邮箱登录token获取用户信息 ===")
    email_profile_response = requests.get(
        f"{BASE_URL}/api/user/profile",
        headers={
            "Authorization": f"Bearer {email_token}",
            "accept": "application/json"
        }
    )
    print("状态码:", email_profile_response.status_code)
    print("响应:", email_profile_response.text)
    
    assert email_profile_response.status_code == 200, "获取用户信息失败"
    
    print("\n所有测试通过！")

if __name__ == "__main__":
    try:
        test_user_flow()
    except AssertionError as e:
        print(f"\n测试失败: {str(e)}")
    except Exception as e:
        print(f"\n测试出错: {str(e)}") 