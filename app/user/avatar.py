"""
头像处理工具
"""
import os
import random
from PIL import Image, ImageDraw
from fastapi import UploadFile
import aiofiles
from datetime import datetime
import hashlib

AVATAR_DIR = "static/avatars"
AVATAR_SIZE = (200, 200)
COLORS = [
    "#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEEAD",
    "#D4A5A5", "#9B59B6", "#3498DB", "#1ABC9C", "#F1C40F"
]

def ensure_avatar_dir():
    """确保头像目录存在"""
    if not os.path.exists(AVATAR_DIR):
        os.makedirs(AVATAR_DIR)

async def save_uploaded_avatar(file: UploadFile, username: str) -> str:
    """保存上传的头像"""
    ensure_avatar_dir()
    
    # 生成文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_extension = os.path.splitext(file.filename)[1]
    filename = f"{username}_{timestamp}{file_extension}"
    filepath = os.path.join(AVATAR_DIR, filename)
    
    # 保存文件
    async with aiofiles.open(filepath, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)
    
    # 处理图片
    with Image.open(filepath) as img:
        img = img.convert('RGB')
        img.thumbnail(AVATAR_SIZE)
        img.save(filepath, 'JPEG')
    
    return f"/{filepath}"

def generate_avatar(username: str) -> str:
    """生成随机头像"""
    ensure_avatar_dir()
    
    # 生成文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{username}_{timestamp}.jpg"
    filepath = os.path.join(AVATAR_DIR, filename)
    
    # 创建随机颜色的背景
    bg_color = random.choice(COLORS)
    img = Image.new('RGB', AVATAR_SIZE, bg_color)
    draw = ImageDraw.Draw(img)
    
    # 生成用户名首字母
    initial = username[0].upper()
    # 计算文字大小和位置
    font_size = 100
    text_x = AVATAR_SIZE[0] // 2
    text_y = AVATAR_SIZE[1] // 2
    
    # 绘制文字
    draw.text((text_x, text_y), initial, fill='white', anchor="mm", font_size=font_size)
    
    # 保存图片
    img.save(filepath, 'JPEG')
    
    return f"/{filepath}" 