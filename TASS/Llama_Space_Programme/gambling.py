
import asyncio
import random
import pygame
import os
import math
import global_variables

# Find the folder containing this game and its image/audio files.
game_folder = os.path.dirname(os.path.abspath(__file__))

# Use the display created once by main.py. This module must be imported
# after that display exists.
screen = pygame.display.get_surface()
if screen is None:
    raise RuntimeError("Import gambling.py after main.py creates the Pygame display.")

WIDTH, HEIGHT = screen.get_size()

# Scale everything relative to the original 800 x 600 design
SCALE = min(WIDTH / 800, HEIGHT / 600)
OFFSET_X = (WIDTH - 800 * SCALE) / 2
OFFSET_Y = (HEIGHT - 600 * SCALE) / 2

def scale_pos(x, y):
    return (
        int(OFFSET_X + x * SCALE),
        int(OFFSET_Y + y * SCALE)
    )

def scale_rect(rect):
    return pygame.Rect(
        *scale_pos(rect.x, rect.y),
        int(rect.width * SCALE),
        int(rect.height * SCALE)
    )

font = pygame.font.SysFont("Arial", max(1, int(28 * SCALE)), bold=True)
title_font = pygame.font.SysFont("Georgia", max(1, int(35 * SCALE)), bold=True)
small_font = pygame.font.SysFont("Arial", max(1, int(16 * SCALE)), bold=True)
tiny_font = pygame.font.SysFont("Arial", max(1, int(12 * SCALE)), bold=True)

casino_music_path = os.path.join(game_folder, "Casino Music.ogg")

clock = pygame.time.Clock()

# Draw the game on a virtual 800 x 600 surface
game_surface = pygame.Surface((800, 600))

# Reuse the shimmer overlay instead of allocating a new surface every frame.
shimmer_surface = pygame.Surface((800, 600), pygame.SRCALPHA)

# --------------------------------------------------
# COLOURS
# --------------------------------------------------

GOLD = (222, 174, 70)
LIGHT_GOLD = (255, 232, 174)
DARK_GOLD = (119, 76, 25)
CHAMPAGNE_GOLD = (255, 244, 207)

EMERALD = (15, 75, 57)
DARK_EMERALD = (5, 35, 28)
LIGHT_EMERALD = (31, 112, 81)

BURGUNDY = (105, 28, 39)
DARK_BURGUNDY = (55, 13, 23)
LIGHT_BURGUNDY = (155, 43, 56)

CREAM = (255, 246, 224)
WHITE = (255, 255, 255)

# --------------------------------------------------
# BACKGROUND
# --------------------------------------------------

background_image_path = os.path.join(game_folder, "Background_image.png")
image = pygame.image.load(background_image_path).convert()

# --------------------------------------------------
# FULLSCREEN BACKGROUND
# --------------------------------------------------

# Make a separate background that fills the entire monitor.
# The image is enlarged proportionally until it covers the screen,
# then the excess is cropped from the centre. This avoids stretching
# or squashing the casino artwork.

original_image_width = image.get_width()
original_image_height = image.get_height()

fullscreen_scale_width = WIDTH / original_image_width
fullscreen_scale_height = HEIGHT / original_image_height

fullscreen_scale = max(
    fullscreen_scale_width,
    fullscreen_scale_height
)

fullscreen_background_width = int(original_image_width * fullscreen_scale)
fullscreen_background_height = int(original_image_height * fullscreen_scale)

fullscreen_background_image = pygame.transform.smoothscale(
    image,
    (fullscreen_background_width, fullscreen_background_height)
)

fullscreen_background = pygame.Surface((WIDTH, HEIGHT))

fullscreen_background_x = (
    WIDTH - fullscreen_background_width
) // 2

fullscreen_background_y = (
    HEIGHT - fullscreen_background_height
) // 2

fullscreen_background.blit(
    fullscreen_background_image,
    (fullscreen_background_x, fullscreen_background_y)
)

# Keep the actual blackjack table at its original 4:3 proportions.
# This prevents cards, chips, buttons and text from being distorted.

