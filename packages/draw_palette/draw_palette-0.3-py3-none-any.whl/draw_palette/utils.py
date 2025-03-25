"""
Utils module
"""

import lupa


def get_text_color(hex_color):
    """
    Getting the color to contrast with the background
            Parameters:
                    hex_color (str): String of hex color

            Returns:
                    color (str): String of the color
    """
    hex_color = hex_color.lstrip("#")
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    brightness = 0.299 * r + 0.587 * g + 0.114 * b
    return "white" if brightness < 128 else "black"


def import_palette(file: str) -> list:
    """
    Import palette from lua file
        Input parameters:
                - file(str) path to a Lua file with a palette table
    """
    lua = lupa.LuaRuntime()

    with open(file, "r", encoding="utf-8") as f:
        lua_code = f.read()
    palette = []
    lua_palette = lua.execute(lua_code)  # pyright: ignore
    for color in lua_palette.items():  # pyright: ignore
        palette.append((color[0], color[1]))

    return palette
