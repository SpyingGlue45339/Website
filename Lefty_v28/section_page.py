import pygame
import random
from style import *
from buttons import draw_button
from facts import FACTS
from audio import play_random_noise

SECTION_CONTENT = {
    "Economy": (
        "THE ECONOMIC QUESTION",
        "PROPERTY • MARKETS • WEALTH",
        "Who owns things? Who pays for them? How much should the state "
        "interfere with markets, property and the distribution of wealth?"
    ),
    "Government": (
        "THE QUESTION OF POWER",
        "AUTHORITY • FREEDOM • THE STATE",
        "How much authority should government possess, and what should "
        "happen when the state and the individual disagree?"
    ),
    "Society": (
        "THE SOCIAL QUESTION",
        "FAMILY • FREEDOM • SOCIAL CHANGE",
        "How should people live? How much should tradition, personal "
        "freedom, family and changing social norms matter?"
    ),
    "Culture": (
        "THE CULTURAL QUESTION",
        "NATION • IDENTITY • TRADITION",
        "What makes a country a country? Consider identity, immigration, "
        "tradition, national independence and cultural change."
    ),
}

SECTION_ORDER = ["Economy", "Government", "Society", "Culture"]


def run(screen, section, start=None, end=None):
    clock = pygame.time.Clock()
    w, h = screen.get_size()
    title, strapline, description = SECTION_CONTENT[section]
    part = SECTION_ORDER.index(section) + 1
    fact = random.choice(FACTS[section])
    button = pygame.Rect(PAGE_MARGIN, 555, w - 2 * PAGE_MARGIN, 78)

    pygame.event.clear()

    while True:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "quit"
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    play_random_noise()
                    return "continue"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                play_random_noise()
                return "continue"

        screen.fill(PAPER)
        label = font("Arial", 14, True).render(
            f"POLITICAL COMPASS   •   PART {part} OF 4",
            True, RED
        )
        screen.blit(label, (PAGE_MARGIN, 45))
        draw_rule(screen, 72, PAGE_MARGIN, w - PAGE_MARGIN, 3)

        heading = font("Georgia", 58, True).render(title, True, INK)
        screen.blit(heading, (PAGE_MARGIN, 125))

        strap = font("Arial", 16, True).render(strapline, True, RED)
        screen.blit(strap, (PAGE_MARGIN, 205))
        draw_rule(screen, 235, PAGE_MARGIN, w - PAGE_MARGIN, 1, INK_LIGHT)

        body = font("Georgia", 27)
        y = 275
        for line in wrap_text(description, body, w - 2 * PAGE_MARGIN):
            screen.blit(body.render(line, True, INK), (PAGE_MARGIN, y))
            y += 39

        fact_font = font("Georgia", 24)
        fact_lines = wrap_text(fact, fact_font, w - 2 * PAGE_MARGIN)
        fact_y = 405
        for line in fact_lines[:3]:
            rendered = fact_font.render(line, True, INK)
            screen.blit(rendered, (PAGE_MARGIN, fact_y))
            fact_y += 34

        draw_button(
            screen,
            button,
            "READ THE QUESTIONS  →",
            mouse_pos,
            font_obj=font("Arial", 21, True),
        )

        hint = font("Arial", 12).render(
            "CLICK TO CONTINUE   •   ENTER / SPACE TO CONTINUE   •   ESC TO QUIT",
            True, INK_LIGHT
        )
        screen.blit(hint, (w // 2 - hint.get_width() // 2, h - 30))

        pygame.display.flip()
        clock.tick(60)
