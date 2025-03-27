import time
import colorama
from colorama import Cursor

from . import termcheck
from . import colormodes
from . import demo_logos

colorama.init()

DELAY = 0.05

def animate_logo(logo: list = demo_logos.DEMOLOGO, colormode: list = colormodes.RGB, delay: float = DELAY, clear: bool = True, reverse: bool = False):
    """
    Animate your logo silly.
    
    Args:
        logo (list): Your logo, every row should be the same length 
        colormode (list): Color mode to animate your logo in
        delay (float): Delay between frames
        clear (bool): Clear the screen before animating
        reverse (bool): Change the color of background instead of text
        
    Returns:
        bool: Either returns True when animation successfully finishes, or False when user cancels it (Ctrl-C)
        
    Example
        >>> animate_logo(logo=["Sick ","Multi","Line ","Logo "])
        True
    """
    if not isinstance(logo, list):
        print("Logo should be a list")
        return None
    if not isinstance(colormode, list):
        print("Color mode should be a list")
        return None
    if not isinstance(delay, (int, float)) or delay < 0:
        print("Delay should be a non-negative number")
        return None
    if not isinstance(clear, bool):
        print("Clear should be a bool")
        return None
    if not isinstance(reverse, bool):
        print("Reverse should be a bool")
        return None
    
    if termcheck.supports_24bit_colors():
        if clear:
            print('\033[H\033[J', end='')
        num_cols = len(logo[0])
        num_rows = len(logo)

        print("\n" * num_rows)
        current_display = [' ' * num_cols for _ in range(num_rows)]

        def get_rgb_color(col_index, max_cols, color_mode):
            if isinstance(color_mode, list):
                if all(isinstance(element, int) for element in color_mode):
                    r, g, b = color_mode
                    if reverse:
                        return f"\033[48;2;{r};{g};{b}m"
                    else:
                        return f"\033[38;2;{r};{g};{b}m"
                elif all(isinstance(element, list) and all(isinstance(sub_element, int) for sub_element in element) for element in color_mode):  # gradient
                    color_list = color_mode
                    pos = (col_index / max_cols) * (len(color_list) - 1)
                    segment = int(pos)
                    fraction = pos - segment
                    if segment >= len(color_list) - 1:
                        r1, g1, b1 = color_list[-1]
                        r2, g2, b2 = color_list[-1]
                    else:
                        r1, g1, b1 = color_list[segment]
                        r2, g2, b2 = color_list[segment + 1]

                    r = int(r1 + (r2 - r1) * fraction)
                    g = int(g1 + (g2 - g1) * fraction)
                    b = int(b1 + (b2 - b1) * fraction)

                    if reverse:
                        return f"\033[48;2;{r};{g};{b}m"
                    else:
                        return f"\033[38;2;{r};{g};{b}m"
                else:
                    return "\033[0m"
            else:
                return "\033[0m"

        try:
            if delay == 0:
                print(Cursor.UP(num_rows), end="")
                for line in logo:
                    colored_line = ''
                    for k, char in enumerate(line):
                        colored_line += get_rgb_color(k, num_cols - 1, colormode) + char
                    print(colored_line + "\033[0m")
            else:
                for i in range(num_cols):
                    for j in range(num_rows):
                        current_display[j] = current_display[j][:i] + logo[j][i] + current_display[j][i + 1:]

                    print(Cursor.UP(num_rows), end="")
                    for line in current_display:
                        colored_line = ''
                        for k, char in enumerate(line):
                            if k <= i:
                                colored_line += get_rgb_color(k, num_cols - 1, colormode) + char
                            else:
                                colored_line += char
                        print(colored_line + "\033[0m")
                    time.sleep(delay)

                print(Cursor.UP(num_rows), end="")
                for line in logo:
                    colored_line = ''
                    for k, char in enumerate(line):
                        colored_line += get_rgb_color(k, num_cols - 1, colormode) + char
                    print(colored_line + "\033[0m")
            colorama.deinit()
            return True
        except KeyboardInterrupt:
            colorama.deinit()
            return False
    else:
        print("Your terminal doesn't support 24bit colors, sorry...")
        return
