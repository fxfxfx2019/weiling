"""
AI 助手服务模块
提供统一的 AI 服务接口，包括代码辅助、问题咨询等功能
"""
from typing import List, Optional, Dict, Any
from .openai_client import OpenAIClient
import json

class AIHelper:
    def __init__(self):
        self.client = OpenAIClient()
        
    async def ask_code_question(self, 
        question: str, 
        code_context: Optional[str] = None,
        language: str = "python"
    ) -> str:
        """
        询问代码相关问题
        
        Args:
            question: 具体的问题
            code_context: 相关的代码上下文
            language: 编程语言
        
        Returns:
            AI 的回答
        """
        messages = []
        
        # 设置系统角色
        messages.append({
            "role": "system",
            "content": f"你是一个专业的{language}开发助手，请帮助用户解决代码相关问题。请给出详细的解释和具体的代码示例。"
        })
        
        # 如果有代码上下文，添加到消息中
        if code_context:
            messages.append({
                "role": "user",
                "content": f"这是相关的代码上下文:\n```{language}\n{code_context}\n```"
            })
        
        # 添加用户问题
        messages.append({
            "role": "user",
            "content": question
        })
        
        response = await self.client.chat_completion_async(messages)
        return response

    async def review_code(self, 
        code: str, 
        language: str = "python",
        focus_aspects: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        代码审查
        
        Args:
            code: 要审查的代码
            language: 编程语言
            focus_aspects: 重点关注的方面，如 ["性能", "安全性", "可读性"]
        
        Returns:
            包含审查结果的字典
        """
        aspects = focus_aspects or ["代码质量", "性能", "安全性", "可读性", "最佳实践"]
        aspects_str = "、".join(aspects)
        
        messages = [
            {
                "role": "system",
                "content": f"你是一个专业的代码审查专家，请从{aspects_str}等方面对以下代码进行审查。"
            },
            {
                "role": "user",
                "content": f"请审查这段代码:\n```{language}\n{code}\n```"
            }
        ]
        
        response = await self.client.chat_completion_async(messages)
        return {
            "review": response,
            "aspects": aspects
        }

    async def optimize_code(self, 
        code: str, 
        language: str = "python",
        optimization_goals: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        代码优化
        
        Args:
            code: 要优化的代码
            language: 编程语言
            optimization_goals: 优化目标，如 ["性能", "内存使用", "可读性"]
        
        Returns:
            包含优化建议和优化后代码的字典
        """
        goals = optimization_goals or ["性能", "可读性", "可维护性"]
        goals_str = "、".join(goals)
        
        messages = [
            {
                "role": "system",
                "content": f"你是一个代码优化专家，请从{goals_str}等方面对代码进行优化，并说明优化原因。"
            },
            {
                "role": "user",
                "content": f"请优化这段代码:\n```{language}\n{code}\n```"
            }
        ]
        
        response = await self.client.chat_completion_async(messages)
        return {
            "suggestions": response,
            "optimization_goals": goals
        }

    async def explain_code(self, 
        code: str, 
        language: str = "python",
        detail_level: str = "detailed"
    ) -> str:
        """
        代码解释
        
        Args:
            code: 要解释的代码
            language: 编程语言
            detail_level: 解释详细程度 ("brief", "normal", "detailed")
        
        Returns:
            代码解释
        """
        detail_prompts = {
            "brief": "请简要解释这段代码的主要功能",
            "normal": "请解释这段代码的功能和关键部分",
            "detailed": "请详细解释这段代码的每个部分，包括实现原理和注意事项"
        }
        
        messages = [
            {
                "role": "system",
                "content": "你是一个专业的代码讲师，请用清晰易懂的方式解释代码。"
            },
            {
                "role": "user",
                "content": f"{detail_prompts.get(detail_level, detail_prompts['normal'])}"
                          f":\n```{language}\n{code}\n```"
            }
        ]
        
        response = await self.client.chat_completion_async(messages)
        return response

    async def generate_test_cases(self, 
        code: str, 
        language: str = "python",
        test_types: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        生成测试用例
        
        Args:
            code: 要测试的代码
            language: 编程语言
            test_types: 测试类型，如 ["单元测试", "集成测试", "边界测试"]
        
        Returns:
            包含测试用例的字典
        """
        types = test_types or ["单元测试", "功能测试", "边界测试"]
        types_str = "、".join(types)
        
        messages = [
            {
                "role": "system",
                "content": f"你是一个测试专家，请为以下代码生成{types_str}等类型的测试用例。"
            },
            {
                "role": "user",
                "content": f"请为这段代码生成测试用例:\n```{language}\n{code}\n```"
            }
        ]
        
        response = await self.client.chat_completion_async(messages)
        return {
            "test_cases": response,
            "test_types": types
        }

    async def debug_code(self, 
        code: str, 
        error_message: Optional[str] = None,
        language: str = "python"
    ) -> Dict[str, Any]:
        """
        代码调试辅助
        
        Args:
            code: 有问题的代码
            error_message: 错误信息
            language: 编程语言
        
        Returns:
            包含调试建议和可能的解决方案的字典
        """
        messages = [
            {
                "role": "system",
                "content": "你是一个调试专家，请帮助分析代码问题并提供解决方案。"
            },
            {
                "role": "user",
                "content": f"这段代码有问题:\n```{language}\n{code}\n```"
            }
        ]
        
        if error_message:
            messages.append({
                "role": "user",
                "content": f"错误信息是:\n{error_message}"
            })
        
        response = await self.client.chat_completion_async(messages)
        return {
            "analysis": response,
            "has_error_message": bool(error_message)
        }

# 创建全局单例实例
ai_helper = AIHelper() 