import os
import sys
import time
import random
from src.utils.ui_helper import clear_screen, ensure_black_background

# 背景和颜色重置代码
BLACK_BG = "\033[40m"  # 黑色背景
RED_BG = "\033[41m"    # 红色背景
BRIGHT_RED_FG = "\033[1;31m"  # 亮红色前景
RESET_COLOR = "\033[0m"

# 中国元素emoji列表
CHINA_EMOJIS = [
    "🇨🇳",  # 中国国旗
    "🐼",   # 熊猫
    "🏮",   # 灯笼
    "🧧",   # 红包/中国结
    "🐉",   # 龙
    "🏯",   # 中国建筑
    "🍜",   # 面条
    "🥢",   # 筷子
    "🍵",   # 茶
    "🥮",   # 月饼
    "🀄",   # 麻将
    "🎏"    # 鲤鱼旗
]

# 不同语言/文字的"中国"表示
CHINA_VARIANTS = [
    "【 简体模式 - 中国 】",
    "【 繁體模式 - 中國 】",
    "【 粤语模式 - 中國(zung1 gwok3) 】"
]

class PandaAnimation:
    """中国元素emoji动画效果类"""
    
    def __init__(self, duration=8):
        """
        初始化中国元素emoji动画
        
        Args:
            duration (int): 动画持续时间（秒）
        """
        self.duration = duration
        self.emojis = []  # 存储所有飘落的emoji位置和速度
        self.max_emojis = 60  # 屏幕上最多显示的emoji数量
        self.text_switch_interval = 1.5  # 文字切换间隔（秒）
        self.current_text_index = 0  # 当前显示的文字索引
        
    def _get_terminal_size(self):
        """获取终端大小"""
        try:
            columns, lines = os.get_terminal_size()
            return lines, columns
        except:
            return 24, 80
    
    def _fill_background(self, color=BLACK_BG):
        """填充整个屏幕为指定背景色"""
        height, width = self._get_terminal_size()
        
        # 确保ANSI背景色
        sys.stdout.write(color)
        sys.stdout.flush()
        
        # 清屏
        clear_screen()
        
        # 使用指定颜色空格填充整个屏幕
        for _ in range(height):
            sys.stdout.write(color + " " * width + "\n")
        
        # 将光标移回屏幕左上角
        sys.stdout.write("\033[H")
        sys.stdout.flush()
    
    def _create_new_emoji(self):
        """创建一个新的飘落emoji"""
        height, width = self._get_terminal_size()
        
        # 随机位置（全屏范围内）
        row = random.randint(0, height - 2)
        col = random.randint(0, width - 4)  # emoji宽度约为2个字符
        
        # 随机移动速度和方向
        speed_y = random.uniform(0.1, 0.6)  # 垂直速度
        speed_x = random.uniform(-0.3, 0.3)  # 水平速度，可以是负值（向左）
        
        # 随机大小（使用ANSI转义序列调整字体大小）
        size = random.choice([1, 2, 3])
        
        # 随机选择一个中国元素emoji
        emoji = random.choice(CHINA_EMOJIS)
        
        return {
            "row": row,
            "col": col,
            "speed_y": speed_y,
            "speed_x": speed_x,
            "size": size,
            "emoji": emoji
        }
    
    def _update_emojis(self):
        """更新所有飘落emoji的位置"""
        height, width = self._get_terminal_size()
        
        # 移除已经飘出屏幕的emoji
        self.emojis = [emoji for emoji in self.emojis 
                       if 0 <= emoji["row"] < height and 0 <= emoji["col"] < width - 4]
        
        # 如果emoji数量少于最大值，随机添加新的emoji
        if len(self.emojis) < self.max_emojis and random.random() < 0.2:
            self.emojis.append(self._create_new_emoji())
        
        # 更新每个emoji的位置
        for emoji in self.emojis:
            emoji["row"] += emoji["speed_y"]
            emoji["col"] += emoji["speed_x"]
            
            # 如果到了屏幕边缘，反弹或重新设置方向
            if emoji["col"] <= 0 or emoji["col"] >= width - 4:
                emoji["speed_x"] *= -0.8  # 反弹，减速
    
    def _draw_emojis(self, elapsed_time):
        """绘制所有飘落的emoji和底部文字"""
        height, width = self._get_terminal_size()
        
        # 先清屏
        self._fill_background(BLACK_BG)
        
        # 绘制每个emoji
        for emoji in self.emojis:
            row = int(emoji["row"])
            col = int(emoji["col"])
            size = emoji["size"]
            emoji_char = emoji["emoji"]
            
            if 0 <= row < height and 0 <= col < width - 4:
                size_code = f"\033[{size}m" if size > 1 else ""
                sys.stdout.write(f"\033[{row};{col}H{size_code}{emoji_char}{RESET_COLOR}")
        
        # 计算当前应该显示哪个文字变体（根据经过的时间）
        text_index = int((elapsed_time / self.text_switch_interval) % len(CHINA_VARIANTS))
        
        # 底部显示文字（交替显示不同变体）
        msg = f"{BRIGHT_RED_FG}{CHINA_VARIANTS[text_index]}{RESET_COLOR}"
        msg_pos = (width - len(msg) + 20) // 2  # +20是为了补偿ANSI颜色代码和宽字符带来的长度计算问题
        sys.stdout.write(f"\033[{height-1};{msg_pos}H{msg}")
        
        sys.stdout.flush()
    
    def play(self):
        """播放中国元素emoji动画"""
        try:
            # 确保黑色背景
            ensure_black_background()
            
            # 清屏并填充黑色背景
            self._fill_background(BLACK_BG)
            
            # 记录开始时间
            start_time = time.time()
            
            # 初始化更多emoji（全屏分布）
            for _ in range(25):
                self.emojis.append(self._create_new_emoji())
            
            # 播放动画直到达到指定时间
            while time.time() - start_time < self.duration:
                # 计算已经过的时间
                elapsed_time = time.time() - start_time
                
                # 更新emoji位置
                self._update_emojis()
                
                # 绘制emoji和文字
                self._draw_emojis(elapsed_time)
                
                # 控制帧率
                time.sleep(0.1)
            
            # 清屏并恢复黑色背景
            clear_screen()
            ensure_black_background()
            
        except KeyboardInterrupt:
            # 用户中断
            clear_screen()
            ensure_black_background()