from src.utils.ui_helper import clear_screen, read_input, ensure_black_background, BLACK_BG, WHITE_FG, wait_for_enter
from src.ui.banner import print_banner
from src.app.search import display_supported_apps
from src.utils.color import Color, get_visible_length
from src.utils.i18n import I18n
import sys
import termios
import tty
import os
import signal
import time


def getch():
    """获取单个字符输入，无需按Enter键"""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def show_main_menu(proc_version, app_list, install_apps):
    """显示主菜单并返回用户选择"""
    ensure_black_background()
    clear_screen()
    print_banner(proc_version)
    
    # 显示已安装且支持的应用程序
    current_page = 0
    page_size = 20
    
    while True:
        ensure_black_background()
        clear_screen()
        print_banner(proc_version)
        
        # 显示应用列表
        displayed_apps, current_page, total_pages = display_supported_apps(
            app_list, install_apps, current_page, page_size
        )
        
        # 确保背景为黑色，文本为白色
        sys.stdout.write(BLACK_BG + WHITE_FG)
        sys.stdout.flush()
        
        # 显示导航选项
        print("\n" + I18n.get_text("operation_options", "操作选项:"))
        print(f"{Color.cyan('n')}. {I18n.get_text('next_page', '下一页')} | {Color.cyan('p')}. {I18n.get_text('prev_page', '上一页')} | {Color.cyan('s')}. {I18n.get_text('search_app', '搜索应用')} | {Color.cyan('q')}. {I18n.get_text('exit', '退出程序')}")
        print(f"{Color.cyan(I18n.get_text('number', '数字'))}. {I18n.get_text('select_app_for_injection', '选择应用进行注入')}")
        
        # 再次确保背景为黑色，文本为白色（以防上面的输出改变了颜色设置）
        sys.stdout.write(BLACK_BG + WHITE_FG)
        sys.stdout.flush()
        
        print("\n" + I18n.get_text("select_operation", "请选择操作: "), end='', flush=True)
        
        # 获取单个字符输入
        choice = getch()
        
        # 当输入n/p/s/q时，直接执行操作，不需要打印输入的字符
        if choice in ['n', 'p', 's', 'q']:
            print(choice)  # 仅打印当前字符提供反馈
            
            if choice == 'n':
                if current_page < total_pages - 1:
                    current_page += 1
                else:
                    print(I18n.get_text("last_page", "已经是最后一页"))
                    wait_for_enter()
            elif choice == 'p':
                if current_page > 0:
                    current_page -= 1
                else:
                    print(I18n.get_text("first_page", "已经是第一页"))
                    wait_for_enter()
            elif choice == 's':
                return '1'  # 进入搜索功能
            elif choice == 'q':
                return '4'  # 退出程序
        elif choice.isdigit():
            # 对于数字选择，需要读取完整的数字
            full_choice = choice
            print(choice, end='', flush=True)  # 打印第一个数字
            
            # 继续读取数字直到遇到非数字字符或Enter
            while True:
                ch = getch()
                if ch.isdigit():
                    full_choice += ch
                    print(ch, end='', flush=True)
                elif ch == '\r' or ch == '\n':  # Enter键
                    print()  # 换行
                    break
                else:
                    print()  # 换行
                    break
            
            try:
                app_idx = int(full_choice)
                if 1 <= app_idx <= len(displayed_apps):
                    # 返回一个特殊命令表示选择的应用
                    return f"SELECT:{app_idx-1+current_page*page_size}"
                else:
                    print(I18n.get_text("invalid_app_number", "无效的应用编号"))
                    wait_for_enter()
            except ValueError:
                print(I18n.get_text("invalid_input", "无效的输入"))
                wait_for_enter()
        else:
            print(choice)  # 打印无效字符
            print(I18n.get_text("invalid_choice", "无效的选择，请重新选择"))
            wait_for_enter() 


class Menu:
    def __init__(self, title, options=None, parent=None, config=None):
        """初始化菜单

        Args:
            title (str): 菜单标题
            options (list, optional): 菜单选项列表，每个选项是一个字典，包含 name 和 action
            parent (Menu, optional): 父菜单，用于返回上级菜单
            config (dict, optional): 配置信息，传递给菜单选项的回调函数
        """
        self.title = title
        self.options = options or []
        self.parent = parent
        self.config = config
        self.running = False
        
    def display(self):
        """显示菜单并处理用户输入"""
        self.running = True
        ensure_black_background()
        
        while self.running:
            clear_screen()
            
            # 设置控制台颜色
            sys.stdout.write(BLACK_BG + WHITE_FG)
            sys.stdout.flush()
            
            # 显示标题和横幅
            print_banner("1.0.0")  # 传入一个默认版本号
            print(Color.cyan("\n===== " + self.title + " =====\n"))
            
            # 显示操作选项
            print(Color.cyan(I18n.get_text("operation_options", "操作选项") + ":"))
            for i, option in enumerate(self.options, 1):
                print(f"{Color.cyan(str(i))}. {option['name']}")
            
            # 显示导航选项
            print(Color.cyan("\n" + I18n.get_text("navigation_options", "导航选项") + ":"))
            if self.parent:
                print(f"{Color.cyan('0')}. {I18n.get_text('back', '返回上级菜单')}")
            else:
                print(f"{Color.cyan('0')}. {I18n.get_text('exit', '退出程序')}")
            
            # 获取用户输入
            choice = read_input("\n" + I18n.get_text("enter_choice", "请输入选项") + ": ")
            
            # 处理用户选择
            if choice == "0":
                if self.parent:
                    # 返回上级菜单
                    return
                else:
                    # 退出程序
                    print("\n" + Color.yellow(I18n.get_text("exiting", "正在退出...")))
                    time.sleep(1)  # 添加一点延迟，更友好的用户体验
                    sys.exit(0)
            
            # 处理菜单选项
            try:
                choice_idx = int(choice) - 1
                if 0 <= choice_idx < len(self.options):
                    option = self.options[choice_idx]
                    action = option.get("action")
                    if action and callable(action):
                        # 执行菜单项对应的操作
                        result = action(self.config)
                        # 如果操作返回False，则直接返回
                        if result is False:
                            return
                    else:
                        print(I18n.get_text("invalid_action", "无效的操作"))
                        wait_for_enter()
                else:
                    print(I18n.get_text("invalid_choice", "无效的选择"))
                    wait_for_enter()
            except ValueError:
                print(I18n.get_text("invalid_choice", "无效的选择"))
                wait_for_enter()
    
    def add_option(self, name, action):
        """添加菜单选项

        Args:
            name (str): 选项名称
            action (callable): 选项对应的操作函数
        """
        self.options.append({"name": name, "action": action})
    
    def stop(self):
        """停止菜单循环"""
        self.running = False 