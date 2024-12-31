import requests
import json

BASE_URL = "http://localhost:8000"

def test_user_flow():
    # 1. 使用用户名登录
    print("\n=== 使用用户名登录测试 ===")
    username_login_data = {
        "username": "testuser",
        "password": "123456"
    }
    username_response = requests.post(
        f"{BASE_URL}/api/user/login",
        data=username_login_data
    )
    print("状态码:", username_response.status_code)
    print("响应:", username_response.text)
    
    # 2. 使用邮箱登录
    print("\n=== 使用邮箱登录测试 ===")
    email_login_data = {
        "username": "newemail@example.com",  # 使用更新后的邮箱
        "password": "123456"
    }
    email_response = requests.post(
        f"{BASE_URL}/api/user/login",
        data=email_login_data
    )
    print("状态码:", email_response.status_code)
    print("响应:", email_response.text)
    
    # 如果登录成功，测试获取用户信息
    if email_response.status_code == 200:
        token = email_response.json()["access_token"]
        headers = {
            "Authorization": f"Bearer {token}",
            "accept": "application/json"
        }
        
        # 获取用户信息
        print("\n=== 获取用户信息测试 ===")
        profile_response = requests.get(
            f"{BASE_URL}/api/user/profile",
            headers=headers
        )
        print("状态码:", profile_response.status_code)
        print("响应:", profile_response.text)

if __name__ == "__main__":
    test_user_flow() 