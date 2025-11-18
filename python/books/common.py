from typing import Tuple


def print_confirmation(file: str) -> None:
    print(f". {file}")

def hex_to_rgba(hex_color: str, alpha: int) -> Tuple[int, int, int, int]:
    hex_color = hex_color.lstrip("#")
    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    return (r, g, b, alpha)

def invert_color(hex_color: str) -> str:
    hex_color = hex_color.lstrip("#")
    r, g, b = 255 - int(hex_color[0:2], 16), 255 - int(hex_color[2:4], 16), 255 - int(hex_color[4:6], 16)
    return f"#{r:02X}{g:02X}{b:02X}"
