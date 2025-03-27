import os
import platform

def supports_24bit_colors():
    """
    Detects if the terminal supports 24-bit colors.
    """
    term = os.environ.get("TERM", "")
    if platform.system() == "Windows":
        try:
            version_info = platform.version().split(".")
            major = int(version_info[0])
            minor = int(version_info[1])
            build = int(version_info[2])
            if major >= 10 and build >= 15063: # Windows 10 build 15063 (Creators Update) or later.
                return True
            else:
                return False

        except ValueError:
            return False

    if "256color" in term or "truecolor" in term or "xterm-256color" in term or "alacritty" in term or "konsole-256color" in term or "gnome-terminal" in term:
        return True

    colorterm = os.environ.get("COLORTERM", "")
    if colorterm in ("truecolor", "24bit"):
        return True

    return False

if __name__ == "__main__":
    if supports_24bit_colors():
        print("Yup, it does support 24 bit colors")
    else:
        print("Aww, no 24 bit colors for ya :(")