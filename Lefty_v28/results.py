import pygame
import asyncio

from style import *
from buttons import draw_button
from audio import play_random_sound
from questions import SECTIONS


QUADRANT_COLOURS = {
    "tl": (177, 91, 99),
    "tr": (188, 150, 91),
    "bl": (104, 145, 121),
    "br": (101, 130, 157),
}

# ---------------------------------------------------------------------------
# Personalised result writing
# ---------------------------------------------------------------------------

OVERALL_TEXT = {
    ("left", "authority"): (
        "Your answers point towards a more collective view of economics and society, "
        "combined with a greater willingness to accept state authority. You are more "
        "comfortable with government taking an active role in shaping outcomes, and "
        "you place more weight on collective goals, public provision and social order "
        "than on leaving decisions entirely to individuals or markets.\n\n"
        "Across the test, your answers suggest that you are willing to use collective "
        "power when you think it can produce a better social outcome. You are not simply "
        "interested in government for its own sake: what matters is whether institutions "
        "can deliver the things you think society should provide and protect."
    ),
    ("left", "liberty"): (
        "Your answers point towards a more collective view of economics and society, "
        "while also placing a strong value on individual freedom. You are more drawn "
        "to redistribution, public provision and collective solutions, but you are also "
        "reluctant to give the state unnecessary power over how people live.\n\n"
        "That combination is important. Your answers do not suggest that you see a larger "
        "role for government as a reason to control personal behaviour. You can support "
        "collective solutions to shared problems while still wanting people to retain "
        "considerable freedom in their own lives."
    ),
    ("right", "authority"): (
        "Your answers point towards a more market-oriented and traditional outlook, "
        "combined with a greater willingness to accept state authority. You place more "
        "weight on private ownership, personal responsibility and established norms, "
        "while being relatively comfortable with government using its powers to maintain "
        "order, enforce rules and protect social stability.\n\n"
        "Your result therefore combines two instincts that are sometimes treated as "
        "opposites: economic or social preference for individual responsibility, alongside "
        "a willingness to accept firm institutions when you think rules, order or continuity "
        "matter."
    ),
    ("right", "liberty"): (
        "Your answers point towards a more market-oriented outlook alongside a strong "
        "commitment to individual freedom. You place more weight on private ownership, "
        "personal responsibility and voluntary choice, and you are reluctant to use state "
        "power to control peaceful individual behaviour.\n\n"
        "The common thread in your answers is a preference for allowing people considerable "
        "room to make their own choices. You are more comfortable with decisions being left "
        "to individuals, families, businesses and voluntary associations than with government "
        "directing them from above."
    ),
    ("left", "middle"): (
        "Your answers lean towards collective and economically interventionist ideas, "
        "but your views on the amount of authority government should exercise are much "
        "more mixed. You can favour a stronger collective role in some areas without "
        "necessarily wanting the state to control how people live.\n\n"
        "This makes your result less about a general enthusiasm for government power and "
        "more about particular outcomes. You appear willing to support collective action "
        "where you think it solves a problem, while remaining less settled about how far "
        "government should go in enforcing rules or regulating personal behaviour."
    ),
    ("right", "middle"): (
        "Your answers lean towards markets, private ownership and individual economic "
        "responsibility, while your views on state authority are more mixed. You can "
        "favour a market-oriented economy without having a consistently strong view for "
        "or against government power in personal and social matters.\n\n"
        "In other words, your economic instincts are clearer than your position on authority. "
        "You tend to give individuals and markets more room to make decisions, but your answers "
        "do not produce one simple rule for how much power government should have elsewhere."
    ),
    ("middle", "authority"): (
        "Your answers do not show a strong overall preference between the collective and "
        "market-oriented sides of the economic spectrum. What stands out more clearly is "
        "your greater comfort with state authority, rules and collective enforcement when "
        "you believe they are needed for order or wider social goals.\n\n"
        "You therefore look less ideologically committed on the economic dimension than on "
        "the question of authority. Your answers suggest that the justification for rules, "
        "institutions and enforcement matters more to you than whether a policy is conventionally "
        "described as left or right."
    ),
    ("middle", "liberty"): (
        "Your answers do not show a strong overall preference between collective and "
        "market-oriented economics. What stands out more clearly is your preference for "
        "individual freedom: you are generally cautious about giving government power to "
        "control peaceful choices or impose unnecessary restrictions.\n\n"
        "You therefore appear more pragmatic about economic arrangements than about personal "
        "freedom. You can accept different economic solutions depending on the problem, but "
        "you are more consistently wary of unnecessary state control over individual life."
    ),
    ("middle", "middle"): (
        "Your answers sit relatively close to the middle on both dimensions. Rather than "
        "following one consistent ideological direction, you appear to weigh the issue "
        "in front of you: sometimes favouring collective action, sometimes individual or "
        "market choice, and sometimes accepting authority where you think it is justified.\n\n"
        "That does not necessarily mean you have no political views. It suggests that your "
        "answers are less easily captured by one ideological label: the details of the policy "
        "and the circumstances around it seem to matter more to you than consistently choosing "
        "the same side of every political argument."
    ),
}

