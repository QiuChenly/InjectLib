from src.utils.color import Color, get_visible_length
from src.utils.ui_helper import BLACK_BG, WHITE_FG, RESET_ALL, CLEAR_SCREEN, HOME_POSITION, ensure_black_background
from src.utils.i18n import I18n
import datetime
import time
import sys
import random
import subprocess
import shutil
import atexit
import os

# 标记是否已初始化黑色背景
_background_initialized = False

# 保存原始打印函数
original_print = print

# 重新定义全局print函数，确保所有输出都有黑色背景和白色文本
def black_background_print(*args, **kwargs):
    """包装原始print函数以确保黑色背景和白色文本"""
    # 在每次打印前确保黑色背景和白色文本
    sys.stdout.write(BLACK_BG + WHITE_FG)
    return original_print(*args, **kwargs)

# 替换全局print函数
print = black_background_print

def get_last_commit_date():
    """从git历史记录中获取最近的提交日期"""
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cd", "--date=format:%Y-%m-%d"],
            capture_output=True,
            text=True,
            check=False
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except Exception:
        pass
    # 如果获取失败，返回当前日期
    return datetime.datetime.now().strftime("%Y-%m-%d")

def get_terminal_size():
    """获取终端宽度和高度"""
    try:
        # 尝试获取终端宽度和高度
        term_width, term_height = shutil.get_terminal_size()
        # 确保宽度合理
        # term_width = max(80, min(term_width, 150))  # 移除此行限制
        term_height = max(24, min(term_height, 50))
        return term_width, term_height
    except Exception:
        # 如果获取失败（例如在非TTY环境中），返回默认值
        return 100, 30

def center_colored_text(text, width):
    """居中显示彩色文本，考虑ANSI颜色代码"""
    visible_length = get_visible_length(text)
    padding = (width - visible_length) // 2
    return " " * padding + text

def fill_background(width, height):
    """填充整个终端为黑色背景和白色文本"""
    # 清屏
    sys.stdout.write(CLEAR_SCREEN)
    sys.stdout.write(HOME_POSITION)
    
    # 设置黑色背景和白色文本
    sys.stdout.write(BLACK_BG + WHITE_FG)
    
    # 使用空格填充每一行
    empty_line = " " * width
    for _ in range(height):
        sys.stdout.write(empty_line + "\n")
    
    # 回到顶部
    sys.stdout.write(HOME_POSITION)
    sys.stdout.flush()

# 初始化终端
def initialize_terminal():
    """初始化终端设置，设置黑色背景和白色文本并清屏"""
    global _background_initialized
    
    if not _background_initialized:
        # 清屏并设置黑色背景和白色文本
        sys.stdout.write(CLEAR_SCREEN)
        sys.stdout.write(HOME_POSITION)
        sys.stdout.write(BLACK_BG + WHITE_FG)
        sys.stdout.flush()
        
        # 填充整个屏幕
        term_width, term_height = get_terminal_size()
        empty_line = " " * term_width
        for _ in range(term_height):
            sys.stdout.write(empty_line + "\n")
        
        # 返回到顶部
        sys.stdout.write(HOME_POSITION)
        sys.stdout.flush()
        
        _background_initialized = True

# 注册退出时恢复终端默认设置的函数
def reset_terminal():
    """恢复终端默认设置"""
    sys.stdout.write(RESET_ALL)
    sys.stdout.flush()

atexit.register(reset_terminal)

# 重定向标准输出的写入方法
original_stdout_write = sys.stdout.write

def black_bg_stdout_write(text):
    """包装stdout.write确保所有直接写入都有黑色背景和白色文本"""
    if not text.startswith('\033'):  # 如果不是ANSI转义序列开头
        return original_stdout_write(BLACK_BG + WHITE_FG + text)
    return original_stdout_write(text)

sys.stdout.write = black_bg_stdout_write

# 程序启动时自动初始化终端
initialize_terminal()

