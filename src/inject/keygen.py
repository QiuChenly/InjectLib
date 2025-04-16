import os
import subprocess
from pathlib import Path
from src.utils.color import Color


# 执行命令并检查结果的辅助函数
def run_command(command, shell=True, check_error=True):
    """运行命令并检查结果，如果出错则显示红色警告
    
    Args:
        command: 要执行的命令
        shell: 是否使用shell执行
        check_error: 是否检查错误
        
    Returns:
        bool: 命令执行成功返回True，否则返回False
    """
    try:
        result = subprocess.run(command, shell=shell, capture_output=True, text=True)
        
        # 检查命令是否执行成功
        if check_error and result.returncode != 0:
            error_msg = result.stderr.strip() or f"命令执行失败: {command}"
            if "No such file or directory" in error_msg or "command not found" in error_msg:
                print(Color.red(f"[错误] {error_msg}"))
            return False
        return True
    except Exception as e:
        if check_error:
            print(Color.red(f"[错误] 执行命令时发生异常: {e}"))
        return False


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