SECTION_AXIS_TEXT = {
    "Economy": {
        "x_neg": "You favour a more collective economic model. Your answers suggest greater support for public ownership, redistribution, stronger worker power and an active state role in deciding how economic resources are organised.",
        "x_pos": "You favour a more market-oriented economic model. Your answers suggest greater support for private ownership, voluntary exchange, personal responsibility and allowing businesses and individuals to make more economic decisions for themselves.",
        "y_neg": "Your answers indicate greater reluctance to use state direction in economic life. Here this is an economic-intervention measure, not a measure of personal liberty.",
        "y_pos": "Your answers indicate greater acceptance of government intervention in the economy through regulation, redistribution, public provision or direct action. Here this is an economic-intervention measure, not a measure of personal authority.",
    },
    "Government": {
        "x_neg": "Within this section, your answers show a slight tendency towards the more socially collective side of the spectrum, although the main issue being tested here is the power and role of the state rather than economics.",
        "x_pos": "Within this section, your answers show a slight tendency towards the more individual or traditional side of the spectrum, although the main issue being tested here is the power and role of the state rather than economics.",
        "y_neg": "You place a strong value on individual liberty. Your answers suggest that government should generally leave peaceful people alone, protect freedom of expression and be cautious about surveillance, punishment and restrictions on personal choice.",
        "y_pos": "You are more comfortable with state authority. Your answers suggest that public order, security, obedience and the enforcement of shared rules can justify giving government substantial powers over individual behaviour.",
    },
    "Society": {
        "x_neg": "You favour a more socially liberal outlook. Your answers suggest that people should be able to form relationships, families and identities in different ways, with personal choice taking priority over inherited social expectations.",
        "x_pos": "You favour a more socially traditional outlook. Your answers suggest that established family structures, conventional moral expectations and continuity with familiar social norms deserve greater weight when society decides what it should encourage.",
        "y_neg": "You place a strong value on personal freedom in social life. Your answers suggest that peaceful adults should generally be able to make their own choices without the state or wider society imposing unnecessary moral restrictions.",
        "y_pos": "You are more comfortable with social authority and shared standards. Your answers suggest that maintaining order and common moral expectations can justify placing limits on individual behaviour when you believe those limits protect society.",
    },
    "Culture": {
        "x_neg": "You favour a more internationalist and multicultural outlook. Your answers suggest that cultural diversity, immigration, distinct identities and cooperation between countries are generally positive developments rather than threats to a fixed national culture.",
        "x_pos": "You place greater emphasis on national identity and cultural continuity. Your answers suggest that a shared national culture, integration, established traditions and the preservation of a country's distinctive character are important social goods.",
        "y_neg": "You favour cultural freedom and gradual organic change. You are less comfortable with governments deciding what a country's culture should look like, and you place more weight on people and communities shaping culture for themselves.",
        "y_pos": "You are more comfortable with cultural authority and preservation. Your answers suggest that collective or governmental action can be justified to protect established traditions, national identity and social continuity when they are under pressure from rapid change.",
    },
}

