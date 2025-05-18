import os
import subprocess
from pathlib import Path
from src.utils.color import Color
from src.inject.helper import run_command

def handle_keygen(bundleIdentifier):
    """处理应用注册"""
    # 获取项目根目录
    root_dir = Path(__file__).resolve().parent.parent.parent
    
    # 构建工具路径
    keygen_path = os.path.join(root_dir, "tool", "KeygenStarter")
    
    # 取出用户名
    username = os.path.expanduser("~").split("/")[-1]
    
    # 设置工具权限
    if not run_command(f"chmod +x '{keygen_path}'"):
        print(Color.red(f"[错误] 无法设置 KeygenStarter 为可执行文件: {keygen_path}"))
        return False
    
    # 运行工具
    if not run_command(f"'{keygen_path}' '{bundleIdentifier}' '{username}'"):
        print(Color.red(f"[错误] 运行 KeygenStarter 失败"))
        return False
    
    return True 