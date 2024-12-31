import requests
import json
import time
import random
import string

class APITester:
    def __init__(self):
        self.base_url = "http://127.0.0.1:8000/api"
        self.access_token = None
        self.headers = {"Content-Type": "application/json"}
        self.username = self.generate_random_username()
    
    def generate_random_username(self):
        """生成随机用户名"""
        letters = string.ascii_lowercase
        return 'test_' + ''.join(random.choice(letters) for i in range(8))
    
    def update_auth_header(self, token):
        self.access_token = token
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
    
    def test_register(self):
        """测试用户注册"""
        print("\n=== 测试用户注册 ===")
        url = f"{self.base_url}/user/register"
        data = {
            "username": self.username,
            "email": f"{self.username}@example.com",
            "password": "Test123"
        }
        response = requests.post(url, json=data)
        print("状态码:", response.status_code)
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        return response.status_code == 200

    def test_login(self):
        """测试用户登录"""
        print("\n=== 测试用户登录 ===")
        url = f"{self.base_url}/user/login"
        data = {
            "username": self.username,
            "password": "Test123"
        }
        response = requests.post(url, json=data)
        print("状态码:", response.status_code)
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        
        if response.status_code == 200:
            token = response.json().get("access_token")
            self.update_auth_header(token)
            return True
        return False

    def test_create_ai(self):
        """测试创建AI实例"""
        print("\n=== 测试创建AI实例 ===")
        url = f"{self.base_url}/ai/create"
        data = {
            "domain": "科技",
            "personality": "专业",
            "theme": "人工智能",
            "level": "高级",
            "description": "一个专业的AI助手",
            "tags": ["AI", "机器学习", "深度学习"]
        }
        response = requests.post(url, json=data, headers=self.headers)
        print("状态码:", response.status_code)
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        return response.status_code == 200

    def test_start_conversation(self):
        """测试开始对话"""
        print("\n=== 测试开始对话 ===")
        url = f"{self.base_url}/conversation/start"
        data = {
            "ai_number": "科技-专业-人工智能-高级001",
            "initial_message": "你好，请介绍一下你自己"
        }
        response = requests.post(url, json=data, headers=self.headers)
        print("状态码:", response.status_code)
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        return response.status_code == 200

    def test_send_message(self):
        """测试发送消息"""
        print("\n=== 测试发送消息 ===")
        url = f"{self.base_url}/conversation/send"
        data = {
            "conversation_id": "1",
            "message": "请解释一下什么是机器学习？"
        }
        response = requests.post(url, json=data, headers=self.headers)
        print("状态码:", response.status_code)
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        return response.status_code == 200

    def test_get_memory(self):
        """测试获取记忆"""
        print("\n=== 测试获取记忆 ===")
        url = f"{self.base_url}/memory/get"
        params = {
            "ai_number": "科技-专业-人工智能-高级001"
        }
        response = requests.get(url, params=params, headers=self.headers)
        print("状态码:", response.status_code)
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        return response.status_code == 200

    def test_update_settings(self):
        """测试更新设置"""
        print("\n=== 测试更新设置 ===")
        url = f"{self.base_url}/settings/update"
        data = {
            "ai_number": "科技-专业-人工智能-高级001",
            "settings": {
                "temperature": 0.7,
                "max_tokens": 2000
            }
        }
        response = requests.post(url, json=data, headers=self.headers)
        print("状态码:", response.status_code)
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        return response.status_code == 200

def run_tests():
    tester = APITester()
    print(f"使用随机生成的用户名: {tester.username}")
    
    # 测试注册和登录
    if not tester.test_register():
        print("注册失败，跳过后续测试")
        return
    
    time.sleep(1)  # 等待数据库更新
    
    if not tester.test_login():
        print("登录失败，跳过后续测试")
        return
    
    time.sleep(1)
    
    # 测试其他功能
    tester.test_create_ai()
    time.sleep(1)
    
    tester.test_start_conversation()
    time.sleep(1)
    
    tester.test_send_message()
    time.sleep(1)
    
    tester.test_get_memory()
    time.sleep(1)
    
    tester.test_update_settings()

if __name__ == "__main__":
    print("开始测试所有API功能...")
    run_tests()
    print("\n测试完成！") 