from tkinter.ttk import Progressbar
import blessed, time, math

term = blessed.Terminal()

def progress(progress : float, width : int):
        # 0 <= progress <= 1
        progress = min(1, max(0, progress))
        whole_width = math.floor(progress * width)
        remainder_width = (progress * width) % 1
        part_width = math.floor(remainder_width * 8)
        part_char = [" ", "▏", "▎", "▍", "▌", "▋", "▊", "▉"][part_width]
        if (width - whole_width - 1) < 0:
          part_char = ""
        line = "█" * whole_width + part_char + " " * (width - whole_width - 1)
        return line

for i in range(0, 101):
    print(term.home + term.clear)
    print(term.normal + term.gold + progress(i/100, 100))
    time.sleep(0.0002)