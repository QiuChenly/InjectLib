import os
import sys
import json
from src.utils.ui_helper import ensure_black_background, wait_for_enter
from src.ui.banner import print_banner
from src.app.scanner import scan_apps
from src.app.app_manager import AppManager
from src.ui.menu_manager import MenuManager
from src.utils.i18n import I18n, _
from src.ui.language_selector import change_language_with_menu, auto_set_language
from src.ui.sakura_animation import SakuraAnimation
from src.ui.panda_animation import PandaAnimation
from src.utils.color import Color
from src.inject.helper import handle_helper  # 引入helper处理逻辑


def main():
    try:
        # 确保整个程序运行期间保持黑色背景
        ensure_black_background()
        
        # 加载配置
        config_path = "config.json"
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                config = json.load(f)
        else:
            config = {"Version": "1.0.0"}

        proc_version = config.get("Version", "1.0.0")
        
        # 使用自动语言检测设置语言
        auto_set_language(config)
        
        # 根据语言显示不同的欢迎动画
        if I18n._current_language == I18n.JAPANESE:
            # 日语：显示樱花花瓣雨动画
            sakura_animation = SakuraAnimation(duration=5, num_petals=150, static_petals=500)
            sakura_animation.play()
        elif I18n._current_language == I18n.CHINESE:
            # 中文：显示熊猫动画
            panda_animation = PandaAnimation(duration=5)
            panda_animation.play()
        
        # 扫描安装的应用（不再显示重复的扫描提示）
        installed_apps = scan_apps()
        
        # 初始化应用管理器
        app_manager = AppManager(config, installed_apps)
        
        # 初始化菜单管理器
        menu_manager = MenuManager(app_manager, proc_version, config)
        
        # 主程序循环
        while True:
            # 确保每次循环都保持黑色背景
            ensure_black_background()
            
            # 显示主菜单
            choice = menu_manager.show_main_menu()
            
            # 处理特殊命令：直接选择应用∂
            if isinstance(choice, int):
                try:
                    app_manager.handle_app_selection(int(choice))
                except (ValueError, IndexError) as e:
                    print(Color.red(_("invalid_app_selection", "无效的应用选择")))
                    print(f"错误详情: {str(e)}")
                    wait_for_enter()
                    continue
            # 处理标准菜单选项
            else:
                if choice == 's':
                    # 按关键字搜索应用
                    apps = menu_manager.handle_app_search()
                    if apps:
                        app_manager.add_selected_apps(apps)
                        print(_("apps_added_message").format(len(apps), app_manager.get_selected_count()))
                    wait_for_enter()
                    
                elif choice == 'i':
                    # 处理已选择的应用
                    menu_manager.handle_process_apps()
                    
                elif choice == 'l':
                    # 使用新的语言选择菜单
                    previous_language = config.get("Language", "en_US")
                    change_language_with_menu(config)
                    
                    # 根据新选择的语言显示不同的欢迎动画
                    current_language = config.get("Language", "en_US")
                    if current_language != previous_language:
                        if current_language == I18n.JAPANESE:
                            # 日语：显示樱花花瓣雨动画
                            sakura_animation = SakuraAnimation(duration=5, num_petals=150, static_petals=500)
                            sakura_animation.play()
                        elif current_language == I18n.CHINESE:
                            # 中文：显示熊猫动画
                            panda_animation = PandaAnimation(duration=5)
                            panda_animation.play()
                    
                elif choice == 'q':
                    # 退出程序
                    print("\n" + _("thank_you_message", "感谢使用，再见!"))
                    break

    except KeyboardInterrupt:
        print("\n" + _("user_interrupted", "用户手动退出程序,祝你使用愉快,再见."))
    except Exception as e:
        print(_("error_occurred", "发生错误: {0}").format(e))
        wait_for_enter()


if __name__ == "__main__":
    main()