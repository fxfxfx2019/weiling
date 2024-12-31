"""
测试 AI 服务
"""
import asyncio
from ai_service.ai_helper import ai_helper

async def main():
    # 测试代码
    code = """
def calculate_fibonacci(n: int) -> int:
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)
    """
    
    try:
        # 测试代码解释功能
        print("\n=== 代码解释 ===")
        explanation = await ai_helper.explain_code(code)
        print(explanation)
        
    except Exception as e:
        print(f"发生错误: {str(e)}")
        if hasattr(e, 'response'):
            print(f"响应内容: {e.response.text}")

if __name__ == "__main__":
    asyncio.run(main()) 