background_scale_width = 800 / original_image_width
background_scale_height = 600 / original_image_height

background_scale = max(
    background_scale_width,
    background_scale_height
)

background_width = int(original_image_width * background_scale)
background_height = int(original_image_height * background_scale)

image = pygame.transform.smoothscale(
    image,
    (background_width, background_height)
)

background_surface = pygame.Surface((800, 600))

background_x = (800 - background_width) // 2
background_y = (600 - background_height) // 2

background_surface.blit(
    image,
    (background_x, background_y)
)

# --------------------------------------------------
# BUTTONS
# --------------------------------------------------

buttons = {
    "YES": pygame.Rect(100, 100, 200, 60),
    "No": pygame.Rect(500, 100, 200, 60),
}

input_box = pygame.Rect(200, 250, 400, 60)

# --------------------------------------------------
# CARD DATA
# --------------------------------------------------

suits = ["Hearts", "Diamonds", "Clubs", "Spades"]

ranks = [
    "Ace", "2", "3", "4", "5", "6", "7",
    "8", "9", "10", "Jack", "Queen", "King"
]

rank_values = {
    "Ace": 11,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "Jack": 10,
    "Queen": 10,
    "King": 10
}

# --------------------------------------------------
# GAME VARIABLES
# --------------------------------------------------

user_text = ""

prompt_text = "Do you want to Gamble?"
game_state = "question"

start_time = 0

# Use the same money balance as the rest of the game.
# Phase 1 stores the player's balance in global_variables.money.
moneytotal = global_variables.money
money = 0

running = True

deck = []
hand = []
hand_value = 0

dealer_hand = []
dealer_hand_value = 0

money_updated = False
round_result = None

# --------------------------------------------------
# TEXT WRAPPING
# --------------------------------------------------

def wrap_text(text, selected_font, max_width):

    words = text.split(" ")
    lines = []
    current_line = ""

    for word in words:

        test_line = (
            current_line + " " + word
            if current_line else word
        )

        if selected_font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)

            current_line = word

    if current_line:
        lines.append(current_line)

    return lines


# --------------------------------------------------
# VISUAL FUNCTIONS
# --------------------------------------------------

def draw_gold_outline(surface, rect, radius=13, highlighted=False):

    # Every layer is drawn INSIDE the supplied rectangle. This means the
    # coloured button fill can never extend beyond its golden frame.
    pygame.draw.rect(
        surface,
        (73, 43, 15),
        rect,
        width=6,
        border_radius=radius
    )

    dark_inner_rect = rect.inflate(-2, -2)
    pygame.draw.rect(
        surface,
        DARK_GOLD,
        dark_inner_rect,
        width=4,
        border_radius=max(2, radius - 2)
    )

    main_gold_rect = rect.inflate(-4, -4)
    pygame.draw.rect(
        surface,
        GOLD,
        main_gold_rect,
        width=3,
        border_radius=max(2, radius - 4)
    )

    highlight_rect = rect.inflate(-7, -7)
    highlight_colour = LIGHT_GOLD if highlighted else CHAMPAGNE_GOLD

    pygame.draw.rect(
        surface,
        highlight_colour,
        highlight_rect,
        width=1,
        border_radius=max(2, radius - 7)
    )

    if highlighted:

        inner_glow_rect = rect.inflate(-10, -10)

        pygame.draw.rect(
            surface,
            (255, 240, 190),
            inner_glow_rect,
            width=1,
            border_radius=max(2, radius - 9)
        )


def draw_panel(surface, rect, opacity=205):

    panel = pygame.Surface(
        (rect.width, rect.height),
        pygame.SRCALPHA
    )

    pygame.draw.rect(
        panel,
        (3, 22, 17, opacity),
        panel.get_rect(),
        border_radius=17
    )

    draw_gold_outline(
        panel,
        panel.get_rect(),
        radius=17,
        highlighted=False
    )

    surface.blit(panel, rect.topleft)


