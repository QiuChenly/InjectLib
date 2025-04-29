import os
import sys
from src.ui.menu import Menu
from src.ui.language_selector import change_language_with_menu
from src.utils.color import Color
from src.utils.i18n import I18n, _
from src.utils.ui_helper import ensure_black_background, clear_screen, read_input, wait_for_enter, print_app_table_header, print_app_info
from src.utils.input_helper import getch
from src.ui.banner import print_banner
from src.app.search import display_supported_apps, select_apps_by_keyword, show_all_supported_apps
from src.app.framework import launch_framework_menu
from src.utils.tool_helper import restart_program

class MenuManager:
    """管理应用的菜单显示和交互"""
    
    def __init__(self, app_manager=None, proc_version=None, config=None):
        """初始化菜单管理器
        
        Args:
            app_manager: 应用管理器对象
            proc_version: 程序版本号
            config (dict, optional): 全局配置对象
        """
        self.config = config or {}
        self.app_manager = app_manager
        self.proc_version = proc_version
        
        # 创建主菜单
        self.main_menu = self._create_main_menu()
        self.current_page = 0
        self.page_size = 20
        self.last_displayed_apps = []  # 保存最近显示的应用列表
    
    def _create_main_menu(self):
        """创建主菜单
        
        Returns:
            Menu: 主菜单对象
        """
        main_menu = Menu(I18n.get_text("main_menu", "主菜单"), config=self.config)
        
        # 添加主菜单选项
        main_menu.add_option(
            I18n.get_text("framework_menu", "框架菜单"), 
            self._open_framework_menu
        )
        
        main_menu.add_option(
            I18n.get_text("change_language", "更改语言"), 
            self._change_language
        )
        
        main_menu.add_option(
            I18n.get_text("search_apps", "搜索支持的应用"), 
            self._search_apps
        )
        
        return main_menu
    
    def _open_framework_menu(self, config):
        """打开框架菜单
        
        Args:
            config (dict): 配置信息
        
        Returns:
            bool: 如果要返回上一级菜单，则返回False
        """
        # 这里调用框架菜单的逻辑
        launch_framework_menu(config)
        return True
    
    def _change_language(self, config):
        """更改语言设置
        
        Args:
            config (dict): 配置信息
        
        Returns:
            bool: 始终返回True以继续主菜单
        """
        # 调用语言选择菜单
        language_changed = change_language_with_menu(config)
        
        # 如果语言已更改，重启程序以应用新语言
        if language_changed:
            print(Color.yellow(_("language_changed", "语言已更改，程序需要重启以应用新设置...")))
            wait_for_enter(_("press_enter_to_restart", "按Enter键重启程序..."))
            restart_program()
            return False  # 不会执行到这里，因为程序已重启
        
        # 如果语言未更改，只需重新创建主菜单以更新菜单项文本
        self.main_menu = self._create_main_menu()
        
        return True
    
    def _search_apps(self, config):
        """搜索支持的应用程序
        
        Args:
            config (dict): 配置信息
        
        Returns:
            bool: 始终返回True以继续主菜单
        """
        # 这里不直接调用display_supported_apps，
        # 而是进入搜索应用流程或返回到主菜单
        print(_("search_function_not_available", "搜索功能暂不可直接访问，请通过主菜单进行搜索"))
        wait_for_enter()
        return True
    
    def display_menu(self):
        """显示主菜单"""
        self.main_menu.display()
    
    def show_main_menu(self):
        """显示主菜单并处理用户交互
        
        Returns:
            str: 用户的选择
        """
        ensure_black_background()
        clear_screen()
        print_banner(self.proc_version)
        
        while True:
            # 确保每次循环都重新导入_函数
            from src.utils.i18n import _
            
            ensure_black_background()
            clear_screen()
            print_banner(self.proc_version)
            
            # 显示应用列表
            if self.app_manager is None:
                print(Color.red(_("error_app_manager_missing", "错误：应用管理器未初始化")))
                wait_for_enter()
                return "5"  # 返回退出程序选项
                
            app_list = self.app_manager.app_list
            install_apps = self.app_manager.installed_apps
            
            displayed_apps, self.current_page, total_pages = display_supported_apps(
                app_list, install_apps, self.current_page, self.page_size
            )
            
            # 保存当前显示的应用列表
            self.last_displayed_apps = displayed_apps
            
            # 显示导航选项
            self._display_navigation_options()
            
            # 显示输入提示但不换行，使用flush确保立即显示
            print("\n" + _("select_operation", "请选择操作,按回车键确认"), end='', flush=True)
            
            # 获取用户输入并按回车键确认
            choice = read_input("").strip()
            if choice.isdigit():
                try:
                    app_idx = int(choice)
                    
                    # 检查是否是有效的应用索引（可能跨页）
                    total_apps = len(self.app_manager.get_installed_supported_apps())
                    
                    # 首先检查是否是有效的应用编号
                    if 1 <= app_idx <= total_apps:
                        # 计算全局索引和页码
                        page_num = (app_idx - 1) // self.page_size
                        page_idx = (app_idx - 1) % self.page_size
                        
                        # 如果不在当前页，先切换到对应页面
                        if self.current_page != page_num:
                            self.current_page = page_num
                            # 重新获取该页的应用列表
                            displayed_apps, _, _ = display_supported_apps(
                                self.app_manager.app_list, 
                                self.app_manager.installed_apps,
                                self.current_page,
                                self.page_size
                            )
                            # 保存当前显示的应用列表
                            self.last_displayed_apps = displayed_apps
                        
                        # 确保索引有效
                        if page_idx < len(self.last_displayed_apps):
                            selected_app = self.last_displayed_apps[page_idx]
                            
                            # 在完整的已安装应用列表中找到这个应用
                            all_installed_apps = self.app_manager.get_installed_supported_apps()
                            
                            # 根据应用的关键属性（如packageName）查找真实索引
                            global_idx = -1
                            package_name = selected_app.get("packageName")
                            for i, app in enumerate(all_installed_apps):
                                if app.get("packageName") == package_name:
                                    global_idx = i
                                    break
                                    
                            # 如果找到了匹配的应用
                            if global_idx >= 0:
                                return global_idx
                            else:
                                print(_("invalid_app_selection", "无效的应用选择"))
                                wait_for_enter()
                        else:
                            print(_("invalid_app_number", "无效的应用编号"))
                            wait_for_enter()
                    else:
                        print(_("invalid_app_number", "无效的应用编号"))
                        wait_for_enter()
                except ValueError:
                    print(_("invalid_input", "无效的输入，请重新选择。"))
                    wait_for_enter()
            else:
                if choice == 'n':
                    if self.current_page < total_pages - 1:
                        self.current_page += 1
                    else:
                        print(_("last_page", "已经是最后一页"))
                        wait_for_enter()
                elif choice == 'p':
                    if self.current_page > 0:
                        self.current_page -= 1
                    else:
                        print(_("first_page", "已经是第一页"))
                        wait_for_enter()
                elif choice == 's' or choice == 'l' or choice == 'q':
                    return choice
                elif choice == 'i':
                    # 检查是否有已选择的应用
                    if self.app_manager.get_selected_count() > 0:
                        return choice
                    else:
                        print(_("no_apps_selected", "未选择任何应用，请先选择应用"))
                        wait_for_enter()
                else:
                    print(choice)  # 打印无效字符
                    print(_("invalid_choice", "无效的选择，请重新选择"))
                    wait_for_enter()
    
    def _display_navigation_options(self):
        """显示导航选项"""
        print("\n" + _("operation_options", "操作选项:"))
        
        # 获取已选择的应用数量
        selected_count = self.app_manager.get_selected_count()
        
        # 基本操作选项
        nav_options = f"{Color.cyan('n')}. {_('next_page', '下一页')} | {Color.cyan('p')}. {_('prev_page', '上一页')} | {Color.cyan('s')}. {_('search_app', '搜索应用')} | {Color.cyan('l')}. {_('switch_language', '切换语言')} | {Color.cyan('q')}. {_('exit', '退出程序')}"
        
        # 如果已选择了应用，显示"开始注入"选项
        if selected_count > 0:
            nav_options += f" | {Color.cyan('i')}. {_('start_injection', '开始注入 ({0}个应用)').format(selected_count)}"
            
        print(nav_options)
        print(f"{Color.cyan(_('number', '数字'))}. {_('select_app_for_injection', '选择应用进行注入 (输入1-9或01-09选择对应应用)')}")
    
    def handle_app_search(self):
        """处理应用搜索功能
        
        Returns:
            list: 匹配的应用列表
        """
        keyword = read_input(_("enter_keyword", "请输入关键字（按Enter返回上一级）: "))
        
        if not keyword:
            return []
        
        # 搜索匹配的应用
        matched_apps = self.app_manager.search_by_keyword(keyword)
        
        if not matched_apps:
            print(_("no_matching_apps", "未找到匹配的应用"))
            wait_for_enter()
            return []
        
        # 记录选择的应用
        app_Lst = []
        selected = set()
        
        while len(selected) < len(matched_apps):
            print("\n" + _("found_matching_apps", "找到以下匹配的应用程序:"))
            
            # 打印表头
            print_app_table_header(include_status=True)
            
            for i, app in enumerate(matched_apps, 1):
                status = _("selected", "✅ 已选中") if i-1 in selected else ""
                app_with_status = {**app, "status": status}
                print_app_info(i, app_with_status, include_status=True)
            
            print(f"\n{_('selected_apps_count', '已选择 {0}/{1} 个应用').format(len(selected), len(matched_apps))}")
            print(_("return_previous", "0. 返回上一级"))
            print(_("confirm_selection", "Enter. 确认当前选择并继续"))
            
            if len(selected) == len(matched_apps):
                print(_("all_apps_selected", "所有应用已选中..."))
                break
            
            # 显示输入提示但不换行
            print(_("enter_app_number", "请输入要选择的应用编号: "), end='', flush=True)
            
            # 获取单个字符输入
            choice = getch()
            
            if choice == '0':
                print(choice)
                if not app_Lst:
                    return []
                break
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
                    if 0 < app_idx <= len(matched_apps):
                        index = app_idx - 1
                        if index not in selected:
                            app_Lst.append(matched_apps[index])
                            selected.add(index)
                            print()  # 换行
                            print(_("app_selected", "已选择应用: {0}").format(matched_apps[index].get('displayName')))
                            if len(selected) == len(matched_apps): 
                                print(_("all_apps_selected", "所有应用已选中..."))
                        else:
                            print()  # 换行
                            print(_("app_already_selected", "应用 {0} 已经被选择，请选择其他应用。").format(matched_apps[index].get('displayName')))
                        wait_for_enter()
                    else:
                        print()  # 换行
                        print(_("invalid_app_number", "无效的应用编号"))
                        wait_for_enter()
                except ValueError:
                    print()  # 换行
                    print(_("invalid_input", "无效的输入"))
                    wait_for_enter()
            elif choice == '\r' or choice == '\n':  # Enter键
                print()  # 换行
                if not app_Lst:
                    print(_("no_app_selected", "未选择任何应用，请至少选择一个应用。"))
                    wait_for_enter()
                else:
                    break
            else:
                print(choice)  # 打印无效字符
                print(_("invalid_input", "无效的输入，请重新选择。"))
                wait_for_enter()
        
        return app_Lst
    
    def handle_browse_all_apps(self):
        """处理浏览所有支持的应用
        
        Returns:
            list: 选择的应用列表
        """
        # 使用search.py中的原始函数来浏览所有应用
        # 这个功能比较复杂，暂时保留原来的逻辑
        return show_all_supported_apps(self.app_manager.app_list, self.app_manager.installed_apps)
    
    def handle_process_apps(self):
        """处理所有选择的应用
        
        Returns:
            bool: 操作成功返回True，否则返回False
        """
        if not self.app_manager.display_selected_apps():
            print(_("no_apps_selected", "未选择任何应用，请先选择应用"))
            wait_for_enter()
            return False
        
        success_count, total = self.app_manager.process_selected_apps()
        if total > 0:
            print(_("processing_complete", "\n处理完成! 成功: {0}/{1}").format(success_count, total))
            # 清空已处理的应用列表
            self.app_manager.clear_selected_apps()
        
        wait_for_enter()
        return True 

def show_main_menu(config=None):
    """显示主菜单的便捷函数

    Args:
        config (dict, optional): 配置信息
    """
    print("警告：独立的show_main_menu函数不再支持直接调用")
    print("请使用MenuManager类来管理菜单")
    print("例如：menu_manager = MenuManager(app_manager, proc_version, config)")
    print("     menu_manager.display_menu()")
    
    # 这是一个后备方案，但不建议使用
    from src.app.scanner import scan_apps
    from src.app.app_manager import AppManager
    
    # 尝试初始化一个简单的菜单管理器
    installed_apps = scan_apps()
    app_manager = AppManager(config, installed_apps)
    menu_manager = MenuManager(app_manager, "1.0.0", config)
    return menu_manager.display_menu() 