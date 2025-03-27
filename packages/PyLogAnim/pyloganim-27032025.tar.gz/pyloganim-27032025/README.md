# PyLogAnim - PYthon LOGo ANIMation

![PyLogAnim Logo](img/pyloganim.png)

---

A simple yet fancy tool to animate logos for your hacking scripts! >:3  

To run a demo, use:
```
python -m PyLogAnim
```


---

## Example Script

```python
import PyLogAnim

logo_altmono = [
    "    _   _ _                       ",
    "   /_\ | | |_ _ __  ___ _ _  ___  ",
    "  / _ \| |  _| '  \/ _ \ ' \/ _ \ ",
    " /_/ \_\_|\__|_|_|_\___/_||_\___/ ",
    "                                  "
]

PyLogAnim.animate_logo(logo=logo_altmono, colormode=PyLogAnim.colormodes.RGB, delay=0.01, reverse=False)
```
This will produce something like this (sadly without borders, as PyPi completely screwed up with those chars):<br>
![Altmono logo](img/altmono.png)

---
Tested in WT, MinGW Terminal. Should work in any other modern terminal that supports ANSI escape codes.

---
### animate_logo(logo,colormode,clear,delay,reverse)
logo - list of strings, with logo you want<br>
colormode - either one of the pre-determined color modes, or your own color/gradient, like [0,255,0] for a simple green or [[255,0,0],[0,0,255]] for a red-blue gradient<br>
clear - should terminal be cleared before showing<br>
delay - how fast or slow logo should reveal, set to 0 for instant showing<br>
reverse - should background be colored instead of the text itself

---
Color modes:<br>
from PyLogAnim.colormodes:
* RED
* GREEN
* BLUE
* YELLOW
* PURPLE
* CYAN
* WHITE
* BLACK
* RGB, RGB_DARK, RGB_DARKER
* RGB_DOUBLE, RGB_DOUBLE_DARK, RGB_DOUBLE_DARKER

---
Unlicense, 2025