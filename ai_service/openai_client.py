"""
OpenAI API 客户端
"""
import os
import json
from typing import List, Dict, Any, Optional
from openai import OpenAI, AsyncOpenAI
from dotenv import load_dotenv

class OpenAIClient:
    def __init__(self):
        # 加载环境变量
        load_dotenv()
        
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY 环境变量未设置")
            
        # 创建同步和异步客户端
        self.client = OpenAI(api_key=api_key)
        self.async_client = AsyncOpenAI(api_key=api_key)
        self.default_model = "o1-preview"  # 设置默认模型
        
    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: str = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        同步方式调用 ChatGPT
        """
        try:
            completion = self.client.chat.completions.create(
                model=model or self.default_model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return completion.choices[0].message.content
        except Exception as e:
            print(f"API 请求错误: {str(e)}")
            raise
        
    async def chat_completion_async(
        self,
        messages: List[Dict[str, str]],
        model: str = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        异步方式调用 ChatGPT
        """
        try:
            completion = await self.async_client.chat.completions.create(
                model=model or self.default_model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return completion.choices[0].message.content
        except Exception as e:
            print(f"API 请求错误: {str(e)}")
            raise
                
    def generate_image(
        self,
        prompt: str,
        size: str = "1024x1024",
        quality: str = "standard",
        n: int = 1
    ) -> List[str]:
        """
        生成图片
        
        Args:
            prompt: 图片描述
            size: 图片尺寸 ("1024x1024", "512x512", "256x256")
            quality: 图片质量 ("standard", "hd")
            n: 生成图片数量
            
        Returns:
            图片URL列表
        """
        try:
            response = self.client.images.generate(
                prompt=prompt,
                size=size,
                quality=quality,
                n=n
            )
            return [image.url for image in response.data]
        except Exception as e:
            print(f"图片生成错误: {str(e)}")
            raise
        
    async def generate_image_async(
        self,
        prompt: str,
        size: str = "1024x1024",
        quality: str = "standard",
        n: int = 1
    ) -> List[str]:
        """
        异步方式生成图片
        """
        try:
            response = await self.async_client.images.generate(
                prompt=prompt,
                size=size,
                quality=quality,
                n=n
            )
            return [image.url for image in response.data]
        except Exception as e:
            print(f"图片生成错误: {str(e)}")
            raise 