def draw_chip(surface, x, y, radius):

    pygame.draw.circle(
        surface, DARK_GOLD, (x, y), radius + 3
    )

    pygame.draw.circle(
        surface, BURGUNDY, (x, y), radius
    )

    pygame.draw.circle(
        surface, GOLD, (x, y), radius - 5, 3
    )

    pygame.draw.circle(
        surface, DARK_BURGUNDY, (x, y), radius - 10
    )

    pygame.draw.circle(
        surface, GOLD, (x, y), radius - 13, 2
    )

    for i in range(8):

        angle = math.radians(i * 45)

        start_x = x + math.cos(angle) * (radius - 3)
        start_y = y + math.sin(angle) * (radius - 3)

        end_x = x + math.cos(angle) * (radius - 9)
        end_y = y + math.sin(angle) * (radius - 9)

        pygame.draw.line(
            surface,
            LIGHT_GOLD,
            (start_x, start_y),
            (end_x, end_y),
            3
        )


def draw_header_shimmer(surface):

    # The shimmer travels along the two gold lines above the table.
    # It changes rail halfway through each cycle, so it never disappears
    # beyond the edge of the screen.
    cycle_length = 4200
    animation_time = pygame.time.get_ticks() % cycle_length
    animation_progress = animation_time / cycle_length

    if animation_progress < 0.5:
        rail_start = 35
        rail_end = 300
        rail_progress = animation_progress * 2
    else:
        rail_start = 500
        rail_end = 765
        rail_progress = (animation_progress - 0.5) * 2

    shimmer_x = int(
        rail_start + 12 + rail_progress * (rail_end - rail_start - 24)
    )

    shimmer_surface.fill((0, 0, 0, 0))

    # A short trail of fine vertical glints gives the moving shine some depth.
    for offset in range(-22, 23, 2):

        glint_x = shimmer_x + offset

        if rail_start <= glint_x <= rail_end:

            strength = 1 - abs(offset) / 24
            alpha = int(185 * strength)
            line_width = max(1, int(3 * strength))

            pygame.draw.line(
                shimmer_surface,
                (255, 241, 194, alpha),
                (glint_x, 29),
                (glint_x, 35),
                line_width
            )

    # A small diamond at the centre makes the shimmer read as a glint.
    pygame.draw.polygon(
        shimmer_surface,
        (255, 250, 220, 245),
        [
            (shimmer_x, 26),
            (shimmer_x + 4, 32),
            (shimmer_x, 38),
            (shimmer_x - 4, 32)
        ]
    )

    surface.blit(shimmer_surface, (0, 0))


def draw_casino_background(surface):

    # Decorative gold rails either side of the title.
    pygame.draw.line(
        surface, DARK_GOLD, (35, 32), (300, 32), 3
    )

    pygame.draw.line(
        surface, DARK_GOLD, (500, 32), (765, 32), 3
    )

    pygame.draw.line(
        surface, GOLD, (35, 30), (300, 30), 1
    )

    pygame.draw.line(
        surface, GOLD, (500, 30), (765, 30), 1
    )

    title = title_font.render(
        "BLACKJACK",
        True,
        LIGHT_GOLD
    )

    surface.blit(
        title,
        title.get_rect(center=(400, 30))
    )

    draw_header_shimmer(surface)

    draw_chip(surface, 48, 525, 29)
    draw_chip(surface, 752, 525, 29)

    diamond_positions = [
        (35, 50),
        (765, 50),
        (35, 565),
        (765, 565)
    ]

    for x, y in diamond_positions:

        pygame.draw.polygon(
            surface,
            GOLD,
            [
                (x, y - 5),
                (x + 5, y),
                (x, y + 5),
                (x - 5, y)
            ]
        )


