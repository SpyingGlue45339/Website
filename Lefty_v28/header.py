import pygame
from style import INK, INK_LIGHT, RED, PAGE_MARGIN, font, draw_rule


def draw_question_header(screen, number, total):
    w, _ = screen.get_size()
    label = font("Arial", 16, True).render(
        f"POLITICAL COMPASS   •   QUESTION {number:02d} OF {total:02d}",
        True, RED
    )
    screen.blit(label, (PAGE_MARGIN, 45))
    draw_rule(screen, 72, PAGE_MARGIN, w - PAGE_MARGIN, 3, INK)



def draw_simple_header(screen, title):
    """Reusable clean header for non-question pages."""
    w, _ = screen.get_size()
    label = font("Arial", 16, True).render(title, True, RED)
    screen.blit(label, (PAGE_MARGIN, 32))
    draw_rule(screen, 72, PAGE_MARGIN, w - PAGE_MARGIN, 3, INK)


def draw_header(screen):
    """Compatibility wrapper for the title screen's existing import."""
    draw_simple_header(screen, "POLITICAL COMPASS")
