import pygame
from style import INK, PAPER, PAPER_DARK, RED


def draw_button(screen, rect, text, mouse_pos, *,
                normal_fill=PAPER_DARK,
                hover_fill=RED,
                normal_text=INK,
                hover_text=PAPER,
                border=INK,
                font_obj=None,
                border_width=2,
                hover_scale=1.035):
    """Draw a consistent newspaper button with a subtle hover expansion."""
    hovered = rect.collidepoint(mouse_pos)

    if hovered:
        draw_rect = rect.inflate(
            int(rect.width * (hover_scale - 1)),
            int(rect.height * (hover_scale - 1)),
        )
    else:
        draw_rect = rect

    pygame.draw.rect(
        screen,
        hover_fill if hovered else normal_fill,
        draw_rect,
    )
    pygame.draw.rect(
        screen,
        border,
        draw_rect,
        border_width,
    )

    if font_obj is None:
        from style import font
        font_obj = font("Arial", 24, True)

    current_font = font_obj
    max_width = max(20, draw_rect.width - 18)
    rendered = current_font.render(
        text,
        True,
        hover_text if hovered else normal_text,
    )
    while rendered.get_width() > max_width and current_font.get_height() > 11:
        current_font = font("Arial", current_font.get_height() - 1, True)
        rendered = current_font.render(
            text,
            True,
            hover_text if hovered else normal_text,
        )
    screen.blit(
        rendered,
        (
            draw_rect.centerx - rendered.get_width() // 2,
            draw_rect.centery - rendered.get_height() // 2,
        ),
    )
    return hovered
