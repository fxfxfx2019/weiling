import requests
import json
import time
import random
import string
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

class UserTester:
    def __init__(self):
        self.base_url = "http://127.0.0.1:8000/api/user"
        self.access_token = None
        self.headers = {"Content-Type": "application/json"}
        self.username = self.generate_random_username()
        
    def generate_random_username(self):
        """生成随机用户名"""
        letters = string.ascii_lowercase
        return 'test_' + ''.join(random.choice(letters) for i in range(8))
        
    def update_auth_header(self, token):
        """更新认证头"""
        self.access_token = token
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }

    def register(self):
        """用户注册"""
        url = f"{self.base_url}/register"
        data = {
            "username": self.username,
            "email": f"{self.username}@example.com",
            "password": "Test123"
        }
        try:
            response = requests.post(url, json=data)
            return {
                "success": response.status_code == 200,
                "status_code": response.status_code,
                "response": response.json()
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def login(self):
        """用户登录"""
        url = f"{self.base_url}/login"
        data = {
            "username": self.username,
            "password": "Test123"
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        try:
            response = requests.post(url, data=data, headers=headers)
            if response.status_code == 200:
                token = response.json().get("access_token")
                self.update_auth_header(token)
            return {
                "success": response.status_code == 200,
                "status_code": response.status_code,
                "response": response.json()
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def update_profile(self):
        """更新用户信息"""
        url = f"{self.base_url}/profile"
        data = {
            "nickname": f"昵称_{self.username}",
            "avatar": "https://example.com/avatar.jpg",
            "bio": "这是一个测试用户的简介"
        }
        try:
            response = requests.put(url, json=data, headers=self.headers)
            return {
                "success": response.status_code == 200,
                "status_code": response.status_code,
                "response": response.json()
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

def test_user_workflow():
    """测试单个用户的完整工作流程"""
    tester = UserTester()
    results = {
        "username": tester.username,
        "register": None,
        "login": None,
        "update": None
    }
    
    # 注册
    results["register"] = tester.register()
    if not results["register"]["success"]:
        return results
    
    time.sleep(0.5)  # 等待数据库更新
    
    # 登录
    results["login"] = tester.login()
    if not results["login"]["success"]:
        return results
    
    time.sleep(0.5)
    
    # 更新信息
    results["update"] = tester.update_profile()
    return results

def run_concurrent_tests(num_users=100):
    """运行并发测试"""
    print(f"\n=== 开始并发测试 ({num_users}个用户) ===")
    start_time = time.time()
    
    success_count = {
        "register": 0,
        "login": 0,
        "update": 0
    }
    
    error_count = {
        "register": 0,
        "login": 0,
        "update": 0
    }
    
    with ThreadPoolExecutor(max_workers=20) as executor:
        future_to_user = {executor.submit(test_user_workflow): i for i in range(num_users)}
        
        for future in as_completed(future_to_user):
            user_num = future_to_user[future]
            try:
                results = future.result()
                print(f"\n用户 {results['username']} 测试结果:")
                
                # 统计注册结果
                if results["register"]:
                    if results["register"]["success"]:
                        success_count["register"] += 1
                        print("✓ 注册成功")
                    else:
                        error_count["register"] += 1
                        print(f"✗ 注册失败: {results['register'].get('response', {}).get('detail', '未知错误')}")
                
                # 统计登录结果
                if results["login"]:
                    if results["login"]["success"]:
                        success_count["login"] += 1
                        print("✓ 登录成功")
                    else:
                        error_count["login"] += 1
                        print(f"✗ 登录失败: {results['login'].get('response', {}).get('detail', '未知错误')}")
                
                # 统计更新结果
                if results["update"]:
                    if results["update"]["success"]:
                        success_count["update"] += 1
                        print("✓ 更新信息成功")
                    else:
                        error_count["update"] += 1
                        print(f"✗ 更新信息失败: {results['update'].get('response', {}).get('detail', '未知错误')}")
                
            except Exception as e:
                print(f"用户 {user_num} 测试过程出现异常: {str(e)}")
    
    end_time = time.time()
    duration = end_time - start_time
    
    print("\n=== 测试统计 ===")
    print(f"总用时: {duration:.2f} 秒")
    print(f"平均每个用户用时: {duration/num_users:.2f} 秒")
    print("\n操作成功统计:")
    print(f"注册成功: {success_count['register']}/{num_users}")
    print(f"登录成功: {success_count['login']}/{num_users}")
    print(f"更新成功: {success_count['update']}/{num_users}")
    print("\n操作失败统计:")
    print(f"注册失败: {error_count['register']}/{num_users}")
    print(f"登录失败: {error_count['login']}/{num_users}")
    print(f"更新失败: {error_count['update']}/{num_users}")

if __name__ == "__main__":
    print("=== 用户系统并发测试 ===")
    print("测试内容：用户注册、登录和信息更新")
    print("并发用户数：100")
    run_concurrent_tests(100) 