SECTION_MIDDLE = {
    "Economy": "Your economic answers are fairly mixed. You do not show a strong preference for either a collective, state-directed economy or a predominantly private, market-led one.",
    "Government": "Your answers are fairly mixed on the authority dimension. You do not show a strong overall preference for either giving the state substantially more power or placing firm limits on it.",
    "Society": "Your social answers are fairly mixed. You do not consistently favour either traditional social expectations or a more socially liberal approach.",
    "Culture": "Your cultural answers are fairly mixed. You do not show a strong overall preference between preserving established national traditions and embracing cultural change and diversity.",
}


def _draw_quadrant(screen, rect, colour, alpha=92):
    # Solid fills are much more reliable in Pygbag/WebAssembly.
    pygame.draw.rect(screen, colour, rect)


def _draw_compass(
    screen,
    rect,
    x,
    y,
    mx,
    my,
    *,
    small=False,
    axis_y_labels=("AUTHORITY", "LIBERTY"),
):
    """Draw the political compass in a web-safe way."""

    left, top, width, height = rect

    cx = left + width // 2
    cy = top + height // 2

    half_w = width // 2
    half_h = height // 2

    # Four quadrants.
    # Use solid colours rather than transparent Surfaces because this
    # renders much more reliably through Pygbag/WebAssembly.
    pygame.draw.rect(
        screen,
        QUADRANT_COLOURS["tl"],
        (left, top, half_w, half_h),
    )

    pygame.draw.rect(
        screen,
        QUADRANT_COLOURS["tr"],
        (cx, top, width - half_w, half_h),
    )

    pygame.draw.rect(
        screen,
        QUADRANT_COLOURS["bl"],
        (left, cy, half_w, height - half_h),
    )

    pygame.draw.rect(
        screen,
        QUADRANT_COLOURS["br"],
        (cx, cy, width - half_w, height - half_h),
    )

    # Border and axes.
    line_width = 1 if small else 2

    pygame.draw.rect(
        screen,
        INK,
        (left, top, width, height),
        line_width,
    )

    pygame.draw.line(
        screen,
        INK,
        (cx, top),
        (cx, top + height),
        line_width,
    )

    pygame.draw.line(
        screen,
        INK,
        (left, cy),
        (left + width, cy),
        line_width,
    )

    # Labels.
    label_size = 7 if small else 10
    axis_font = font("Arial", label_size, True)

    left_label = axis_font.render("LEFT", True, INK_LIGHT)
    right_label = axis_font.render("RIGHT", True, INK_LIGHT)

    screen.blit(
        left_label,
        (left + 6, cy - left_label.get_height() - 4),
    )

    screen.blit(
        right_label,
        (
            left + width - right_label.get_width() - 6,
            cy - right_label.get_height() - 4,
        ),
    )

    top_label = axis_font.render(axis_y_labels[0], True, INK_LIGHT)
    bottom_label = axis_font.render(axis_y_labels[1], True, INK_LIGHT)

    gap = 6 if small else 10

    screen.blit(
        top_label,
        (
            cx - top_label.get_width() - gap,
            top + 5,
        ),
    )

    screen.blit(
        bottom_label,
        (
            cx - bottom_label.get_width() - gap,
            top + height - bottom_label.get_height() - 5,
        ),
    )

    # Position of the player.
    norm_x = max(-1.0, min(1.0, x / (mx or 1)))
    norm_y = max(-1.0, min(1.0, y / (my or 1)))

    margin = 8 if small else 18

    px = int(
        cx + norm_x * (half_w - margin)
    )

    py = int(
        cy - norm_y * (half_h - margin)
    )

    # Player marker.
    radius = 5 if small else 10

    pygame.draw.circle(
        screen,
        PAPER,
        (px, py),
        radius + 3,
    )

    pygame.draw.circle(
        screen,
        RED,
        (px, py),
        radius,
    )

    pygame.draw.circle(
        screen,
        INK,
        (px, py),
        radius,
        1,
    )

    return px, py


def _draw_header(screen, title):
    rendered = font("Georgia", 51, True).render(title, True, INK)
    screen.blit(rendered, (PAGE_MARGIN, 28))
    draw_rule(screen, 109, PAGE_MARGIN, screen.get_width() - PAGE_MARGIN, 3)


