from PyLogAnim import animate_logo
from PyLogAnim import colormodes
from PyLogAnim import demo_logos

print("RegularLogoTest")
animate_logo(logo=demo_logos.DEMOLOGO, colormode=colormodes.RGB, clear=False)

print("ReverseLogoTest")
animate_logo(logo=demo_logos.DEMOLOGO, colormode=colormodes.RGB_DARK, clear=False, reverse=True)

print("DiffColorsTest")
for md in [colormodes.RED, colormodes.GREEN, colormodes.BLUE, colormodes.YELLOW, colormodes.PURPLE, colormodes.CYAN, colormodes.WHITE, colormodes.BLACK, colormodes.RGB, colormodes.RGB_DARK, colormodes.RGB_DARKER, colormodes.RGB_DOUBLE, colormodes.RGB_DOUBLE_DARK, colormodes.RGB_DOUBLE_DARKER]:
    print(md)
    if not animate_logo(logo=demo_logos.DEMOLOGO_FILL, colormode=md, delay=0.01, clear=False):
        print("DiffColorsTest Cancelled")
        break

print("InstantTest")
animate_logo(logo=demo_logos.DEMOLOGO, colormode=colormodes.RGB, delay=0, clear=False)
animate_logo(logo=demo_logos.DEMOLOGO, colormode=colormodes.RGB_DARK, delay=0, clear=False,reverse=True)