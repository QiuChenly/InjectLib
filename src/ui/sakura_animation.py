import os
import sys
import time
import random
import threading
from src.utils.ui_helper import clear_screen, ensure_black_background
from src.utils.color import Color

# 樱花符号
SAKURA_SYMBOLS = ["🌸", "💮", "🌹", "❀", "✿", "❁", "❃", "❊", "✽"]
# 颜色变种（粉色系列）
SAKURA_COLORS = [
    "\033[38;5;218m",  # 浅粉色
    "\033[38;5;217m",  # 粉红色
    "\033[38;5;211m",  # 亮粉色
    "\033[38;5;219m",  # 淡紫粉色
    "\033[38;5;225m",  # 极浅粉色
]
# 黑色背景和颜色重置代码
BLACK_BG = "\033[40m"
RESET_COLOR = "\033[0m"

class Petal:
    """表示单个花瓣的类"""
    def __init__(self, x, y, terminal_height, terminal_width, is_static=False):
        self.x = x
        self.y = y
        self.symbol = random.choice(SAKURA_SYMBOLS)
        self.color = random.choice(SAKURA_COLORS)
        self.speed = random.uniform(0.2, 1.0) if not is_static else 0
        self.drift = random.uniform(-0.3, 0.3) if not is_static else 0  # 左右漂移的速度
        self.terminal_height = terminal_height
        self.terminal_width = terminal_width
        self.is_static = is_static  # 是否是静态花瓣（不移动）
        
    def update(self):
        """更新花瓣位置"""
        if self.is_static:
            return  # 静态花瓣不移动
            
        self.y += self.speed
        self.x += self.drift
        
        # 如果花瓣飘出屏幕底部，重新从顶部开始
        if self.y >= self.terminal_height:
            self.y = 0
            self.x = random.uniform(0, self.terminal_width)
            
        # 如果花瓣飘出屏幕左右，则拉回到屏幕内
        if self.x < 0:
            self.x = 0
            self.drift = abs(self.drift)  # 反向漂移
        elif self.x >= self.terminal_width:
            self.x = self.terminal_width - 1
            self.drift = -abs(self.drift)  # 反向漂移
            
    def __str__(self):
        """花瓣的字符表示"""
        return f"{self.color}{self.symbol}{RESET_COLOR}{BLACK_BG}"