def _section_limits():
    return {
        name: (
            max(1.0, sum(abs(q["x"]) for q in qs)),
            max(1.0, sum(abs(q["y"]) for q in qs)),
        )
        for name, qs in SECTIONS
    }


def _strength(value, limit):
    ratio = abs(value) / max(limit, 1.0)
    if ratio >= 0.70:
        return "strongly"
    if ratio >= 0.38:
        return "clearly"
    if ratio >= 0.15:
        return "slightly"
    return "very close to the middle"


def _section_score_text(name, sx, sy):
    """Small text helper retained for regression tests and lightweight callers."""
    if sx < -0.12:
        x_word = "left"
    elif sx > 0.12:
        x_word = "right"
    else:
        x_word = "middle"
    if sy < -0.12:
        y_word = "liberty"
    elif sy > 0.12:
        y_word = "authority"
    else:
        y_word = "middle"
    return f"{name}: {x_word}, {y_word}"


def _axis_interpretation(name, sx, sy, max_x, max_y):
    texts = SECTION_AXIS_TEXT[name]
    nx = sx / max_x if max_x else 0
    ny = sy / max_y if max_y else 0

    if abs(nx) < 0.12:
        x_read = f"Your horizontal score is {sx:+.2f}, placing you very close to the middle. {SECTION_MIDDLE[name]}"
    else:
        side = "left" if nx < 0 else "right"
        x_read = f"Your horizontal score is {sx:+.2f}. You lean {_strength(sx, max_x)} to the {side}. {texts['x_neg'] if nx < 0 else texts['x_pos']}"

    if name == "Economy":
        if abs(ny) < 0.12:
            y_read = (
                f"Your economic-intervention score is {sy:+.2f}, placing you very close to the middle of this measure. "
                "This vertical position is not an authoritarian/libertarian score: the Economy section does not test personal liberty or state authority. "
                "It instead reflects how willing you are to accept government direction of economic activity."
            )
        else:
            side = "less government intervention" if ny < 0 else "more government intervention"
            y_read = (
                f"Your economic-intervention score is {sy:+.2f}. You lean {_strength(sy, max_y)} towards {side}. "
                f"{texts['y_neg'] if ny < 0 else texts['y_pos']}"
            )
    elif abs(ny) < 0.12:
        y_read = (
            f"Your vertical score is {sy:+.2f}, placing you very close to the middle of the liberty/authority dimension. "
            "Your answers do not show a strong preference between greater individual freedom and greater state authority."
        )
    else:
        side = "towards liberty" if ny < 0 else "towards authority"
        y_read = f"Your vertical score is {sy:+.2f}. You lean {_strength(sy, max_y)} {side}. {texts['y_neg'] if ny < 0 else texts['y_pos']}"

    return x_read, y_read


def _overall_bucket(x, y, mx, my):
    nx = x / mx if mx else 0
    ny = y / my if my else 0
    def axis(v):
        if v <= -0.12:
            return "left"
        if v >= 0.12:
            return "right"
        return "middle"
    return axis(nx), "authority" if ny >= 0.12 else "liberty" if ny <= -0.12 else "middle"


