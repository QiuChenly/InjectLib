class Color:
    """终端颜色工具类"""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    GREY = '\033[90m'
    BLACK = '\033[30m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
    # 黑色背景和白色文本
    BLACK_BG = '\033[40m'
    WHITE_FG = '\033[37m'
    
    # 用于恢复黑色背景和白色文本
    RESTORE_BG_FG = '\033[0m\033[40m\033[37m'
    
    @staticmethod
    def colorize(text, color):
        """将文本着色，并在重置后恢复黑色背景和白色文本"""
        return f"{color}{text}{Color.RESTORE_BG_FG}"
        
    @staticmethod
    def red(text):
        return Color.colorize(text, Color.RED)
        
    @staticmethod
    def green(text):
        return Color.colorize(text, Color.GREEN)
        
    @staticmethod
    def yellow(text):
        return Color.colorize(text, Color.YELLOW)
        
    @staticmethod
    def blue(text):
        return Color.colorize(text, Color.BLUE)
        
    @staticmethod
    def magenta(text):
        return Color.colorize(text, Color.MAGENTA)
        
    @staticmethod
    def cyan(text):
        return Color.colorize(text, Color.CYAN)
        
    @staticmethod
    def grey(text):
        return Color.colorize(text, Color.GREY)
        
    @staticmethod
    def bold(text):
        return Color.colorize(text, Color.BOLD)


def get_visible_length(text):
    """计算去除ANSI颜色代码后的文本可见长度，中文字符计为两个宽度，特殊字符特殊处理"""
    import re
    # 去除所有ANSI颜色代码
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    clean_text = ansi_escape.sub('', text)
    
    # 计算字符宽度
    length = 0
    for char in clean_text:
        # 特殊处理Logo字符
        if char == '█':
            length += 1
        # 判断是否是全角字符（中文、日文、韩文等）
        elif ord(char) > 127:  # ASCII范围外的字符
            length += 2
        else:
            length += 1
    return length


def truncate_text(text, max_length=20):
    """截断过长的文本，添加省略号，考虑ANSI颜色代码和中文字符宽度"""
    if text is None:
        return ""
    
    # 如果文本中没有颜色代码，使用简化的方法处理
    import re
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    clean_text = ansi_escape.sub('', text)
    
    if len(clean_text) == len(text):
        # 没有颜色代码的情况
        result = ""
        current_length = 0
        for char in text:
            char_width = 2 if ord(char) > 127 else 1
            if current_length + char_width <= max_length - 3:
                result += char
                current_length += char_width
            else:
                return result + "..."
        return text
    
    # 处理带颜色代码的文本
    result = ""
    current_length = 0
    ansi_codes = []
    
    # 正则表达式匹配ANSI颜色代码
    ansi_pattern = re.compile(r'(\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~]))')
    
    # 分割文本，保留ANSI代码
    parts = ansi_pattern.split(text)
    
    for part in parts:
        if ansi_pattern.match(part):
            # 如果是ANSI代码，加入结果和代码堆栈
            result += part
            ansi_codes.append(part)
        else:
            # 如果是普通文本
            for char in part:
                char_width = 2 if ord(char) > 127 else 1
                if current_length + char_width <= max_length - 3:
                    result += char
                    current_length += char_width
                else:
                    # 达到最大长度，添加省略号并退出
                    result += "..."
                    # 确保关闭所有颜色代码,并恢复黑色背景和白色文本
                    if ansi_codes and '\033[0m' not in ansi_codes:
                        result += Color.RESTORE_BG_FG
                    return result
    
    return result 