import pygame

from style import *
from buttons import draw_button
from question_photos import photo_for_question, PHOTO_BOX
from header import draw_question_header


ANSWER_LABELS = [
    "STRONGLY DISAGREE",
    "DISAGREE",
    "AGREE",
    "STRONGLY AGREE",
]


def answer_rects(screen, q=None):
    """Four equal-width answer buttons, raised comfortably from the bottom."""
    w, h = screen.get_size()

    margin = PAGE_MARGIN
    gap = 12
    available = w - 2 * margin
    button_width = (available - 3 * gap) // 4
    button_height = 72

    # 55 px of breathing room below the buttons.
    y = h - 127

    return [
        pygame.Rect(
            margin + i * (button_width + gap),
            y,
            button_width,
            button_height,
        )
        for i in range(4)
    ]


def _draw_question_text(screen, text, top_y, max_width):
    """Draw the question and return the y-coordinate immediately below it."""
    # Use a slightly smaller font automatically for unusually long questions.
    size = 34
    while size > 24:
        qfont = font("Georgia", size)
        lines = wrap_text(text, qfont, max_width)
        if len(lines) <= 3:
            break
        size -= 2

    line_height = size + 10
    y = top_y

    for line in lines:
        rendered = qfont.render(line, True, INK)
        screen.blit(
            rendered,
            (screen.get_width() // 2 - rendered.get_width() // 2, y),
        )
        y += line_height

    return y


def draw(screen, q, number, total, selected=None, photo_number=None):
    w, h = screen.get_size()
    screen.fill(PAPER)

    # Clean question masthead. LEFTY SIMULATOR deliberately does not appear.
    draw_question_header(screen, number, total)

    category = q.get("section", q.get("category", "POLITICS"))
    cat = font("Arial", 14, True).render(
        str(category).upper(),
        True,
        RED,
    )
    screen.blit(cat, (PAGE_MARGIN, 91))

    # Question is centred above the image.
    question_bottom = _draw_question_text(
        screen,
        q["question"],
        128,
        w - 2 * PAGE_MARGIN,
    )

    # Every question has the same photo area, regardless of source image
    # dimensions. The actual photo is contained proportionally inside it.
    if photo_number is not None:
        photo = photo_for_question(str(category), photo_number)

        box_w, box_h = PHOTO_BOX
        box_left = (w - box_w) // 2
        box_top = 270

        # If a particularly long question needs more room, move the photo
        # down, but never let it collide with the answer buttons.
        if question_bottom > box_top - 18:
            box_top = min(question_bottom + 18, h - 430)

        if photo is not None:
            photo_rect = photo.get_rect()
            photo_rect.center = (
                box_left + box_w // 2,
                box_top + box_h // 2,
            )
            screen.blit(photo, photo_rect)

    rects = answer_rects(screen, q)
    mouse_pos = pygame.mouse.get_pos()

    for i, rect in enumerate(rects):
        draw_button(
            screen,
            rect,
            ANSWER_LABELS[i],
            mouse_pos,
            font_obj=font("Arial", 20, True),
        )

        if selected == i:
            # A clear selected state without changing the geometry.
            pygame.draw.rect(screen, RED, rect, 3)

    hint = font("Arial", 11).render(
        "CLICK AN ANSWER   •   1–4 TO SELECT   •   ENTER / SPACE TO CONFIRM",
        True,
        INK_LIGHT,
    )
    screen.blit(
        hint,
        (w // 2 - hint.get_width() // 2, h - 31),
    )
