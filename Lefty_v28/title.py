import pygame
import asyncio
import random
from style import *
from buttons import draw_button
from facts import FACTS
from reviews import run as reviews_screen
from audio import play_random_sound


from header import draw_header
TAGLINES = [
    ("A somewhat serious investigation into your political soul.", 2.0),
    ("Master debating politics since 2022.", 0.5),
    ("So back bench, it's actually fallen off.", 0.25),
    ("A name so bad, Joe Biden would be proud.", 0.25),
]


async def run(screen):
    clock = pygame.time.Clock()
    w, h = screen.get_size()

    play_rect = pygame.Rect(w // 2 - 160, 545, 320, 70)
    reviews_rect = pygame.Rect(PAGE_MARGIN, h - 58, 120, 34)

    all_facts = [fact for pool in FACTS.values() for fact in pool]
    title_fact = random.choice(all_facts)
    tagline = random.choices(
        [text for text, _ in TAGLINES],
        weights=[weight for _, weight in TAGLINES],
        k=1,
    )[0]

    while True:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    return "play"
                if event.key == pygame.K_ESCAPE:
                    return "quit"
                if event.key == pygame.K_r:
                    return "reviews"

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if reviews_rect.collidepoint(event.pos):
                    play_random_sound()
                    result = await reviews_screen(screen)
                    if result == "quit":
                        return "quit"
                    pygame.event.clear()
                    continue
                if play_rect.collidepoint(event.pos):
                    play_random_sound()
                    return "play"

        screen.fill(PAPER)

        label = font("Arial", 14, True).render(
            "POLITICAL COMPASS", True, RED
        )
        screen.blit(label, (PAGE_MARGIN, 45))
        draw_rule(screen, 72, PAGE_MARGIN, w - PAGE_MARGIN, 3)

        heading = font("Georgia", 64, True).render(
            "LEFTY SIMULATOR", True, INK
        )
        screen.blit(
            heading,
            (w // 2 - heading.get_width() // 2, 165),
        )

        sub_font = font("Georgia", 26)
        sub_lines = wrap_text(tagline, sub_font, w - 2 * PAGE_MARGIN)
        sub_y = 285
        for line in sub_lines:
            sub = sub_font.render(line, True, INK)
            screen.blit(
                sub,
                (w // 2 - sub.get_width() // 2, sub_y),
            )
            sub_y += 34

        draw_rule(screen, 350, PAGE_MARGIN + 100, w - PAGE_MARGIN - 100, 1, INK_LIGHT)

        fact_font = font("Georgia", 24, italic=True)
        fact_lines = wrap_text(title_fact, fact_font, w - 2 * PAGE_MARGIN)
        fact_y = 385
        for line in fact_lines[:3]:
            rendered = fact_font.render(line, True, INK)
            screen.blit(
                rendered,
                (w // 2 - rendered.get_width() // 2, fact_y),
            )
            fact_y += 31

        draw_button(
            screen,
            play_rect,
            "PLAY  →",
            mouse_pos,
            font_obj=font("Arial", 22, True),
        )

        draw_button(
            screen, reviews_rect, "REVIEWS", mouse_pos,
            font_obj=font("Arial", 12, True),
            border_width=1, hover_scale=1.03,
        )

        hint = font("Arial", 12).render(
            "CLICK PLAY   •   ENTER / SPACE TO START",
            True, INK_LIGHT,
        )
        screen.blit(
            hint,
            (w // 2 - hint.get_width() // 2, 635),
        )

        pygame.display.flip()
        await asyncio.sleep(1 / 60)