def draw_fancy_button(surface, name, rect, hovered, selected=False):

    if name == "YES":
        top_colour = LIGHT_EMERALD
        bottom_colour = DARK_EMERALD
    else:
        top_colour = LIGHT_BURGUNDY
        bottom_colour = DARK_BURGUNDY

    # The selected option receives a much clearer golden highlight.
    if selected:
        top_colour = tuple(
            min(255, value + 48)
            for value in top_colour
        )

        bottom_colour = tuple(
            min(255, value + 32)
            for value in bottom_colour
        )

    elif hovered:
        top_colour = tuple(
            min(255, value + 35)
            for value in top_colour
        )

        bottom_colour = tuple(
            min(255, value + 25)
            for value in bottom_colour
        )

    # Keep the gradient comfortably inside the gold outline.
    inner_rect = rect.inflate(-12, -12)

    button_surface = pygame.Surface(
        (inner_rect.width, inner_rect.height),
        pygame.SRCALPHA
    )

    for y in range(inner_rect.height):

        ratio = y / max(1, inner_rect.height - 1)

        colour = tuple(
            int(
                top_colour[i] * (1 - ratio)
                + bottom_colour[i] * ratio
            )
            for i in range(3)
        )

        pygame.draw.line(
            button_surface,
            colour,
            (0, y),
            (inner_rect.width - 1, y)
        )

    # Give the inner gradient rounded corners rather than square corners
    # poking out from behind the curved gold frame.
    rounded_mask = pygame.Surface(
        (inner_rect.width, inner_rect.height),
        pygame.SRCALPHA
    )

    pygame.draw.rect(
        rounded_mask,
        (255, 255, 255, 255),
        rounded_mask.get_rect(),
        border_radius=8
    )

    button_surface.blit(
        rounded_mask,
        (0, 0),
        special_flags=pygame.BLEND_RGBA_MULT
    )

    if selected or hovered:

        inner_highlight = pygame.Surface(
            (inner_rect.width, inner_rect.height),
            pygame.SRCALPHA
        )

        pygame.draw.rect(
            inner_highlight,
            (255, 222, 135, 34 if selected else 20),
            inner_highlight.get_rect(),
            border_radius=8
        )

        button_surface.blit(inner_highlight, (0, 0))

    surface.blit(button_surface, inner_rect.topleft)

    # The outline is the outermost visible edge of the button.
    # No shadow or fill extends beyond this rectangle.
    draw_gold_outline(
        surface,
        rect,
        radius=14,
        highlighted=(selected or hovered)
    )

    # Fine top bevel, also kept inside the frame.
    pygame.draw.line(
        surface,
        CHAMPAGNE_GOLD,
        (rect.x + 24, rect.y + 8),
        (rect.right - 24, rect.y + 8),
        1
    )

    text = font.render(name, True, CREAM)
    text_shadow = font.render(name, True, (0, 0, 0))

    # Centre the foreground lettering on both axes of the button.
    surface.blit(
        text_shadow,
        text_shadow.get_rect(
            center=(rect.centerx + 1, rect.centery + 2)
        )
    )

    surface.blit(
        text,
        text.get_rect(center=rect.center)
    )


def draw_fancy_text(surface, text, position, selected_font, colour):

    shadow = selected_font.render(text, True, (0, 0, 0))
    foreground = selected_font.render(text, True, colour)

    surface.blit(
        shadow,
        shadow.get_rect(
            center=(position[0] + 1, position[1] + 1)
        )
    )

    surface.blit(
        foreground,
        foreground.get_rect(center=position)
    )


# --------------------------------------------------
# PROMPT PANEL
# --------------------------------------------------

def draw_prompt_panel(surface, lines):

    line_height = 34
    max_lines = 4

    if len(lines) > max_lines:
        lines = lines[-max_lines:]

    panel_height = max(
        65,
        len(lines) * line_height + 24
    )

    # Keep the prompt above the footer, even when four lines are displayed.
    panel_bottom = 545
    panel_y = min(460, panel_bottom - panel_height)

    prompt_panel = pygame.Rect(
        75, panel_y, 650, panel_height
    )

    draw_panel(surface, prompt_panel, 210)

    if lines:

        # Centre the complete block of lines vertically inside the panel.
        first_line_centre = (
            prompt_panel.centery
            - ((len(lines) - 1) * line_height) / 2
        )

        for i, line in enumerate(lines):

            draw_fancy_text(
                surface,
                line,
                (
                    prompt_panel.centerx,
                    int(first_line_centre + i * line_height)
                ),
                font,
                CREAM
            )

    return prompt_panel


