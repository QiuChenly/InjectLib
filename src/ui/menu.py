from src.utils.ui_helper import clear_screen, read_input, ensure_black_background, BLACK_BG, WHITE_FG, wait_for_enter
from src.ui.banner import print_banner
from src.utils.color import Color, get_visible_length
from src.utils.i18n import I18n
from src.utils.input_helper import getch
import sys
import os
import signal
import time


def show_main_menu(proc_version, app_list, install_apps):
    """显示主菜单并返回用户选择"""
    # 提示：该函数已被MenuManager替代，此处仅保留以兼容旧代码
    print("警告：独立的show_main_menu函数不再支持直接调用")
    print("请使用MenuManager类来管理菜单")
    return '1'  # 默认返回搜索功能


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