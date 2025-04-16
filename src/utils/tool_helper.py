import os
import sys
import platform
import subprocess
from src.utils.ui_helper import clear_screen, wait_for_enter
from src.utils.i18n import _, I18n
from src.utils.color import Color

def get_script_path():
    """获取当前脚本的路径"""
    if getattr(sys, 'frozen', False):
        # 如果是打包后的可执行文件
        return os.path.abspath(sys.executable)
    else:
        # 如果是脚本运行
        return os.path.abspath(sys.argv[0])

def restart_program():
    """重启程序
    
    完全重启当前程序，并保持相同的命令行参数
    """
    script_path = get_script_path()
    clear_screen()
    print(Color.yellow(_("restarting_program", "正在重启程序...")))
    
    # 获取系统平台
    system = platform.system()
    
    # 获取原始命令行参数（去除脚本名称）
    args = sys.argv[1:]
    
    if system == "Windows":
        # Windows平台使用pythonw.exe避免出现cmd窗口
        python_exe = sys.executable
        subprocess.Popen([python_exe, script_path] + args)
    else:
        # macOS和Linux平台
        os.execl(sys.executable, sys.executable, script_path, *args)
    
    # 终止当前进程
    sys.exit(0)

def reshow_menu(menu_function, *args, **kwargs):
    """重新显示菜单
    
    Args:
        menu_function: 要重新显示的菜单函数
        *args, **kwargs: 传递给菜单函数的参数
    """
    clear_screen()
    return menu_function(*args, **kwargs)

def execute_and_return(function, return_menu_function, *args, **kwargs):
    """执行功能并返回到指定菜单
    
    Args:
        function: 要执行的功能函数
        return_menu_function: 执行完后返回的菜单函数
        *args, **kwargs: 传递给功能函数的参数
        
    Returns:
        返回菜单函数的执行结果
    """
    # 执行功能
    result = function(*args, **kwargs)
    
    # 等待用户按Enter继续
    wait_for_enter()
    
    # 返回到指定菜单
    return reshow_menu(return_menu_function) 