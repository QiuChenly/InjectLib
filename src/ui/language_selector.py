import sys
import os
import json
import locale
from src.utils.color import Color
from src.utils.ui_helper import clear_screen, read_input, ensure_black_background, BLACK_BG, WHITE_FG, wait_for_enter
from src.utils.i18n import I18n
from src.ui.banner import print_banner

# 语言代码到国旗表情的映射
LANGUAGE_FLAGS = {
    "zh_CN": "🇨🇳",  # 中国
    "en_US": "🇺🇸",  # 美国
    "ja_JP": "🇯🇵",  # 日本
    "ru_RU": "🇷🇺",  # 俄罗斯
    "fr_FR": "🇫🇷",  # 法国
}

# 语言代码到显示名称的映射
LANGUAGE_DISPLAY_NAMES = {
    "zh_CN": "简体中文",
    "en_US": "English",
    "ja_JP": "日本語",
    "ru_RU": "Русский",
    "fr_FR": "Français",
}

# 系统语言代码到我们的语言代码的映射
SYSTEM_TO_APP_LANGUAGE = {
    "zh_CN": "zh_CN",
    "zh_TW": "zh_CN",  # 暂时将繁体中文映射到简体中文
    "zh_HK": "zh_CN",  # 暂时将香港繁体中文映射到简体中文
    "en_US": "en_US",
    "en_GB": "en_US",  # 将英国英语映射到美国英语
    "en": "en_US",     # 将通用英语映射到美国英语
    "ja_JP": "ja_JP",
    "ja": "ja_JP",     # 将通用日语映射到日本日语
    "ru_RU": "ru_RU",
    "ru": "ru_RU",     # 将通用俄语映射到俄罗斯俄语
    "fr_FR": "fr_FR",
    "fr": "fr_FR",     # 将通用法语映射到法国法语
}

def get_language_display_info(language_code):
    """获取语言的显示名称和国旗"""
    flag = LANGUAGE_FLAGS.get(language_code, "")
    display_name = LANGUAGE_DISPLAY_NAMES.get(language_code, language_code)
    return display_name, flag

def get_system_language():
    """获取系统语言并映射到应用支持的语言代码
    
    Returns:
        str: 应用支持的语言代码，如果系统语言不支持则返回默认的英语代码
    """
    try:
        # 获取系统语言设置
        system_locale = locale.getdefaultlocale()[0]
        if not system_locale:
            return "en_US"  # 默认英文
        
        # 先尝试完整匹配
        if system_locale in SYSTEM_TO_APP_LANGUAGE:
            return SYSTEM_TO_APP_LANGUAGE[system_locale]
        
        # 尝试语言部分匹配（不包括国家/地区代码）
        lang_code = system_locale.split('_')[0]
        if lang_code in SYSTEM_TO_APP_LANGUAGE:
            return SYSTEM_TO_APP_LANGUAGE[lang_code]
        
        # 没有匹配项，返回默认语言
        return "en_US"
    except Exception:
        # 出现任何错误，返回默认语言
        return "en_US"

def show_language_selection_menu(current_language):
    """显示语言选择菜单"""
    ensure_black_background()
    clear_screen()
    
    # 设置控制台颜色
    sys.stdout.write(BLACK_BG + WHITE_FG)
    sys.stdout.flush()
    
    # 显示语言选择标题
    print(Color.cyan("\n===== " + I18n.get_text("language_selection", "语言选择 / Language Selection") + " =====\n"))
    
    # 获取可用的语言列表
    available_languages = []
    locales_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "locales")
    
    if os.path.exists(locales_dir):
        for filename in os.listdir(locales_dir):
            if filename.endswith(".json"):
                language_code = os.path.splitext(filename)[0]
                available_languages.append(language_code)
    
    # 如果没有找到语言文件，使用默认语言
    if not available_languages:
        available_languages = ["zh_CN", "en_US"]
    
    # 显示语言选项
    for i, lang_code in enumerate(available_languages, 1):
        display_name, flag = get_language_display_info(lang_code)
        current_marker = " ← " + I18n.get_text("current", "当前") if lang_code == current_language else ""
        print(f"{Color.cyan(str(i))}. {flag} {display_name}{current_marker}")
    
    # 显示返回选项
    print(f"\n{Color.cyan('0')}. {I18n.get_text('back', '返回')}")
    
    # 提示用户选择
    choice = read_input("\n" + I18n.get_text("select_language", "请选择语言 / Please select language") + ": ")
    
    # 处理用户选择
    if choice == "0":
        return None
    
    try:
        choice_idx = int(choice) - 1
        if 0 <= choice_idx < len(available_languages):
            return available_languages[choice_idx]
        else:
            print(I18n.get_text("invalid_choice", "无效的选择"))
            wait_for_enter()
            return show_language_selection_menu(current_language)
    except ValueError:
        print(I18n.get_text("invalid_choice", "无效的选择"))
        wait_for_enter()
        return show_language_selection_menu(current_language)

def change_language_with_menu(config=None):
    """显示语言选择菜单并更改语言设置
    
    Args:
        config (dict, optional): 配置信息，如果提供则会更新配置文件
    
    Returns:
        bool: 如果语言已更改则返回True，否则返回False
    """
    current_language = "en_US"  # 默认语言为英语
    
    if config:
        current_language = config.get("Language", "en_US")
    
    selected_language = show_language_selection_menu(current_language)
    
    # 如果用户选择了一个语言
    if selected_language:
        # 如果选择的语言与当前语言不同
        if selected_language != current_language:
            # 设置新语言
            I18n.set_language(selected_language)
            
            # 如果提供了配置信息，则更新配置文件
            if config:
                config["Language"] = selected_language
                # 将配置保存到文件
                config_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
                config_path = os.path.join(config_dir, "config.json")
                
                with open(config_path, "w", encoding="utf-8") as f:
                    json.dump(config, f, indent=4)
            
            # 显示语言已更新的消息
            display_name, _ = get_language_display_info(selected_language)
            print(I18n.get_text("language_updated", "语言已更新为") + f": {display_name}")
            wait_for_enter()
            
            return True  # 语言已更改
    
    return False  # 语言未更改或用户未选择语言

def auto_set_language(config=None):
    """根据系统语言自动设置应用语言
    
    Args:
        config (dict, optional): 配置信息，如果提供则会更新配置文件
    
    Returns:
        bool: 如果语言已更改则返回True，否则返回False
    """
    # 如果配置文件中已经有语言设置，则使用该设置
    if config and "Language" in config:
        # 已经有语言设置，使用该设置
        I18n.set_language(config["Language"])
        return False
    
    # 没有语言设置，根据系统语言自动设置
    system_lang = get_system_language()
    I18n.set_language(system_lang)
    
    # 如果提供了配置信息，更新配置文件
    if config:
        config["Language"] = system_lang
        # 将配置保存到文件
        config_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
        config_path = os.path.join(config_dir, "config.json")
        
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4)
    
    return True  # 语言已更改 