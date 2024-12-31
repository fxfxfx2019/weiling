from ai_service.openai_client import OpenAIClient

def get_startup_fix():
    client = OpenAIClient()
    
    error_message = """
在Python FastAPI项目中遇到一个奇怪的问题：

1. 调试信息显示settings对象是正确的：
```
=== Settings Debug Info ===
Settings type: <class 'app.config.Settings'>
Settings content: {
    'MONGODB_URL': 'mongodb://localhost:27017',
    'MONGODB_DB_NAME': 'weiling',
    'JWT_SECRET_KEY': 'your-super-secret-key-here',
    'JWT_ALGORITHM': 'HS256',
    'JWT_ACCESS_TOKEN_EXPIRE_MINUTES': 30
}
========================
```

2. 但是仍然遇到错误：
```
ERROR:    Application startup failed. Exiting.
Traceback (most recent call last):
  File "app/__init__.py", line 34, in startup_db_client
    app.mongodb_client = AsyncIOMotorClient(settings.MONGODB_URL)
AttributeError: module 'app.settings' has no attribute 'MONGODB_URL'
```

3. 相关代码：
app/__init__.py:
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

# 添加调试信息
print("=== Settings Debug Info ===")
print(f"Settings type: {type(settings)}")
print(f"Settings content: {settings.model_dump()}")
print("========================")

@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(settings.MONGODB_URL)
    app.mongodb = app.mongodb_client[settings.MONGODB_DB_NAME]
```

app/config/__init__.py:
```python
from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    MONGODB_URL: str = "mongodb://localhost:27017"
    MONGODB_DB_NAME: str = "weiling"
    
    class Config:
        env_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env")
        env_file_encoding = "utf-8"

settings = Settings()
```

这很奇怪，因为：
1. 调试信息显示settings对象确实包含MONGODB_URL
2. 但是在startup_db_client函数中却无法访问这个属性
3. 错误信息提到"module 'app.settings'"，但我们实际上是从'app.config'导入的

请分析这个问题并提供解决方案。
"""
    
    response = client.chat_completion([
        {"role": "user", "content": error_message}
    ])
    
    print("=== OpenAI 解决方案 ===")
    print(response)

if __name__ == "__main__":
    get_startup_fix() 