def _draw_main_result(screen, x, y, mx, my):
    """Main result: use the page as an editorial result sheet rather than leaving dead space."""
    screen.fill(PAPER)
    w, h = screen.get_size()
    _draw_header(screen, "YOUR POLITICAL POSITION")

    bucket = _overall_bucket(x, y, mx, my)
    summary = OVERALL_TEXT[bucket]
    paragraphs = summary.split("\n\n")

    # Two-column opening: the writing gets enough width to breathe; the compass is compact.
    left_x = PAGE_MARGIN
    left_w = 525
    graph_w, graph_h = 410, 290
    graph_x = w - PAGE_MARGIN - graph_w
    graph_y = 146

    kicker = font("Arial", 15, True).render("YOUR RESULT", True, RED)
    screen.blit(kicker, (left_x, 140))

    body_font = font("Georgia", 20)
    yy = 173
    for paragraph in paragraphs:
        for line in wrap_text(paragraph, body_font, left_w):
            screen.blit(body_font.render(line, True, INK), (left_x, yy))
            yy += 27
        yy += 12

    _draw_compass(screen, (graph_x, graph_y, graph_w, graph_h), x, y, mx, my)

    # A compact numerical footer under the interpretation makes the result feel complete.
    score_font = font("Arial", 13, True)
    score_text = score_font.render(f"EXACT SCORES   X {x:+.2f}     Y {y:+.2f}", True, INK_LIGHT)
    screen.blit(score_text, (graph_x, graph_y + graph_h + 16))

    # Buttons sit immediately below the content rather than at the bottom of a large empty page.
    button_y = h - 72
    gap = 18
    button_w = 310
    total_w = button_w * 2 + gap
    first_x = (w - total_w) // 2
    analyse_rect = pygame.Rect(first_x, button_y, button_w, 54)
    again_rect = pygame.Rect(first_x + button_w + gap, button_y, button_w, 54)
    mouse_pos = pygame.mouse.get_pos()
    draw_button(screen, analyse_rect, "ANALYSE RESULTS", mouse_pos, font_obj=font("Arial", 17, True))
    draw_button(screen, again_rect, "TAKE THE TEST AGAIN", mouse_pos, font_obj=font("Arial", 17, True))
    return analyse_rect, again_rect


def _section_card_blurb(name, sx, sy, max_x, max_y):
    nx = sx / max_x if max_x else 0.0
    ny = sy / max_y if max_y else 0.0
    if abs(nx) < 0.12:
        horizontal = "CLOSE TO THE CENTRE"
    else:
        horizontal = "LEANING LEFT" if nx < 0 else "LEANING RIGHT"
    if name == "Economy":
        if abs(ny) < 0.12:
            vertical = "ECONOMIC INTERVENTION: CENTRE"
        else:
            vertical = "LESS STATE INTERVENTION" if ny < 0 else "MORE STATE INTERVENTION"
    else:
        if abs(ny) < 0.12:
            vertical = "CLOSE TO THE CENTRE"
        else:
            vertical = "LEANING TOWARDS LIBERTY" if ny < 0 else "LEANING TOWARDS AUTHORITY"
    return f"{horizontal}  •  {vertical}"


def _draw_section_card(screen, rect, name, sx, sy, max_x, max_y):
    """Clickable card with a proper hover expansion/highlight and right-aligned action."""
    rect = pygame.Rect(rect)
    hovered = rect.collidepoint(pygame.mouse.get_pos())
    draw_rect = rect.inflate(8, 8) if hovered else rect

    fill = (238, 232, 216) if hovered else PAPER_DARK
    pygame.draw.rect(screen, fill, draw_rect)
    pygame.draw.rect(screen, RED if hovered else INK_LIGHT, draw_rect, 2 if hovered else 1)

    x0, y0, w, h = draw_rect
    title = font("Arial", 17, True).render(name.upper(), True, RED)
    screen.blit(title, (x0 + 18, y0 + 13))

    compass_rect = (x0 + 18, y0 + 43, 235, 116)
    axis_labels = ("MORE STATE", "LESS STATE") if name == "Economy" else ("AUTHORITY", "LIBERTY")
    _draw_compass(screen, compass_rect, sx, sy, max_x, max_y, small=True, axis_y_labels=axis_labels)

    info_x = x0 + 272
    info_w = w - 292
    label = font("Arial", 11, True).render("YOUR POSITION", True, RED if hovered else INK_LIGHT)
    screen.blit(label, (info_x, y0 + 45))

    info_font = font("Georgia", 15)
    yy = y0 + 68
    for line in wrap_text(_section_card_blurb(name, sx, sy, max_x, max_y), info_font, info_w):
        screen.blit(info_font.render(line, True, INK), (info_x, yy))
        yy += 20

    hint = font("Arial", 11, True).render("CLICK TO ANALYSE THIS SECTION  →", True, RED if hovered else INK_LIGHT)
    screen.blit(hint, (x0 + w - hint.get_width() - 18, y0 + h - hint.get_height() - 15))
    return rect


