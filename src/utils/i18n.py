import os
import json
import glob
from pathlib import Path

class I18n:
    """国际化支持类
    
    用于管理多语言翻译，支持动态加载语言文件。
    """
    
    # 预定义的语言代码（用于便捷访问）
    CHINESE = 'zh_CN'
    ENGLISH = 'en_US'
    JAPANESE = 'ja_JP'
    RUSSIAN = 'ru_RU'
    FRENCH = 'fr_FR'
    
    # 默认语言
    _current_language = ENGLISH
    
    # 翻译字典
    _translations = {}
    
    # 可用语言列表
    _available_languages = []
    
    # 语言名称映射
    _language_names = {
        CHINESE: "中文",
        ENGLISH: "English",
        JAPANESE: "日本語",
        RUSSIAN: "Русский",
        FRENCH: "Français"
    }
    
    @classmethod
    def init(cls, language=None):
        """初始化国际化支持
        
        Args:
            language: 指定语言代码，默认使用中文
        """
        # 加载所有可用的语言文件
        cls._scan_available_languages()
        
        # 设置当前语言
        if language and language in cls._available_languages:
            cls._current_language = language
        elif cls.CHINESE in cls._available_languages:
            cls._current_language = cls.CHINESE
        elif len(cls._available_languages) > 0:
            cls._current_language = cls._available_languages[0]
        
        # 加载翻译文件
        cls._load_translations()
    
    @classmethod
    def _scan_available_languages(cls):
        """扫描所有可用的语言文件"""
        cls._available_languages = []
        cls._translations = {}
        
        root_dir = Path(__file__).resolve().parent.parent.parent
        locale_dir = os.path.join(root_dir, "locales")
        
        # 确保语言文件目录存在
        os.makedirs(locale_dir, exist_ok=True)
        
        # 扫描所有json文件
        for language_file in glob.glob(os.path.join(locale_dir, "*.json")):
            language_code = os.path.basename(language_file).replace(".json", "")
            cls._available_languages.append(language_code)
            cls._translations[language_code] = {}
        
        # 如果没有发现任何语言文件，添加默认语言
        if not cls._available_languages:
            cls._available_languages = [cls.CHINESE, cls.ENGLISH]
    
    @classmethod
    def _load_translations(cls):
        """加载翻译文件"""
        root_dir = Path(__file__).resolve().parent.parent.parent
        locale_dir = os.path.join(root_dir, "locales")
        
        # 加载每种语言的翻译
        for language_code in cls._available_languages:
            lang_file = os.path.join(locale_dir, f"{language_code}.json")
            if os.path.exists(lang_file):
                try:
                    with open(lang_file, 'r', encoding='utf-8') as f:
                        cls._translations[language_code] = json.load(f)
                except Exception as e:
                    print(f"加载语言文件 {lang_file} 时出错: {e}")
    
    @classmethod
    def get_available_languages(cls):
        """获取所有可用的语言代码
        
        Returns:
            list: 可用语言代码列表
        """
        return cls._available_languages
    
    @classmethod
    def set_language(cls, language):
        """设置当前语言
        
        Args:
            language: 语言代码
        """
        # 确保语言在可用列表中
        if language not in cls._available_languages:
            # 重新扫描可用语言，确保新添加的语言文件被检测到
            cls._scan_available_languages()
        
        if language in cls._available_languages:
            # 如果该语言的翻译尚未加载，则加载它
            if language not in cls._translations or not cls._translations[language]:
                try:
                    root_dir = Path(__file__).resolve().parent.parent.parent
                    locale_dir = os.path.join(root_dir, "locales")
                    lang_file = os.path.join(locale_dir, f"{language}.json")
                    if os.path.exists(lang_file):
                        with open(lang_file, 'r', encoding='utf-8') as f:
                            cls._translations[language] = json.load(f)
                except Exception as e:
                    print(f"加载语言文件时出错: {e}")
            
            cls._current_language = language
        else:
            print(f"不支持的语言: {language}，使用默认语言 {cls.ENGLISH}")
            cls._current_language = cls.ENGLISH
    
    @classmethod
    def get_language_name(cls, language_code):
        """获取语言名称
        
        Args:
            language_code: 语言代码
            
        Returns:
            str: 语言名称
        """
        return cls._language_names.get(language_code, language_code)
    
    @classmethod
    def register_language_name(cls, language_code, name):
        """注册语言名称
        
        Args:
            language_code: 语言代码
            name: 语言名称
        """
        cls._language_names[language_code] = name
    
    @classmethod
    def get_next_language(cls):
        """获取下一个语言
        
        Returns:
            str: 下一个语言的代码
        """
        if not cls._available_languages:
            return cls._current_language
            
        current_index = cls._available_languages.index(cls._current_language) if cls._current_language in cls._available_languages else -1
        next_index = (current_index + 1) % len(cls._available_languages)
        return cls._available_languages[next_index]
    
    @classmethod
    def get_text(cls, key, default=None):
        """获取指定键的翻译文本
        
        Args:
            key: 翻译键
            default: 未找到翻译时的默认值，默认返回键名
            
        Returns:
            str: 翻译后的文本
        """
        if default is None:
            default = key
            
        return cls._translations.get(cls._current_language, {}).get(key, default)

# 创建一个简化的调用函数
def _(key, default=None):
    """获取翻译的简化函数
    
    Args:
        key: 翻译键
        default: 默认值
        
    Returns:
        str: 翻译后的文本
    """
    return I18n.get_text(key, default) 