# --------------------------------------------------
# DEALER SECTION
# --------------------------------------------------

def draw_dealer_section(surface):

    if len(dealer_hand) == 0:
        return

    dealer_panel = pygame.Rect(
        150, 245, 500, 125
    )

    draw_panel(surface, dealer_panel, 210)

    heading = small_font.render(
        "THE DEALER",
        True,
        LIGHT_GOLD
    )

    cards_text = ", ".join(dealer_hand)

    card_lines = wrap_text(
        cards_text,
        font,
        450
    )[:2]

    value_surface = small_font.render(
        "HAND VALUE: " + str(dealer_hand_value),
        True,
        GOLD
    )

    # Use fixed, evenly spaced centre points for the dealer information.
    # Every rendered item is centred on its own point.
    content_items = [heading]

    for line in card_lines:
        content_items.append(font.render(line, True, CREAM))

    content_items.append(value_surface)

    item_spacing = 28
    total_height = (len(content_items) - 1) * item_spacing
    first_item_centre = dealer_panel.centery - total_height / 2

    for i, item_surface in enumerate(content_items):

        item_rectangle = item_surface.get_rect(
            center=(
                dealer_panel.centerx,
                int(first_item_centre + i * item_spacing)
            )
        )

        surface.blit(item_surface, item_rectangle)


# --------------------------------------------------
# INPUT BOX
# --------------------------------------------------

def draw_fancy_input_box(surface):

    pygame.draw.rect(
        surface,
        (4, 27, 20),
        input_box,
        border_radius=12
    )

    inner_input_box = input_box.inflate(-8, -8)

    pygame.draw.rect(
        surface,
        (7, 39, 28),
        inner_input_box,
        border_radius=8
    )

    draw_gold_outline(
        surface,
        input_box,
        radius=12,
        highlighted=True
    )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

def draw_footer(surface):

    footer_text = ""

    if game_state == "question":
        footer_text = "CHOOSE YOUR FATE"

    elif game_state == "welcome":
        footer_text = "WELCOME TO THE TABLE"

    elif game_state == "welcome2":
        footer_text = "PLACE YOUR BET"

    elif game_state == "betting":
        footer_text = "ENTER TO PLACE BET  |  BACKSPACE TO EDIT"

    elif game_state == "playing":
        footer_text = "H - HIT       S - STAND"

    elif game_state == "dealer":
        footer_text = "THE HOUSE IS PLAYING..."

    if footer_text:

        footer = small_font.render(
            footer_text,
            True,
            GOLD
        )

        surface.blit(
            footer,
            footer.get_rect(center=(400, 570))
        )


# --------------------------------------------------
# BLACKJACK FUNCTIONS
# --------------------------------------------------

def calculate_hand(cards):

    value = 0
    aces = 0

    for card in cards:

        rank = card.split()[0]

        value += rank_values[rank]

        if rank == "Ace":
            aces += 1

    while value > 21 and aces > 0:

        value -= 10
        aces -= 1

    return value


def create_deck():

    new_deck = []

    for suit in suits:

        for rank in ranks:

            new_deck.append(
                rank + " of " + suit
            )

    random.shuffle(new_deck)

    return new_deck


def finish_round(result, message):

    global game_state, prompt_text, round_result

    round_result = result
    prompt_text = message

    game_state = "finished"


def reset_game():

    global game_state, prompt_text
    global user_text, money, deck, hand
    global hand_value, dealer_hand
    global dealer_hand_value, money_updated
    global round_result

    game_state = "question"
    prompt_text = "Do you want to Gamble?"

    user_text = ""
    money = 0

    deck = []
    hand = []
    hand_value = 0

    dealer_hand = []
    dealer_hand_value = 0

    money_updated = False
    round_result = None


# --------------------------------------------------
# DEALER TURN
# --------------------------------------------------

