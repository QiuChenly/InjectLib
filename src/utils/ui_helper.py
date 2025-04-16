import sys
import os
from src.utils.color import Color, truncate_text, get_visible_length
from src.utils.i18n import _, I18n

# 定义ANSI颜色代码（统一管理）
BLACK_BG = "\033[40m"  # 黑色背景
WHITE_FG = "\033[37m"  # 白色前景色
RESET_ALL = "\033[0m"  # 重置所有属性
CLEAR_SCREEN = "\033[2J"  # 清屏
HOME_POSITION = "\033[H"  # 光标回到左上角

# 保存原始打印函数
original_print = print

def ensure_black_background():
    """确保终端输出为黑色背景和白色文本"""
    sys.stdout.write(BLACK_BG + WHITE_FG)
    sys.stdout.flush()
    
def black_background_print(*args, **kwargs):
    """包装原始print函数以确保黑色背景和白色文本"""
    # 在每次打印前确保黑色背景和白色文本
    sys.stdout.write(BLACK_BG + WHITE_FG)
    return original_print(*args, **kwargs)

def clear_screen():
    """清理屏幕并保持黑色背景和白色文本"""
    # 先执行系统清屏命令
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # 然后手动设置黑色背景和白色文本
    sys.stdout.write(BLACK_BG + WHITE_FG)  # 黑色背景，白色文本
    sys.stdout.flush()

def read_input(prompt):
    """读取用户输入并转换为小写"""
    # 确保输入提示是白色的
    sys.stdout.write(BLACK_BG + WHITE_FG)
    sys.stdout.flush()
    return input(prompt).strip().lower()

def confirm_action(prompt):
    """获取用户确认（y/n）"""
    response = read_input(prompt)
    return response == 'y'

def wait_for_enter():
    """等待用户按Enter键继续"""
    input(_("press_enter_to_continue", "按Enter键继续..."))

def format_app_info(app_info, include_status=False):
    """格式化应用信息，返回格式化后的名称、包名、版本等信息
    
    Args:
        app_info: 应用信息字典
        include_status: 是否包含安装状态
        
    Returns:
        dict: 包含格式化后字段的字典
    """
    # 设置列宽
    name_width = 30
    package_width = 40
    version_width = 15
    build_width = 15
    
    # 获取应用信息
    name = app_info.get("displayName", _("unknown", "未知"))
    package_name = app_info.get("packageName", _("unknown", "未知"))
    version = app_info.get("version", _("unknown", "未知"))
    build_version = app_info.get("buildVersion", _("unknown", "未知"))
    is_installed = app_info.get("isInstalled", True)
    
    # 截断文本
    name_truncated = truncate_text(name, name_width-2)
    package_truncated = truncate_text(package_name, package_width-2)
    version_truncated = truncate_text(version, version_width-2)
    build_version_truncated = truncate_text(build_version, build_width-2)
    
    # 确保名称和包名长度固定（考虑中文字符宽度）
    visible_name_length = get_visible_length(name_truncated)
    visible_package_length = get_visible_length(package_truncated)
    visible_version_length = get_visible_length(version_truncated)
    visible_build_length = get_visible_length(build_version_truncated)
    
    spaces_name = " " * (name_width - visible_name_length)
    spaces_package = " " * (package_width - visible_package_length)
    spaces_version = " " * (version_width - visible_version_length)
    spaces_build = " " * (build_width - visible_build_length)
    
    name_formatted = name_truncated + spaces_name
    package_formatted = package_truncated + spaces_package
    version_formatted = version_truncated + spaces_version
    build_formatted = build_version_truncated + spaces_build
    
    # 统一颜色方案
    if is_installed:
        name_colored = Color.green(name_formatted)
        package_colored = Color.cyan(package_formatted)
        version_colored = Color.yellow(version_formatted)
        build_version_colored = Color.yellow(build_formatted)
        status = Color.green(_("installed", "已安装")) if include_status else ""
    else:
        name_colored = Color.grey(name_formatted)
        package_colored = Color.grey(package_formatted)
        version_colored = Color.grey(version_formatted)
        build_version_colored = Color.grey(_("unknown", "未知"))
        status = Color.grey(_("not_installed", "未安装")) if include_status else ""
    
    result = {
        "name": name_colored,
        "package": package_colored,
        "version": version_colored,
        "build": build_version_colored,
        "status": status,
        "name_width": name_width,
        "package_width": package_width,
        "version_width": version_width,
        "build_width": build_width
    }
    
    return result

def print_app_table_header(include_status=False):
    """打印应用表格头部"""
    # 设置列宽
    name_width = 30
    package_width = 40
    version_width = 15
    build_width = 15
    status_width = 10
    
    # 创建表头
    header_app = _("app_name", "应用名称")
    header_pkg = _("package_name", "包名")
    header_version = _("version", "版本")
    header_build = _("build_version", "构建版本")
    header_status = _("status", "状态")
    header_index = _("index", "序号")
    
    # 打印表头
    if include_status:
        print(f"{header_index:<6}\t{header_app:<{name_width}}\t{header_pkg:<{package_width}}\t{header_version:<{version_width}}\t{header_build:<{build_width}}\t{header_status:<{status_width}}")
        print("-" * (6 + name_width + package_width + version_width + build_width + status_width + 20))
    else:
        print(f"{header_index:<6}\t{header_app:<{name_width}}\t{header_pkg:<{package_width}}\t{header_version:<{version_width}}\t{header_build:<{build_width}}")
        print("-" * (6 + name_width + package_width + version_width + build_width + 16))

def print_app_info(index, app_info, include_status=False):
    """打印格式化的应用信息"""
    formatted = format_app_info(app_info, include_status)
    
    if include_status:
        print(f"{index:<6}\t{formatted['name']:<{formatted['name_width']}}\t{formatted['package']:<{formatted['package_width']}}\t{formatted['version']:<{formatted['version_width']}}\t{formatted['build']:<{formatted['build_width']}}\t{formatted['status']}")
    else:
        print(f"{index:<6}\t{formatted['name']:<{formatted['name_width']}}\t{formatted['package']:<{formatted['package_width']}}\t{formatted['version']:<{formatted['version_width']}}\t{formatted['build']:<{formatted['build_width']}}") 