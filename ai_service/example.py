"""
AI 服务使用示例
"""
import asyncio
from .ai_helper import ai_helper

async def main():
    # 示例代码
    code = """
def calculate_fibonacci(n: int) -> int:
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)
    """
    
    # 1. 代码解释
    print("\n=== 代码解释 ===")
    explanation = await ai_helper.explain_code(code)
    print(explanation)
    
    # 2. 代码优化
    print("\n=== 代码优化建议 ===")
    optimization = await ai_helper.optimize_code(code)
    print(optimization["suggestions"])
    
    # 3. 代码审查
    print("\n=== 代码审查 ===")
    review = await ai_helper.review_code(code)
    print(review["review"])
    
    # 4. 生成测试用例
    print("\n=== 测试用例生成 ===")
    test_cases = await ai_helper.generate_test_cases(code)
    print(test_cases["test_cases"])
    
    # 5. 询问具体问题
    print("\n=== 问题咨询 ===")
    question = "这个斐波那契数列实现的时间复杂度是多少？如何优化？"
    answer = await ai_helper.ask_code_question(question, code)
    print(answer)

if __name__ == "__main__":
    asyncio.run(main()) 