def _draw_analysis_overview(screen, x, y, mx, my, section_scores):
    screen.fill(PAPER)
    w, h = screen.get_size()
    limits = _section_limits()
    score_map = {name: (sx, sy) for name, sx, sy in section_scores}
    _draw_header(screen, "ANALYSIS OF YOUR RESULTS")

    heading = font("Arial", 15, True).render("YOUR OVERALL POSITION", True, RED)
    screen.blit(heading, (PAGE_MARGIN, 140))

    intro_font = font("Georgia", 20)
    intro = "This page gives the detail behind your result. Select a section to see what your answers there suggest about you."
    intro_w = w - PAGE_MARGIN * 2 - 285
    yy = 172
    for line in wrap_text(intro, intro_font, intro_w):
        screen.blit(intro_font.render(line, True, INK), (PAGE_MARGIN, yy))
        yy += 27

    score_font = font("Arial", 13, True)
    screen.blit(score_font.render(f"EXACT SCORES   X {x:+.2f}     Y {y:+.2f}", True, INK_LIGHT), (PAGE_MARGIN, yy + 8))

    mini_w, mini_h = 245, 150
    mini = (w - PAGE_MARGIN - mini_w, 137, mini_w, mini_h)
    _draw_compass(screen, mini, x, y, mx, my, small=True)

    # Cards use almost the full remaining page, with the action anchored to the right.
    card_gap = 16
    card_w = (w - 2 * PAGE_MARGIN - card_gap) // 2
    card_h = 188
    card_y = 292
    positions = [
        (PAGE_MARGIN, card_y),
        (PAGE_MARGIN + card_w + card_gap, card_y),
        (PAGE_MARGIN, card_y + card_h + card_gap),
        (PAGE_MARGIN + card_w + card_gap, card_y + card_h + card_gap),
    ]

    card_rects = {}
    for name, (tx, ty) in zip(("Economy", "Government", "Society", "Culture"), positions):
        sx, sy = score_map.get(name, (0.0, 0.0))
        lim_x, lim_y = limits.get(name, (1.0, 1.0))
        card_rects[name] = _draw_section_card(
            screen, pygame.Rect(tx, ty, card_w, card_h), name, sx, sy, lim_x, lim_y
        )

    back_rect = pygame.Rect(PAGE_MARGIN, h - 53, 190, 42)
    draw_button(screen, back_rect, "← BACK", pygame.mouse.get_pos(), font_obj=font("Arial", 14, True))
    return back_rect, card_rects


