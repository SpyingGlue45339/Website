import math
import pygame
import asyncio
from style import PAPER, INK, INK_LIGHT, RED, PAGE_MARGIN, font, draw_rule
from buttons import draw_button

REVIEWS = [('As useless as a marzipan dildo', 'Malcom Tucker', 1), ('This test is spiffing', 'Martin Luther King', 4), ('Muy Bien', 'Pierre Delecto', 5), ('My friends like this test', 'a sheep', 5), ('Better than Brexit', 'Nigel Farage', 4), ('I had great fun doing the err...you know... oh, you know the thing', 'Joe Biden', 3)]

def wrap_text_local(text, fnt, max_width):
    words = text.split()
    lines, current = [], ""
    for word in words:
        test = word if not current else current + " " + word
        if fnt.size(test)[0] <= max_width:
            current = test
        else:
            if current: lines.append(current)
            current = word
    if current: lines.append(current)
    return lines

def star_points(cx, cy, radius):
    points = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        r = radius if i % 2 == 0 else radius * .42
        points.append((cx + math.cos(a)*r, cy + math.sin(a)*r))
    return points

def draw_stars(screen, x, y, rating):
    for i in range(5):
        cx = x + i * 27
        pygame.draw.polygon(
            screen,
            RED if i < rating else PAPER,
            star_points(cx, y, 10)
        )
        if i >= rating:
            pygame.draw.polygon(screen, INK_LIGHT, star_points(cx, y, 10), 1)

async def run(screen):
    clock = pygame.time.Clock()
    while True:
        w, h = screen.get_size()
        mouse = pygame.mouse.get_pos()
        back = pygame.Rect(w//2-145, h-82, 290, 58)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "back"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if back.collidepoint(event.pos):
                    return "back"

        screen.fill(PAPER)
        title = font("Georgia", 46, True).render("REVIEWS", True, INK)
        screen.blit(title, (PAGE_MARGIN, 38))
        draw_rule(screen, 98, PAGE_MARGIN, w-PAGE_MARGIN, 3, INK)

        sub = font("Arial", 14, True).render(
            "WHAT THE PUBLIC HAS TO SAY", True, RED)
        screen.blit(sub, (PAGE_MARGIN, 118))

        y = 165
        qfont = font("Georgia", 23, italic=True)
        afont = font("Arial", 18, True)

        for quote, author, rating in REVIEWS:
            for line in wrap_text_local(
                "'" + quote + "'", qfont, w-2*PAGE_MARGIN-235
            ):
                screen.blit(qfont.render(line, True, INK), (PAGE_MARGIN, y))
                y += 27

            author_y = y + 1
            screen.blit(
                afont.render("— " + author, True, INK_LIGHT),
                (PAGE_MARGIN, author_y)
            )

            stars_width = 4 * 27 + 20
            draw_stars(
                screen,
                w-PAGE_MARGIN-stars_width+10,
                author_y + 10,
                rating
            )

            y += 36
            if y > h-130:
                break

        draw_button(
            screen, back, "BACK", mouse,
            font_obj=font("Arial", 20, True)
        )
        pygame.display.flip()
        await asyncio.sleep(1 / 60)
