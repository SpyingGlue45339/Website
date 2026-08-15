import pygame
from pathlib import Path


# ---------------------------------------------------------
# COLOURS
# ---------------------------------------------------------

PAPER = (244, 240, 228)
PAPER_DARK = (232, 226, 210)
INK = (25, 25, 24)
INK_LIGHT = (88, 84, 77)
RED = (145, 35, 45)

PAGE_MARGIN = 64


# ---------------------------------------------------------
# FONT FILES
# ---------------------------------------------------------

FONT_DIR = Path(__file__).resolve().parent / "fonts"

SERIF_REGULAR = FONT_DIR / "LiberationSerif-Regular.ttf"
SERIF_BOLD = FONT_DIR / "LiberationSerif-Bold.ttf"
SERIF_ITALIC = FONT_DIR / "LiberationSerif-Italic.ttf"
SERIF_BOLD_ITALIC = FONT_DIR / "LiberationSerif-BoldItalic.ttf"

SANS_REGULAR = FONT_DIR / "LiberationSans-Regular.ttf"
SANS_BOLD = FONT_DIR / "LiberationSans-Bold.ttf"


# ---------------------------------------------------------
# FONT CACHE
# ---------------------------------------------------------

_font_cache = {}


def font(name, size, bold=False, italic=False):
    """
    Load a bundled font.

    The rest of the game can continue using:
        font("Georgia", ...)
        font("Arial", ...)

    but the actual font files are bundled with the game, so
    desktop and web versions render consistently.
    """

    key = (name.lower(), size, bold, italic)

    if key in _font_cache:
        return _font_cache[key]

    name_lower = name.lower()

    # Georgia / other serif requests
    if name_lower in (
        "georgia",
        "times",
        "times new roman",
        "serif",
    ):
        if bold and italic:
            font_path = SERIF_BOLD_ITALIC
        elif bold:
            font_path = SERIF_BOLD
        elif italic:
            font_path = SERIF_ITALIC
        else:
            font_path = SERIF_REGULAR

    # Arial / other sans-serif requests
    else:
        if bold:
            font_path = SANS_BOLD
        else:
            font_path = SANS_REGULAR

    try:
        loaded_font = pygame.font.Font(str(font_path), size)
    except (pygame.error, OSError):
        # This should only happen if a font file is missing.
        # Keep the game from completely crashing.
        loaded_font = pygame.font.SysFont(
            name,
            size,
            bold=bold,
            italic=italic,
        )

    _font_cache[key] = loaded_font
    return loaded_font


# ---------------------------------------------------------
# HORIZONTAL RULE
# ---------------------------------------------------------

def draw_rule(
    s,
    y,
    x1=PAGE_MARGIN,
    x2=None,
    width=2,
    colour=INK,
):
    if x2 is None:
        x2 = s.get_width() - PAGE_MARGIN

    pygame.draw.line(
        s,
        colour,
        (x1, y),
        (x2, y),
        width,
    )


# ---------------------------------------------------------
# TEXT WRAPPING
# ---------------------------------------------------------

def wrap_text(text, f, max_width):
    lines = []
    cur = ""

    for word in text.split():
        test = (cur + " " + word).strip()

        if f.size(test)[0] <= max_width:
            cur = test
        else:
            if cur:
                lines.append(cur)

            cur = word

    if cur:
        lines.append(cur)

    return lines