class SakuraAnimation:
    """樱花花瓣雨动画效果类"""
    
    def __init__(self, duration=3, num_petals=50, static_petals=400):
        """
        初始化樱花动画
        
        Args:
            duration (int): 动画持续时间（秒）
            num_petals (int): 动态花瓣数量
            static_petals (int): 静态背景花瓣数量
        """
        self.duration = duration
        self.num_petals = num_petals
        self.static_petals = static_petals
        self.stop_event = threading.Event()
        
    def _get_terminal_size(self):
        """获取终端大小"""
        try:
            columns, lines = os.get_terminal_size()
            return lines, columns
        except:
            return 24, 80
    
    def _fill_background(self):
        """填充整个屏幕为黑色背景"""
        height, width = self._get_terminal_size()
        
        # 确保ANSI背景色为黑色
        sys.stdout.write(BLACK_BG)
        sys.stdout.flush()
        
        # 清屏
        clear_screen()
        
        # 使用黑色空格填充整个屏幕
        for _ in range(height):
            sys.stdout.write(BLACK_BG + " " * width + "\n")
        
        # 将光标移回屏幕左上角
        sys.stdout.write("\033[H")
        sys.stdout.flush()
            
    def _center_text(self, text, width):
        """居中显示文本"""
        padding = (width - len(text)) // 2
        return BLACK_BG + " " * padding + text
    
    def _draw_welcome_message(self, frame_count):
        """绘制欢迎消息，带有淡入效果"""
        height, width = self._get_terminal_size()
        progress = min(1.0, frame_count / 10.0)  # 10帧内逐渐淡入
        
        # 欢迎消息
        welcome_text = "ようこそ！"  # "欢迎！"的日语
        
        # 计算中心位置
        center_y = height // 2 - 3
        
        # 渐变色（从暗到亮）
        gradient = [
            "\033[38;5;52m", "\033[38;5;88m", "\033[38;5;124m", 
            "\033[38;5;160m", "\033[38;5;196m", "\033[38;5;202m", 
            "\033[38;5;208m", "\033[38;5;214m", "\033[38;5;220m"
        ]
        
        # 根据进度选择颜色
        color_idx = min(int(progress * len(gradient)), len(gradient) - 1)
        color = gradient[color_idx]
        
        # 生成带颜色的文本
        colored_text = f"{color}{welcome_text}{RESET_COLOR}{BLACK_BG}"
        
        # 居中显示
        centered_text = self._center_text(colored_text, width)
        sys.stdout.write(f"\033[{center_y};0H{centered_text}")
        
        # 日语说明
        jp_text = "日本語モードへようこそ"  # "欢迎使用日语模式"
        jp_colored = f"\033[38;5;219m{jp_text}{RESET_COLOR}{BLACK_BG}"
        centered_jp = self._center_text(jp_colored, width)
        sys.stdout.write(f"\033[{center_y+2};0H{centered_jp}")
    
    def _create_background_canvas(self, static_petals):
        """创建包含静态花瓣的背景画布"""
        height, width = self._get_terminal_size()
        
        # 创建空白画布 (使用黑色背景)
        canvas = [[BLACK_BG + ' ' for _ in range(width)] for _ in range(height)]
        
        # 将静态花瓣均匀分布在画布上
        for petal in static_petals:
            x, y = int(petal.x), int(petal.y)
            if 0 <= x < height and 0 <= y < width:
                canvas[x][y] = str(petal)
        
        return canvas
    
    def _draw_frame(self, dynamic_petals, static_canvas, frame_count):
        """绘制单帧动画"""
        # 复制静态背景画布
        height, width = self._get_terminal_size()
        canvas = [row[:] for row in static_canvas]  # 深复制静态画布
        
        # 更新并绘制动态花瓣
        for petal in dynamic_petals:
            # 更新花瓣位置（先更新再绘制，这样显示的是更新后的位置）
            petal.update()
            
            # 将动态花瓣放置在画布上
            x, y = int(petal.x), int(petal.y)
            if 0 <= x < height and 0 <= y < width:
                canvas[x][y] = str(petal)
        
        # 清屏后绘制整个画布
        clear_screen()
        sys.stdout.write("\033[H")  # 移动光标到左上角
        for row in canvas:
            print(''.join(row))
        
        # 绘制欢迎信息（带淡入效果）
        self._draw_welcome_message(frame_count)
        
        # 在底部中央显示"日本語"文字
        if height > 2:
            msg = f"\033[38;5;213m✿ 日本語モード ✿{RESET_COLOR}{BLACK_BG}"
            padding = " " * ((width - len(msg) + 24) // 2)  # 调整补偿ANSI颜色代码
            sys.stdout.write(f"\033[{height-1};0H{BLACK_BG}{padding}{msg}")  # 将光标移动到底部中央
        
        sys.stdout.flush()
    
    def _create_initial_petals(self, count, is_static=False):
        """创建初始的花瓣，均匀分布在整个屏幕上"""
        height, width = self._get_terminal_size()
        petals = []
        
        # 计算每个区域的花瓣数量
        sections_h = 10  # 水平分区数
        sections_v = 10  # 垂直分区数
        
        # 为了让花瓣看起来更自然，我们在每个区域内随机分布花瓣
        section_width = width / sections_h
        section_height = height / sections_v
        
        # 每个区域至少有一定数量的花瓣
        petals_per_section = max(1, count // (sections_h * sections_v))
        
        # 为每个区域分配花瓣
        for section_x in range(sections_h):
            for section_y in range(sections_v):
                # 在当前区域内随机生成花瓣
                for _ in range(petals_per_section):
                    # 随机位置在当前区域内
                    x = random.uniform(section_y * section_height, (section_y + 1) * section_height)
                    y = random.uniform(section_x * section_width, (section_x + 1) * section_width)
                    petals.append(Petal(x, y, height, width, is_static=is_static))
        
        # 如果花瓣总数不足，再随机添加一些
        remaining = count - len(petals)
        for _ in range(remaining):
            x = random.uniform(0, height)
            y = random.uniform(0, width)
            petals.append(Petal(x, y, height, width, is_static=is_static))
            
        return petals
    
    def play(self):
        """播放樱花花瓣雨动画"""
        try:
            # 确保黑色背景
            ensure_black_background()
            
            # 额外填充整个屏幕为黑色
            self._fill_background()
            
            # 获取屏幕尺寸
            height, width = self._get_terminal_size()
            
            # 创建静态背景花瓣（铺满屏幕的花瓣）
            static_petal_count = max(self.static_petals, int((height * width) / 25))  # 根据屏幕大小动态调整
            static_petals = self._create_initial_petals(static_petal_count, is_static=True)
            
            # 创建背景画布（含静态花瓣）
            static_canvas = self._create_background_canvas(static_petals)
            
            # 创建动态花瓣（会飘动的花瓣）
            dynamic_petal_count = max(self.num_petals, int((height * width) / 100))
            dynamic_petals = self._create_initial_petals(dynamic_petal_count, is_static=False)
            
            # 记录开始时间
            start_time = time.time()
            frame_count = 0
            
            # 播放动画直到达到指定时间
            while time.time() - start_time < self.duration:
                if self.stop_event.is_set():
                    break
                self._draw_frame(dynamic_petals, static_canvas, frame_count)
                time.sleep(0.1)  # 控制帧率
                frame_count += 1
                
            # 清屏并恢复黑色背景
            clear_screen()
            ensure_black_background()
            
        except KeyboardInterrupt:
            self.stop()
    
    def stop(self):
        """停止动画"""
        self.stop_event.set()
        clear_screen()
        ensure_black_background() 