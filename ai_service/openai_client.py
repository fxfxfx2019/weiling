from openai import OpenAI
from dotenv import load_dotenv
import os
from typing import List, Dict, Any, Optional

class OpenAIClient:
    """OpenAI API客户端封装类"""
    
    def __init__(self):
        # 加载环境变量
        load_dotenv()
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )
    
    def chat_completion(
        self, 
        messages: List[Dict[str, str]], 
        model: str = "gpt-3.5-turbo",
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        调用OpenAI聊天补全API
        
        Args:
            messages: 消息列表
            model: 模型名称
            temperature: 温度参数(0-1)
            max_tokens: 最大token数
            
        Returns:
            str: AI响应的文本
        """
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenAI API调用出错: {e}")
            return f"错误: {str(e)}"
            
    def generate_image(
        self,
        prompt: str,
        size: str = "1024x1024",
        quality: str = "standard",
        n: int = 1
    ) -> List[str]:
        """
        调用DALL-E 3生成图片
        
        Args:
            prompt: 图片描述
            size: 图片尺寸
            quality: 图片质量
            n: 生成图片数量
            
        Returns:
            List[str]: 图片URL列表
        """
        try:
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size=size,
                quality=quality,
                n=n
            )
            return [image.url for image in response.data]
        except Exception as e:
            print(f"图片生成出错: {e}")
            return [] 