def play_dealer_turn():

    global dealer_hand
    global dealer_hand_value
    global prompt_text

    dealer_hand = []

    for i in range(2):
        dealer_hand.append(deck.pop())

    dealer_hand_value = calculate_hand(dealer_hand)

    while dealer_hand_value < 17:

        card = deck.pop()
        dealer_hand.append(card)

        dealer_hand_value = calculate_hand(dealer_hand)

    prompt_text = "Dealer's hand: " + ", ".join(dealer_hand)

    prompt_text += (
        "\nDealer's hand value: "
        + str(dealer_hand_value)
    )

    if dealer_hand_value > 21:

        finish_round("win", "Dealer busts! You win!")

    elif dealer_hand_value > hand_value:

        finish_round("loss", "Dealer wins!")

    elif dealer_hand_value < hand_value:

        finish_round("win", "You win!")

    else:

        finish_round("tie", "It's a tie!")


# --------------------------------------------------
# MAIN GAME LOOP
# --------------------------------------------------



async def run_blackjack(screen_surface):
    """Run Blackjack on the shared display without shutting Pygame down."""
    global screen, running, prompt_text, game_state, start_time
    global moneytotal, money, user_text, hand_value, round_result
    global deck, hand, dealer_hand, dealer_hand_value, money_updated

    screen = screen_surface
    running = True
    casino_window_closed = False

    # Start a fresh visit, while preserving the balance shared with Phase 1.
    moneytotal = global_variables.money
    money = 0
    user_text = ""
    prompt_text = "Do you want to Gamble?"
    game_state = "question"
    start_time = 0
    deck = []
    hand = []
    hand_value = 0
    dealer_hand = []
    dealer_hand_value = 0
    money_updated = False
    round_result = None
    question_selection = "YES"

    try:
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        pygame.mixer.music.load(casino_music_path)
        pygame.mixer.music.play(-1)
    except pygame.error as audio_error:
        print("Casino music could not be started:", audio_error)

    while running:

        game_surface.blit(background_surface, (0, 0))

        draw_casino_background(game_surface)

        # --------------------------------------------------
        # HANDLE EVENTS
        # --------------------------------------------------

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                casino_window_closed = True
                running = False

            # MOUSE
            if event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:

                    # Convert fullscreen mouse position
                    mouse_x = (event.pos[0] - OFFSET_X) / SCALE
                    mouse_y = (event.pos[1] - OFFSET_Y) / SCALE

                    virtual_mouse = (mouse_x, mouse_y)

                    if game_state == "question":

                        if buttons["YES"].collidepoint(virtual_mouse):

                            question_selection = "YES"
                            game_state = "welcome"
                            prompt_text = "You clicked YES!"

                            start_time = pygame.time.get_ticks()

                        elif buttons["No"].collidepoint(virtual_mouse):

                            question_selection = "No"
                            running = False

            # KEYBOARD
            if event.type == pygame.KEYDOWN:

                # EXIT FULLSCREEN
                if event.key == pygame.K_ESCAPE:
                    running = False

                # OPENING YES/NO CHOICE: WASD and arrow keys both work.
                elif game_state == "question":
                    if event.key in (pygame.K_w, pygame.K_UP, pygame.K_d, pygame.K_RIGHT):
                        question_selection = "YES"
                    elif event.key in (pygame.K_s, pygame.K_DOWN, pygame.K_a, pygame.K_LEFT):
                        question_selection = "No"
                    elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                        if question_selection == "YES":
                            game_state = "welcome"
                            prompt_text = "You clicked YES!"
                            start_time = pygame.time.get_ticks()
                        else:
                            running = False

                # BETTING STAGE
                elif game_state == "betting":

                    if event.key == pygame.K_BACKSPACE:

                        user_text = user_text[:-1]

                    elif event.key == pygame.K_RETURN:

                        if user_text:

                            try:

                                money = int(user_text)

                                if 0 < money <= moneytotal:

                                    money_updated = False
                                    round_result = None

                                    deck = create_deck()

                                    hand = [
                                        deck.pop(),
                                        deck.pop()
                                    ]

                                    hand_value = calculate_hand(hand)

                                    dealer_hand = []
                                    dealer_hand_value = 0

                                    prompt_text = (
                                        "Your hand: "
                                        + ", ".join(hand)
                                    )

                                    prompt_text += (
                                        "\nYour hand value: "
                                        + str(hand_value)
                                    )

                                    user_text = ""

                                    if hand_value == 21:

                                        finish_round(
                                            "win",
                                            "Blackjack! You win!"
                                        )

                                    else:

                                        prompt_text += (
                                            "\nPress H to hit or S to stand."
                                        )

                                        game_state = "playing"

                                else:

                                    prompt_text = (
                                        "Invalid bet! Enter an amount "
                                        "within your balance."
                                    )

                                    user_text = ""

                            except ValueError:

                                prompt_text = (
                                    "Please enter a valid number."
                                )

                                user_text = ""

                    elif event.unicode.isdigit():

                        user_text += event.unicode

                # PLAYING STAGE
                elif game_state == "playing":

                    if event.key == pygame.K_h:

                        card = deck.pop()

                        hand.append(card)

                        hand_value = calculate_hand(hand)

                        prompt_text = (
                            "Your hand: "
                            + ", ".join(hand)
                        )

                        prompt_text += (
                            "\nYour hand value: "
                            + str(hand_value)
                        )

                        if hand_value > 21:

                            finish_round(
                                "loss",
                                "BUST! You went over 21!"
                            )

                        elif hand_value == 21:

                            prompt_text += (
                                "\nYou got 21! Dealer's turn."
                            )

                            play_dealer_turn()

                        else:

                            prompt_text += (
                                "\nPress H to hit or S to stand."
                            )

                    elif event.key == pygame.K_s:

                        prompt_text = "You chose to stand!"

                        prompt_text += (
                            "\nYour final hand value: "
                            + str(hand_value)
                        )

                        play_dealer_turn()

                # FINISHED STAGE
                elif game_state == "finished":

                    if event.key == pygame.K_q:
                        running = False

                    elif event.key == pygame.K_c:
                        reset_game()

        # --------------------------------------------------
        # TIMED WELCOME SCREENS
        # --------------------------------------------------

        if game_state == "welcome":

            if pygame.time.get_ticks() - start_time >= 2000:

                prompt_text = (
                    "Welcome to Blackjack! You have $"
                    + str(moneytotal)
                    + "."
                )

                game_state = "welcome2"

                start_time = pygame.time.get_ticks()

        if game_state == "welcome2":

            if pygame.time.get_ticks() - start_time >= 3000:

                prompt_text = "How much would you like to bet?"

                game_state = "betting"

        # --------------------------------------------------
        # UPDATE MONEY
        # --------------------------------------------------

        if game_state == "finished" and not money_updated:

            if round_result == "win":
                moneytotal += money

            elif round_result == "loss":
                moneytotal -= money

            money_updated = True

        # --------------------------------------------------
        # DISPLAY
        # --------------------------------------------------

        if game_state == "finished":

            if round_result == "win":
                result_message = "YOU WIN!"

            elif round_result == "loss":
                result_message = "YOU LOSE!"

            else:
                result_message = "IT'S A TIE!"

            lines = [
                result_message,
                "Balance: $" + str(moneytotal),
                "Q: QUIT     C: PLAY AGAIN"
            ]

        else:

            lines = []

            for paragraph in prompt_text.split("\n"):

                wrapped = wrap_text(
                    paragraph,
                    font,
                    600
                )

                lines.extend(wrapped)

        # DEALER HAND
        if game_state == "finished" or game_state == "dealer":

            draw_dealer_section(game_surface)

        # PROMPT BAR
        draw_prompt_panel(game_surface, lines)

        # YES AND NO BUTTONS
        if game_state == "question":

            mouse = pygame.mouse.get_pos()

            virtual_mouse = (
                (mouse[0] - OFFSET_X) / SCALE,
                (mouse[1] - OFFSET_Y) / SCALE
            )

            for name, rect in buttons.items():

                hovered = rect.collidepoint(virtual_mouse)
                selected = name == question_selection

                draw_fancy_button(
                    game_surface,
                    name,
                    rect,
                    hovered,
                    selected
                )

        # BETTING INPUT
        if game_state == "betting":

            draw_fancy_input_box(game_surface)

            text_surface = font.render(
                user_text,
                True,
                LIGHT_GOLD
            )

            text_rectangle = text_surface.get_rect(
                center=input_box.center
            )

            game_surface.blit(
                text_surface,
                text_rectangle
            )

            balance_panel = pygame.Rect(
                250, 370, 300, 60
            )

            draw_panel(game_surface, balance_panel)

            balance_message = font.render(
                "Balance: $" + str(moneytotal),
                True,
                LIGHT_GOLD
            )

            game_surface.blit(
                balance_message,
                balance_message.get_rect(center=(400, 400))
            )

        # FOOTER
        draw_footer(game_surface)

        # --------------------------------------------------
        # SCALE TO FULLSCREEN
        # --------------------------------------------------

        # Fill the whole monitor with the casino artwork first.
        # The game itself is then drawn on top, centred and proportional.

        screen.blit(fullscreen_background, (0, 0))

        scaled_surface = pygame.transform.smoothscale(
            game_surface,
            (
                int(800 * SCALE),
                int(600 * SCALE)
            )
        )

        screen.blit(
            scaled_surface,
            (int(OFFSET_X), int(OFFSET_Y))
        )

        # --------------------------------------------------
        # FULLSCREEN GOLD FRAME
        # --------------------------------------------------

        # Add a matching gold frame around the entire fullscreen image.
        # The original blackjack decorations remain untouched inside it.

        outer_margin = max(8, int(min(WIDTH, HEIGHT) * 0.012))

        fullscreen_frame = pygame.Rect(
            outer_margin,
            outer_margin,
            WIDTH - outer_margin * 2,
            HEIGHT - outer_margin * 2
        )

        pygame.draw.rect(
            screen,
            (77, 48, 17),
            fullscreen_frame,
            width=max(5, int(min(WIDTH, HEIGHT) * 0.006)),
            border_radius=max(8, int(min(WIDTH, HEIGHT) * 0.018))
        )

        pygame.draw.rect(
            screen,
            GOLD,
            fullscreen_frame.inflate(-4, -4),
            width=max(2, int(min(WIDTH, HEIGHT) * 0.003)),
            border_radius=max(7, int(min(WIDTH, HEIGHT) * 0.018) - 3)
        )

        pygame.draw.rect(
            screen,
            LIGHT_GOLD,
            fullscreen_frame.inflate(-9, -9),
            width=1,
            border_radius=max(6, int(min(WIDTH, HEIGHT) * 0.018) - 6)
        )

        # Small gold corner diamonds to carry the original casino styling
        # all the way around the fullscreen frame.

        corner_size = max(5, int(min(WIDTH, HEIGHT) * 0.009))
        corner_positions = [
            (outer_margin + 5, outer_margin + 5),
            (WIDTH - outer_margin - 5, outer_margin + 5),
            (outer_margin + 5, HEIGHT - outer_margin - 5),
            (WIDTH - outer_margin - 5, HEIGHT - outer_margin - 5)
        ]

        for corner_x, corner_y in corner_positions:
            pygame.draw.polygon(
                screen,
                LIGHT_GOLD,
                [
                    (corner_x, corner_y - corner_size),
                    (corner_x + corner_size, corner_y),
                    (corner_x, corner_y + corner_size),
                    (corner_x - corner_size, corner_y)
                ]
            )

        pygame.display.flip()

        clock.tick(60)
        await asyncio.sleep(0)


    # Save the casino balance for the shop phase.
    global_variables.money = moneytotal
    try:
        if pygame.mixer.get_init():
            pygame.mixer.music.fadeout(500)
    except pygame.error:
        pass
    return not casino_window_closed