def _draw_contribution_bar(screen, x, y, width, value, limit, label, left_label, right_label):
    label_font = font("Arial", 12, True)
    screen.blit(label_font.render(label, True, INK_LIGHT), (x, y))
    bar_y = y + 22
    pygame.draw.rect(screen, INK_LIGHT, (x, bar_y, width, 10), 1)
    centre = x + width // 2
    pygame.draw.line(screen, INK_LIGHT, (centre, bar_y), (centre, bar_y + 10), 1)
    ratio = max(-1.0, min(1.0, value / max(limit, 1.0)))
    px = centre + int(ratio * (width // 2 - 5))
    pygame.draw.circle(screen, RED, (px, bar_y + 5), 6)

    endpoint_font = font("Arial", 10, True)
    left = endpoint_font.render(left_label, True, INK_LIGHT)
    right = endpoint_font.render(right_label, True, INK_LIGHT)
    screen.blit(left, (x, bar_y + 14))
    screen.blit(right, (x + width - right.get_width(), bar_y + 14))


def _draw_section_detail(screen, name, sx, sy, max_x, max_y):
    screen.fill(PAPER)
    w, h = screen.get_size()
    _draw_header(screen, f"{name.upper()} — YOUR RESULTS")

    score_font = font("Arial", 13, True)
    screen.blit(score_font.render(f"EXACT SECTION SCORES   X {sx:+.2f}     Y {sy:+.2f}", True, INK_LIGHT), (PAGE_MARGIN, 134))

    compass_rect = (PAGE_MARGIN, 177, 400, 280)
    axis_labels = ("MORE STATE", "LESS STATE") if name == "Economy" else ("AUTHORITY", "LIBERTY")
    _draw_compass(screen, compass_rect, sx, sy, max_x, max_y, axis_y_labels=axis_labels)

    text_x = 505
    text_w = w - text_x - PAGE_MARGIN
    screen.blit(font("Arial", 15, True).render("YOUR POSITION ON THIS SECTION", True, RED), (text_x, 181))

    if name == "Economy":
        _draw_contribution_bar(screen, text_x, 218, text_w, sx, max_x, "HORIZONTAL — LEFT ↔ RIGHT", "LEFT", "RIGHT")
        _draw_contribution_bar(screen, text_x, 287, text_w, sy, max_y, "ECONOMIC INTERVENTION", "LESS STATE", "MORE STATE")
    else:
        _draw_contribution_bar(screen, text_x, 218, text_w, sx, max_x, "HORIZONTAL — LEFT ↔ RIGHT", "LEFT", "RIGHT")
        _draw_contribution_bar(screen, text_x, 287, text_w, sy, max_y, "VERTICAL — LIBERTY ↔ AUTHORITY", "LIBERTY", "AUTHORITY")

    x_read, y_read = _axis_interpretation(name, sx, sy, max_x, max_y)
    text_y = 365
    screen.blit(font("Arial", 15, True).render("WHAT YOUR ANSWERS SUGGEST ABOUT YOU", True, RED), (text_x, text_y))
    body_font = font("Georgia", 17)
    text_y += 32
    for paragraph in (x_read, y_read):
        for line in wrap_text(paragraph, body_font, text_w):
            screen.blit(body_font.render(line, True, INK), (text_x, text_y))
            text_y += 23
        text_y += 8

    back_rect = pygame.Rect(PAGE_MARGIN, h - 53, 190, 42)
    names = [name for name, _ in SECTIONS]
    idx = names.index(name)
    next_name = names[(idx + 1) % len(names)]
    next_rect = pygame.Rect(w - PAGE_MARGIN - 230, h - 53, 230, 42)
    draw_button(screen, back_rect, "← OVERVIEW", pygame.mouse.get_pos(), font_obj=font("Arial", 14, True))
    draw_button(screen, next_rect, f"NEXT: {next_name.upper()} →", pygame.mouse.get_pos(), font_obj=font("Arial", 14, True))
    return back_rect, next_rect


async def run(screen, x, y, mx, my, section_scores=None):
    clock = pygame.time.Clock()
    if section_scores is None:
        section_scores = []

    score_map = {name: (sx, sy) for name, sx, sy in section_scores}
    limits = _section_limits()
    state = "result"
    selected_section = None

    while True:
        if state == "result":
            analyse_rect, again_rect = _draw_main_result(screen, x, y, mx, my)
        elif state == "overview":
            back_rect, card_rects = _draw_analysis_overview(screen, x, y, mx, my, section_scores)
        else:
            sx, sy = score_map.get(selected_section, (0.0, 0.0))
            lim_x, lim_y = limits.get(selected_section, (1.0, 1.0))
            back_rect, next_rect = _draw_section_detail(screen, selected_section, sx, sy, lim_x, lim_y)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if state == "detail":
                        state = "overview"
                    elif state == "overview":
                        state = "result"
                    else:
                        return "quit"
                    continue

                if state == "result" and event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    play_random_sound()
                    return "again"

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if state == "result":
                    if analyse_rect.collidepoint(event.pos):
                        play_random_sound()
                        state = "overview"
                    elif again_rect.collidepoint(event.pos):
                        play_random_sound()
                        return "again"

                elif state == "overview":
                    if back_rect.collidepoint(event.pos):
                        play_random_sound()
                        state = "result"
                    else:
                        for name, rect in card_rects.items():
                            if rect.collidepoint(event.pos):
                                play_random_sound()
                                selected_section = name
                                state = "detail"
                                break

                else:
                    if back_rect.collidepoint(event.pos):
                        play_random_sound()
                        state = "overview"
                    elif next_rect.collidepoint(event.pos):
                        play_random_sound()
                        selected_section = [name for name, _ in SECTIONS][
                            ([name for name, _ in SECTIONS].index(selected_section) + 1) % len(SECTIONS)
                        ]

        pygame.display.flip()
        await asyncio.sleep(1 / 60)
