from openai_client import OpenAIClient

def main():
    # 创建OpenAI客户端实例
    client = OpenAIClient()
    
    # 示例1: 聊天补全
    messages = [
        {"role": "user", "content": "你好，请介绍一下你自己"}
    ]
    response = client.chat_completion(messages)
    print("AI回复:", response)
    
    # 示例2: 图片生成
    prompt = "一只可爱的熊猫正在吃竹子"
    image_urls = client.generate_image(prompt)
    print("生成的图片URL:", image_urls)

if __name__ == "__main__":
    main() 