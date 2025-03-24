import sys
import time
from typing import Optional

class WindchimeProgress:
    # 定义可用的风铃样式
    STYLES = {
        'fengling': '🎐',    # 风铃
        'ala': '🍎',         # 红苹果
        'blueberry': '🫐',   # 蓝莓
        'green_apple': '🍏', # 青苹果
        'orange': '🍊',      # 橘子
        'grape': '🍇',       # 葡萄
        'strawberry': '🍓',  # 草莓
        'peach': '🍑',       # 桃子
        'pear': '🍐',        # 梨
        'banana': '🍌',      # 香蕉
        'watermelon': '🍉',  # 西瓜
        'bell': '🔔',        # 铃铛
        'chime': '🎋',       # 七夕竹子（带铃铛装饰）
        'temple': '⛩️',      # 神社（通常挂有风铃）
        'ribbon': '🎀',      # 丝带（可以用作装饰风铃）
        'sparkle': '✨',     # 闪烁（可以表示风铃声）
        'star': '⭐',        # 星星
        'crystal': '💎',     # 水晶（像风铃）
        'running': '🏃',     # 跑步
        'rocket': '🚀',      # 火箭
    }

    def __init__(self, total: int, width: int = 20, style: str = 'fengling'):
        self.total = total
        self.width = width
        self.current = 0
        self.start_time = time.time()
        
        # 设置风铃样式
        if style not in self.STYLES:
            print(f"Warning: Style '{style}' not found. Using default 'fengling'.")
            style = 'fengling'
        self.windchime = self.STYLES[style]
        self.empty = "　"  # 使用全角空格，保持对齐
        
        # ANSI转义序列，用于添加颜色
        self.BLUE = "\033[94m"
        self.GREEN = "\033[92m"
        self.CYAN = "\033[96m"
        self.PURPLE = "\033[95m"
        self.YELLOW = "\033[93m"
        self.RED = "\033[91m"
        self.ORANGE = "\033[33m"  # 添加橙色
        self.RESET = "\033[0m"
        
        # 根据不同的样式选择不同的颜色
        self.style_colors = {
            'ala': self.RED,          # 红苹果用红色
            'blueberry': self.BLUE,   # 蓝莓用蓝色
            'green_apple': self.GREEN, # 青苹果用绿色
            'orange': self.ORANGE,     # 橘子用橙色
            'grape': self.PURPLE,      # 葡萄用紫色
            'strawberry': self.RED,    # 草莓用红色
            'peach': self.YELLOW,      # 桃子用黄色
            'pear': self.GREEN,        # 梨用绿色
            'banana': self.YELLOW,     # 香蕉用黄色
            'watermelon': self.GREEN,  # 西瓜用绿色
            'fengling': self.BLUE,
            'bell': self.YELLOW,
            'chime': self.GREEN,
            'temple': self.RED,
            'ribbon': self.PURPLE,
            'sparkle': self.YELLOW,
            'star': self.YELLOW,
            'crystal': self.CYAN,
            'running': self.RED,       # 跑步用红色
            'walking': self.GREEN,     # 走路用绿色
            'strolling': self.BLUE,    # 散步用蓝色
            'rocket': self.YELLOW,     # 火箭用黄色
        }
        self.color = self.style_colors.get(style, self.BLUE)
        
    def update(self, n: int) -> None:
        """Update the progress bar with the current value."""
        self.current = n
        self._display()
        
    def _display(self) -> None:
        """Display the current progress."""
        # Calculate percentage
        percentage = (self.current / self.total) * 100
        
        # Calculate filled length
        filled = int(self.width * self.current / self.total)
        # 使用选定的图标作为进度条填充，添加颜色
        bar = self.color + self.windchime * filled + self.RESET + self.empty * (self.width - filled)
        
        # Calculate elapsed time
        elapsed = time.time() - self.start_time
        
        # Create progress string with colored percentage
        progress_str = f"\r[{bar}] {self.GREEN}{percentage:.1f}%{self.RESET} | {self.current}/{self.total} | {elapsed:.1f}s"
        
        # Write to stdout
        sys.stdout.write(progress_str)
        sys.stdout.flush()
        
    def finish(self) -> None:
        """Complete the progress bar."""
        self.update(self.total)
        print()  # New line after completion
        
    @classmethod
    def available_styles(cls) -> list:
        """Return a list of available progress bar styles."""
        return list(cls.STYLES.keys())
    
    @classmethod
    def show_styles(cls) -> None:
        """展示所有可用的样式及其效果"""
        print("\n可用的进度条样式：")
        print("-" * 50)
        print("\n水果样式：")
        fruit_styles = ['ala', 'blueberry', 'green_apple', 'orange', 'grape', 
                       'strawberry', 'peach', 'pear', 'banana', 'watermelon']
        for style in fruit_styles:
            icon = cls.STYLES[style]
            print(f"样式名称: {style:15} 图标: {icon}")
            
        print("\n装饰样式：")
        other_styles = [s for s in cls.STYLES if s not in fruit_styles]
        for style in other_styles:
            icon = cls.STYLES[style]
            print(f"样式名称: {style:15} 图标: {icon}")
        print("-" * 50)
        
        print("\n使用示例：")
        print("from fengling import WindchimeProgress")
        print("# 水果样式")
        print("progress = WindchimeProgress(total=100, style='ala')        # 红苹果样式")
        print("progress = WindchimeProgress(total=100, style='blueberry')  # 蓝莓样式")
        print("progress = WindchimeProgress(total=100, style='orange')     # 橘子样式")
        print("\n# 装饰样式")
        print("progress = WindchimeProgress(total=100, style='fengling')   # 风铃样式")
        print("\n可用的样式名称：")
        print(", ".join(cls.STYLES.keys())) 