from ai_service.openai_client import OpenAIClient

def get_backend_structure():
    client = OpenAIClient()
    
    prompt = """基于以下需求，请详细设计Python后端架构：
    
    1. 项目名称：唯灵(weiling) - AI互动系统
    2. 核心功能：
       - 用户系统（普通用户/会员）
       - AI等级系统
       - 对话系统
       - 记忆管理
       - 个性化设置
    3. 技术要求：
       - Python 3.8+
       - MongoDB 4.4+
       - Docker容器化
       - JWT认证
       - 多重加密通讯
    
    请提供：
    1. 详细的目录结构
    2. 核心模块设计
    3. API接口设计
    4. 数据库模型设计
    5. 安全机制实现建议
    """
    
    response = client.chat_completion([
        {"role": "user", "content": prompt}
    ])
    
    print("=== OpenAI 后端架构建议 ===")
    print(response)
    
if __name__ == "__main__":
    get_backend_structure() 