def print_banner(proc_version):
    """打印程序横幅"""
    # 确保黑色背景和白色文本
    ensure_black_background()
    
    # 获取终端尺寸
    term_width, term_height = get_terminal_size()
    
    # 填充整个终端背景为黑色
    fill_background(term_width, term_height)
    
    # 确保proc_version是字符串类型
    proc_version_str = str(proc_version)
    
    # 获取版本发布日期
    release_date = get_last_commit_date()
    
    # 留出两侧的空白以增强视觉效果
    display_width = term_width - 4
    
    # 简化版banner，自适应终端宽度
    print()
    top_border = Color.CYAN + "━" * display_width + Color.RESET + BLACK_BG + WHITE_FG
    print(center_colored_text(top_border, term_width))
    
    # 标题行 - 使用简单的居中方式
    title = Color.BOLD + Color.WHITE + I18n.get_text("app_title", "MacOS 应用注入工具") + Color.RESET + BLACK_BG + WHITE_FG + " " + Color.RED + "[" + Color.GREEN + "v" + proc_version_str + Color.RED + "]" + Color.RESET + BLACK_BG + WHITE_FG
    print(center_colored_text(title, term_width))
    
    # 日期行和版本类型
    edition = Color.RED + "[" + Color.WHITE + I18n.get_text("edition_name", "PROFESSIONAL EDITION") + Color.RED + "]" + Color.RESET + BLACK_BG + WHITE_FG + " - " + Color.YELLOW + release_date + Color.RESET + BLACK_BG + WHITE_FG
    print(center_colored_text(edition, term_width))
    
    divider = Color.CYAN + "━" * display_width + Color.RESET + BLACK_BG + WHITE_FG
    print(center_colored_text(divider, term_width))
    
    # LOGO - 每行单独居中显示
    logo_lines = [
        "  ██████╗ ██╗██╗   ██╗ ██████╗██╗  ██╗███████╗███╗   ██╗██╗  ██╗   ██╗ ",
        " ██╔═══██╗██║██║   ██║██╔════╝██║  ██║██╔════╝████╗  ██║██║  ╚██╗ ██╔╝ ",
        " ██║   ██║██║██║   ██║██║     ███████║█████╗  ██╔██╗ ██║██║   ╚████╔╝  ",
        " ██║▄▄ ██║██║██║   ██║██║     ██╔══██║██╔══╝  ██║╚██╗██║██║    ╚██╔╝   ",
        " ╚██████╔╝██║╚██████╔╝╚██████╗██║  ██║███████╗██║ ╚████║███████╗██║    ",
        "  ╚══▀▀═╝ ╚═╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝╚══════╝╚═╝    "
    ]
    
    gradient_colors = [Color.CYAN, Color.BLUE, Color.MAGENTA, Color.RED, Color.YELLOW, Color.GREEN]
    
    for i, line in enumerate(logo_lines):
        color = gradient_colors[i % len(gradient_colors)]
        colored_line = color + line + Color.RESET + BLACK_BG + WHITE_FG
        # 计算正确的居中位置
        # centered_line = center_colored_text(colored_line, term_width)
        # print(centered_line)
        print(colored_line) # 直接打印，不居中
    
    print(center_colored_text(divider, term_width))
    
    # 信息部分 - 使用自定义函数居中
    info_line1 = Color.BOLD + Color.WHITE + I18n.get_text("original_design", "Original Design By ") + Color.YELLOW + "QiuChenly(github.com/qiuchenly)" + Color.WHITE + ", " + I18n.get_text("py_version_by", "Py ver. by ") + Color.MAGENTA + "X1a0He" + Color.RESET + BLACK_BG + WHITE_FG
    info_line2 = Color.BOLD + Color.WHITE + I18n.get_text("auto_inject_version", "自动注入版本号: ") + Color.GREEN + proc_version_str + Color.RESET + BLACK_BG + WHITE_FG + " (" + Color.RED + I18n.get_text("premium_features", "Premium Features Enabled") + Color.RESET + BLACK_BG + WHITE_FG + ")"
    info_line3 = Color.BOLD + Color.WHITE + I18n.get_text("injection_prompt", "注入时请根据提示输入'") + Color.YELLOW + "y" + Color.WHITE + I18n.get_text("injection_prompt_or", "' 或者按下") + Color.CYAN + I18n.get_text("enter_key", "回车键") + Color.WHITE + I18n.get_text("injection_prompt_skip", "跳过这一项。") + Color.RESET + BLACK_BG + WHITE_FG
    
    print(center_colored_text(info_line1, term_width))
    print(center_colored_text(info_line2, term_width))
    print(center_colored_text(info_line3, term_width))
    
    # 加载动画 - 居中显示
    loading_text = I18n.get_text("system_initializing", "系统初始化中")
    loading_visible_length = len(loading_text)
    loading_complete_text = I18n.get_text("system_initializing_complete", "系统初始化中... 完成！")
    loading_complete_visible_length = len(loading_complete_text)
    padding = (term_width - loading_complete_visible_length) // 2
    
    # 打印空格到起始位置
    sys.stdout.write(" " * padding + Color.GREEN + loading_text + Color.RESET + BLACK_BG + WHITE_FG)
    sys.stdout.flush()
    
    for _ in range(3):
        time.sleep(0.1)
        sys.stdout.write(Color.GREEN + "." + Color.RESET + BLACK_BG + WHITE_FG)
        sys.stdout.flush()
    
    print() # 保留一个换行
    
    print(center_colored_text(divider, term_width))
    
    # 随机提示
    tip_messages = [
        I18n.get_text("tip_number_keys", "提示: 在主菜单使用数字键快速选择应用"),
        I18n.get_text("tip_quit", "提示: 按'q'键可以随时退出程序"),
        I18n.get_text("tip_permissions", "提示: 确保您有足够的权限来运行此工具"),
        I18n.get_text("tip_documentation", "提示: 查看文档获取更多使用技巧和帮助")
    ]
    
    tip = Color.GREY + random.choice(tip_messages) + Color.RESET + BLACK_BG + WHITE_FG
    print(center_colored_text(tip, term_width))
    print() 