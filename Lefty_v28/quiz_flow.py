import pygame
from audio import play_random_sound
import random
import asyncio

from style import *
from question_page import draw as draw_question, answer_rects
from questions import SECTIONS, QUESTIONS
from scoring import score_question, RESPONSE_LABELS
from buttons import draw_button
from facts import FACTS
from results import run as results_screen

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

def _draw_section(screen, section_index, question_count, fact):
    screen.fill(PAPER)
    w, h = screen.get_size()
    name, qs = SECTIONS[section_index]

    title, strapline, description = SECTION_CONTENT[name]
    label = font("Arial", 16, True).render(
        f"THE POLITICAL COMPASS   •   PART {section_index + 1} OF {len(SECTIONS)}",
        True,
        RED,
    )
    screen.blit(label, (PAGE_MARGIN, 32))
    draw_rule(screen, 72, PAGE_MARGIN, w - PAGE_MARGIN, 3, INK)

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

    # Newspaper item: every item in the section has equal odds.
    fact_font = font("Georgia", 24, italic=True)
    fact_lines = wrap_text(
        fact,
        fact_font,
        w - 2 * PAGE_MARGIN,
    )
    fact_y = 415
    for line in fact_lines[:3]:
        rendered = fact_font.render(line, True, INK)
        screen.blit(rendered, (PAGE_MARGIN, fact_y))
        fact_y += 34

    button = pygame.Rect(PAGE_MARGIN, 555, w - 2 * PAGE_MARGIN, 78)
    draw_button(
        screen,
        button,
        "READ THE QUESTIONS  →",
        pygame.mouse.get_pos(),
        font_obj=font("Arial", 21, True),
    )

    hint = font("Arial", 12).render(
        "CLICK TO CONTINUE   •   ENTER / SPACE TO CONTINUE",
        True, INK_LIGHT,
    )
    screen.blit(hint, (w // 2 - hint.get_width() // 2, h - 30))


async def run(screen):
    """
    The complete quiz flow.

    There is exactly ONE Pygame event loop here. Section fronts, questions
    and interludes are states of this loop rather than separate functions
    that each consume their own event queues.

        section -> question -> question -> ... -> next section
                 -> question -> ... -> results

    This is deliberately boring architecture: one owner for input, one
    place where state changes, and no return-value hand-offs between pages.
    """
    clock = pygame.time.Clock()

    section_index = 0
    question_index = 0
    global_question_number = 0

    x = 0.0
    y = 0.0

    # Keep a compact audit trail for the analysis page. The main compass
    # never displays these figures; they only appear when ANALYSE RESULTS
    # is deliberately opened.
    section_scores = {
        name: [0.0, 0.0] for name, _ in SECTIONS
    }

    state = "section"
    selected = None
    section_fact = random.choice(FACTS[SECTIONS[0][0]])

    while True:
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                return None

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return None

            if state == "section":
                if event.type == pygame.KEYDOWN and event.key in (
                    pygame.K_RETURN, pygame.K_SPACE
                ):
                    play_random_sound()
                    state = "question"
                    selected = None
                    pygame.event.clear()
                    continue

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    play_random_sound()
                    state = "question"
                    selected = None
                    pygame.event.clear()
                    continue

            elif state == "question":
                name, questions = SECTIONS[section_index]
                q = questions[question_index]

                if event.type == pygame.KEYDOWN:
                    keys = [
                        pygame.K_1, pygame.K_2,
                        pygame.K_3, pygame.K_4,
                    ]
                    keypad = [
                        pygame.K_KP1, pygame.K_KP2,
                        pygame.K_KP3, pygame.K_KP4,
                    ]

                    for i in range(4):
                        if event.key in (keys[i], keypad[i]):
                            selected = i

                    if (
                        event.key in (pygame.K_RETURN, pygame.K_SPACE)
                        and selected is not None
                    ):
                        play_random_sound()
                        x_delta, y_delta = score_question(q, selected)
                        x += x_delta
                        y += y_delta
                        section_name = q.get("section", SECTIONS[section_index][0])
                        section_scores[section_name][0] += x_delta
                        section_scores[section_name][1] += y_delta

                        question_index += 1
                        global_question_number += 1
                        selected = None

                        if question_index >= len(questions):
                            if section_index >= len(SECTIONS) - 1:
                                max_x = sum(abs(q["x"]) for q in QUESTIONS)
                                max_y = sum(abs(q["y"]) for q in QUESTIONS)
                                result = results_screen(
                                    screen, x, y, max_x, max_y,
                                    [(name, vals[0], vals[1])
                                     for name, vals in section_scores.items()]
                                )
                                if result == "again":
                                    return "again"
                                return None

                            section_index += 1
                            question_index = 0
                            state = "section"
                            section_fact = random.choice(FACTS[SECTIONS[section_index][0]])

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for i, rect in enumerate(answer_rects(screen, q)):
                        if rect.collidepoint(event.pos):
                            play_random_sound()
                            x_delta, y_delta = score_question(q, i)
                            x += x_delta
                            y += y_delta
                            section_name = q.get("section", SECTIONS[section_index][0])
                            section_scores[section_name][0] += x_delta
                            section_scores[section_name][1] += y_delta

                            question_index += 1
                            global_question_number += 1
                            selected = None

                            if question_index >= len(questions):
                                if section_index >= len(SECTIONS) - 1:
                                    max_x = sum(abs(q["x"]) for q in QUESTIONS)
                                    max_y = sum(abs(q["y"]) for q in QUESTIONS)
                                    result = await results_screen(
                                        screen, x, y, max_x, max_y,
                                        [(name, vals[0], vals[1])
                                        for name, vals in section_scores.items()]
                                    )
                                    if result == "again":
                                        return "again"
                                    return None

                                section_index += 1
                                question_index = 0
                                state = "section"
                                section_fact = random.choice(FACTS[SECTIONS[section_index][0]])
                            break

        if state == "section":
            _draw_section(
                screen,
                section_index,
                len(SECTIONS[section_index][1]),
                section_fact,
            )

        elif state == "question":
            q = SECTIONS[section_index][1][question_index]
            draw_question(
                screen,
                q,
                global_question_number + 1,
                len(QUESTIONS),
                selected,
                photo_number=question_index + 1,
            )

        pygame.display.flip()
        await asyncio.sleep(1 / 60)
