import asyncio
import os
import pygame
import global_variables
import audio_manager

# The main launcher creates the one shared Pygame display.
# This module only draws onto the surface passed to run_phase1().
screen_width = 1280
screen_height = 720
screen = None

clock = pygame.time.Clock()
fps = 60
llama_frame_time = 300  # Milliseconds per frame: increase this to make the bobbing slower.

folder = os.path.dirname(os.path.abspath(__file__))

# ------------------------------------------------------------
# SHOP MUSIC AND SOUND EFFECTS
# ------------------------------------------------------------

# The shop music is started when this phase is entered.
shopping_music_path = os.path.join(folder, "shopping.ogg")

# Load the purchase sound effect.
buying_sound_path = os.path.join(folder, "buying.ogg")
buying_sound = audio_manager.load_sound(buying_sound_path, volume=0.8)

font_path = os.path.join(folder, "ShareTechMono-Regular.ttf")

font_big = pygame.font.Font(font_path, 42)
font_medium = pygame.font.Font(font_path, 27)
font_small = pygame.font.Font(font_path, 23)
font_small_italic = pygame.font.Font(font_path, 21)
font_tiny = pygame.font.Font(font_path, 19)

outside_image_name = "outside_shops.png"
propulsion_image_name = "propulsion_workshop.png"
life_support_image_name = "life_support_pharmacy.png"
supplies_image_name = "supplies_supermarket.png"
electronics_image_name = "electronics_tech_shop.png"
safety_image_name = "safety_shop.png"
base_image_name = "base_shop.png"
llama_image_1_name = "llama_bob_frame_1.png"
llama_image_2_name = "llama_bob_frame_2.png"


def load_pic(image_name):

    image_path = os.path.join(folder, image_name)

    if os.path.isfile(image_path):

        picture = pygame.image.load(image_path).convert_alpha()

        return picture

    print("Could not find image:", image_name)

    return None


outside_background = load_pic(outside_image_name)
propulsion_background = load_pic(propulsion_image_name)
life_support_background = load_pic(life_support_image_name)
supplies_background = load_pic(supplies_image_name)
electronics_background = load_pic(electronics_image_name)
safety_background = load_pic(safety_image_name)
base_background = load_pic(base_image_name)
llama_frame_1 = load_pic(llama_image_1_name)

llama_frame_2 = load_pic(llama_image_2_name)

# ------------------------------------------------------------
# BLIMP IMAGE
# ------------------------------------------------------------

# Load the blue blimp. The image should be in the same folder as this file.
blimp_image = load_pic("blimp.png")

# Resize the blimp while preserving its original proportions.
if blimp_image is not None:
    blimp_width = 500
    blimp_height = int(
        blimp_image.get_height() * blimp_width / blimp_image.get_width()
    )

    blimp_image = pygame.transform.smoothscale(
        blimp_image,
        (blimp_width, blimp_height)
    )

# The Gambling button sits over the gondola underneath the blimp.
# Its position is relative to the blimp's position, which is (20, 20).
# Move it slightly higher so it sits more naturally on the gondola.
gambling_button_rect = pygame.Rect(20 + 180, 20 + 70, 175, 42)

if outside_background is not None:
    outside_background = pygame.transform.scale(outside_background, (screen_width, screen_height))

if llama_frame_1 is not None:
    llama_frame_1 = pygame.transform.scale(llama_frame_1, (400, 400))

if llama_frame_2 is not None:
    llama_frame_2 = pygame.transform.scale(llama_frame_2, (400, 400))

if propulsion_background is not None:
    propulsion_background = pygame.transform.scale(propulsion_background, (screen_width, screen_height))

if life_support_background is not None:
    life_support_background = pygame.transform.scale(life_support_background, (screen_width, screen_height))

if supplies_background is not None:
    supplies_background = pygame.transform.scale(supplies_background, (screen_width, screen_height))

if electronics_background is not None:
    electronics_background = pygame.transform.scale(electronics_background, (screen_width, screen_height))

if safety_background is not None:
    safety_background = pygame.transform.scale(safety_background, (screen_width, screen_height))

if base_background is not None:
    base_background = pygame.transform.scale(base_background, (screen_width, screen_height))


# rocket stuffz

rocket_shop = [
    ["High-efficiency rocket engine", 35000, "Propulsion", "Gets more thrust from every drop of fuel."],
    ["Heavy-duty rocket engine", 50000, "Propulsion", "A powerful engine for carrying heavier loads."],
    ["Dugong Deliverables Premium Fuel", 18000, "Propulsion", "High-performance, unlike Leopold in bed."],
    ["Fuel (small)", 4000, "Propulsion", "VAT-free, regulation-free, insurance-free, and practically free."],
    ["Fuel (large)", 9000, "Propulsion", "Cheaper to buy in bulk!"],
    ["Engine cooling system", 4000, "Propulsion", "Stops the engine from getting a little too toasty."],

    ["Plethora of plants", 1200, "Life Support", "They just look nice, innit..."],
    ["Soil filtration system", 4000, "Life Support", "An apple a day keeps the perchlorates away."],
    ["Air filtration system", 3500, "Life Support", "Filters unwanted particles from the cabin air."],
    ["Emergency oxygen supply", 2000, "Life Support", "A backup supply for rather unfortunate moments."],
    ["Temperature regulation system", 4500, "Life Support", "Keeps the cabin at the right temperature for rice pudding."],
    ["Water recycling system", 8000, "Life Support", "Many people say urea-water tastes scrummdidlyumptious."],
    ["Hydroponic crop system", 5500, "Life Support", "Grow food at your base using water and electrical power."],

    ["Basic food rations (5 days)", 1000, "Supplies", "Five days of ASDA own-brand ready meals."],
    ["Premium food rations (5 days)", 2000, "Supplies", "Five days of slightly less painful meals."],
    ["Packet of crisps", 10, "Supplies", "All you need for Mars is a bag of Ready Salted?"],
    ["Gallon of water", 1000, "Supplies", "Fresh from Finneas Fennex Fox's fine... well...you know..."],
    ["Water storage tank", 1500, "Supplies", "Extra capacity for carrying water and storing it at your base."],

    ["Navigational computer", 3500, "Electronics", "Helps you work out where you are going."],
    ["Steering wheel", 3500, "Electronics", "XBOX compatible; it greatly increases your manoeuverability."],
    ["Scout drone", 6000, "Electronics", "A small probe found on the surface of Hoth."],
    ["Long-range radio transmitter", 4500, "Electronics", "For contacting fellow Llamas from very far away."],
    ["Solar panels", 5000, "Electronics", "Turns sunlight into useful electrical power."],
    ["Self-sweeping solar panels", 20000, "Electronics", "Solar panels that clean themselves. Useless."],
    ["Backup battery", 2500, "Electronics", "Stores electricity for when the Sun is on strike."],
    ["Laser blaster", 2500, "Electronics", "A laser blaster. Suitable for children 3 and under."],

    ["Basic spacesuit", 6000, "Safety", "A standard suit for going outside the rocket."],
    ["Advanced spacesuit", 12000, "Safety", "Leopold wishes he has this level of protection in bed."],
    ["Emergency medical kit", 1500, "Safety", "Sometimes llamas get dysentery..."],
    ["Radiation shielding", 8500, "Safety", "The UAE Safety Board says this could help you in this quest."],
    ["Emergency escape system", 10000, "Safety", "An emergency way out if things go very wrong."],

    ["Concrete box", 6000, "Base", "A sturdy, if rather uninspiring, IKEA template."],
    ["Polycarbon dome", 30000, "Base", "A large, slightly performative, dome for your lunar base."]
]


# VARIABLES:
# Load starting game variables

money = global_variables.money

food = global_variables.food
water = global_variables.water
# Water quantity and water storage capacity are separate resources.
# Older versions of global_variables.py may not yet define water_capacity.
water_capacity = getattr(global_variables, "water_capacity", max(100, water))
oxygen = global_variables.oxygen

energy = global_variables.energy
power = global_variables.power

rad = global_variables.rad

inventory = global_variables.inventory

status_message = ""


# These rectangles sit over the six black doorways in outside_shops.png.
# The background is resized from 1672 x 941 to 1280 x 720.

shop_entrances = [
    ["Propulsion", pygame.Rect(693, 149, 191, 101)],
    ["Life Support", pygame.Rect(964, 151, 190, 102)],
    ["Supplies", pygame.Rect(693, 355, 188, 93)],
    ["Electronics", pygame.Rect(966, 357, 188, 90)],
    ["Safety", pygame.Rect(694, 552, 184, 96)],
    ["Base", pygame.Rect(967, 560, 181, 89)]
]

button_left = 350
button_top = 130
button_width = 580
button_min_height = 116
button_gap_y = 10

# The list scrolls in pixels, not item counts. This matters because item cards
# have different heights depending on their descriptions.
shop_viewport = pygame.Rect(button_left, button_top, button_width, 495)
scroll_offset = 0
scrollbar_dragging = False
scrollbar_drag_grab = 0
scroll_pixels_per_wheel_notch = 75

# The item cards keep their original overall width, but their height is
# calculated from the amount of text they need to display.
button_text_width = 390
button_padding_top = 18
button_padding_bottom = 16
button_line_gap = 5


def wrap_text(message, font, maximum_width):

    words = str(message).split()

    lines = []
    current_line = ""

    for word in words:

        if current_line == "":
            proposed_line = word
        else:
            proposed_line = current_line + " " + word

        proposed_width = font.size(proposed_line)[0]

        if proposed_width <= maximum_width:
            current_line = proposed_line
        else:
            if current_line != "":
                lines.append(current_line)

            # Split an individual word if it is wider than the available space.
            if font.size(word)[0] > maximum_width:

                partial_word = ""

                for character in word:

                    proposed_partial_word = partial_word + character

                    if font.size(proposed_partial_word)[0] <= maximum_width:
                        partial_word = proposed_partial_word
                    else:
                        if partial_word != "":
                            lines.append(partial_word)
                        partial_word = character

                current_line = partial_word

            else:
                current_line = word

    if current_line != "":
        lines.append(current_line)

    if len(lines) == 0:
        lines.append("")

    return lines


def get_item_text_layout(item):

    item_name = item[0]
    item_subtitle = item[3]

    name_lines = wrap_text(item_name, font_medium, button_text_width)
    subtitle_lines = wrap_text(item_subtitle, font_small_italic, button_text_width)

    name_line_height = font_medium.get_linesize()
    subtitle_line_height = font_small_italic.get_linesize()

    required_height = (
        button_padding_top
        + len(name_lines) * name_line_height
        + button_line_gap
        + len(subtitle_lines) * subtitle_line_height
        + button_padding_bottom
    )

    required_height = max(button_min_height, required_height)

    return name_lines, subtitle_lines, required_height


def get_button(item_number, item):
    """Return an item's on-screen rectangle using the pixel scroll offset.

    item_number is the item's index in the current shop's complete list.
    Cards above the viewport are still included in the layout calculation,
    which keeps every shop's scrolling consistent regardless of card height.
    """
    button_y = button_top - scroll_offset
    available_items = get_items(current_shop)

    for previous_number in range(item_number):
        if previous_number < len(available_items):
            previous_item = available_items[previous_number]
            button_y += get_item_text_layout(previous_item)[2] + button_gap_y

    button_height = get_item_text_layout(item)[2]
    return pygame.Rect(button_left, button_y, button_width, button_height)


def get_shop_content_height(shop_name):
    """Calculate the full pixel height of all cards in a shop."""
    items = get_items(shop_name)
    if not items:
        return 0

    cards_height = sum(get_item_text_layout(item)[2] for item in items)
    gaps_height = max(0, len(items) - 1) * button_gap_y
    return cards_height + gaps_height


def get_max_scroll(shop_name):
    return max(0, get_shop_content_height(shop_name) - shop_viewport.height)


def clamp_scroll(shop_name):
    global scroll_offset
    scroll_offset = max(0, min(int(scroll_offset), get_max_scroll(shop_name)))


def get_scrollbar_rects(shop_name):
    """Return the scrollbar track and thumb for the current shop."""
    track = pygame.Rect(button_left + button_width + 12, shop_viewport.y, 14, shop_viewport.height)
    content_height = get_shop_content_height(shop_name)

    if content_height <= shop_viewport.height:
        thumb_height = track.height
    else:
        thumb_height = max(38, int(track.height * shop_viewport.height / content_height))
        thumb_height = min(track.height, thumb_height)

    maximum_scroll = get_max_scroll(shop_name)
    available_thumb_travel = track.height - thumb_height
    if maximum_scroll > 0 and available_thumb_travel > 0:
        thumb_y = track.y + round((scroll_offset / maximum_scroll) * available_thumb_travel)
    else:
        thumb_y = track.y

    thumb = pygame.Rect(track.x, thumb_y, track.width, thumb_height)
    return track, thumb


def set_scroll_from_mouse(shop_name, mouse_y, grab_offset):
    """Move the scrollbar thumb to the mouse and update the pixel offset."""
    global scroll_offset
    track, thumb = get_scrollbar_rects(shop_name)
    maximum_scroll = get_max_scroll(shop_name)
    travel = track.height - thumb.height

    if maximum_scroll <= 0 or travel <= 0:
        scroll_offset = 0
        return

    thumb_y = max(track.y, min(mouse_y - grab_offset, track.bottom - thumb.height))
    fraction = (thumb_y - track.y) / travel
    scroll_offset = round(fraction * maximum_scroll)


def get_items(shop_name):

    shop_items = []

    for item in rocket_shop:

        if item[2] == shop_name:

            shop_items.append(item)

    return shop_items


def item_effect(item):

    global food, water, water_capacity, oxygen

    item_name = item[0]

    if item_name == "Emergency oxygen supply":

        oxygen = oxygen + 20

    if item_name == "Basic food rations (5 days)":

        food = food + 50

    if item_name == "Premium food rations (5 days)":

        food = food + 100

    if item_name == "Packet of crisps":

        food = food + 1

    # One gallon is approximately 3.785 litres.
    # The game's previous 10-litre water supply was worth 100 water units,
    # so one gallon is worth approximately 38 water units.
    if item_name == "Gallon of water":

        water = water + 38

    # A storage tank increases the maximum amount that can be stored.
    # It does not magically add water to the current supply.
    if item_name == "Water storage tank":

        water_capacity = water_capacity + 50


def buy(item):

    global money, status_message

    if item not in rocket_shop:

        status_message = "That item is no longer available."

        return

    item_price = item[1]

    if money < item_price:

        status_message = "Insufficient funds!"

        return

    money = money - item_price

    inventory.append(item.copy())

    rocket_shop.remove(item)

    item_effect(item)

    # Play the purchase sound only after a successful purchase.
    audio_manager.play_sound(buying_sound)

    status_message = "Purchased: " + item[0]


def text(message, font, colour, x, y, centred=False):

    words = font.render(str(message), True, colour)

    words_rect = words.get_rect()

    if centred:

        words_rect.center = (x, y)

    else:

        words_rect.topleft = (x, y)

    screen.blit(words, words_rect)


def box(rectangle, fill_colour, border_colour):

    pygame.draw.rect(screen, fill_colour, rectangle, border_radius=7)

    pygame.draw.rect(screen, border_colour, rectangle, 2, border_radius=7)


def money_display():

    money_text = "MONEY: £" + str(money)

    money_text_width = font_medium.size(money_text)[0]

    money_box_width = money_text_width + 34
    money_box_height = font_medium.get_linesize() + 18

    money_box = pygame.Rect(
        screen_width - money_box_width - 25,
        18,
        money_box_width,
        money_box_height
    )

    box(money_box, (35, 30, 27), (220, 176, 112))

    text(money_text, font_medium, (255, 230, 160), money_box.centerx, money_box.centery, True)


def item_button(item, item_number, mouse_position):
    """Draw one item card. item_number is its absolute shop-list index."""
    button_rect = get_button(item_number, item)
    mouse_is_over = button_rect.collidepoint(mouse_position)

    if mouse_is_over:
        button_colour = (75, 94, 105)
        border_colour = (255, 225, 155)
    else:
        button_colour = (35, 34, 34)
        border_colour = (190, 160, 120)

    box(button_rect, button_colour, border_colour)

    item_price = "£" + str(item[1])
    name_lines, subtitle_lines, required_height = get_item_text_layout(item)
    name_line_height = font_medium.get_linesize()
    subtitle_line_height = font_small_italic.get_linesize()

    text_y = button_rect.y + button_padding_top
    for name_line in name_lines:
        text(name_line, font_medium, (255, 250, 235), button_rect.x + 20, text_y)
        text_y += name_line_height

    text_y += button_line_gap
    for subtitle_line in subtitle_lines:
        text(subtitle_line, font_small_italic, (205, 198, 180), button_rect.x + 20, text_y)
        text_y += subtitle_line_height

    text(item_price, font_medium, (255, 220, 135), button_rect.right - 110, button_rect.centery, True)


def draw_llama():

    frame_number = (pygame.time.get_ticks() // llama_frame_time) % 2

    if frame_number == 0:

        llama_picture = llama_frame_1

    else:

        llama_picture = llama_frame_2

    if llama_picture is not None:

        screen.blit(llama_picture, (190, 300))


def fake_outside():

    screen.fill((105, 135, 153))

    pygame.draw.rect(screen, (126, 158, 174), (0, 0, screen_width, 430))

    pygame.draw.rect(screen, (75, 100, 84), (0, 405, screen_width, 100))

    pygame.draw.rect(screen, (63, 59, 58), (0, 625, screen_width, 95))

    for shop in shop_entrances:

        door = shop[1]

        pygame.draw.rect(screen, (26, 24, 24), door)

        pygame.draw.rect(screen, (190, 151, 103), door, 5)


def outside(mouse_position):
    if outside_background is not None:
        screen.blit(outside_background, (0, 0))
    else:
        fake_outside()

    draw_llama()

    # Draw the large blimp and its clickable Gambling sign.
    if blimp_image is not None:
        screen.blit(blimp_image, (20, 20))

    # Draw the clickable casino sign independently of the decorative blimp.
    # That way a missing/failed blimp image cannot disable gambling.
    gambling_mouse_position = pygame.mouse.get_pos()
    gambling_button_colour = (250, 240, 215)
    gambling_border_colour = (
        (35, 190, 85)
        if gambling_button_rect.collidepoint(gambling_mouse_position)
        else (30, 150, 65)
    )
    gambling_text_colour = (20, 105, 45)

    pygame.draw.rect(screen, gambling_button_colour, gambling_button_rect, border_radius=7)
    pygame.draw.rect(screen, gambling_border_colour, gambling_button_rect, width=3, border_radius=7)

    gambling_text = font_small.render("Gambling", True, gambling_text_colour)
    gambling_text_rect = gambling_text.get_rect(center=gambling_button_rect.center)
    screen.blit(gambling_text, gambling_text_rect)

    # Shop entrances are selected with the mouse only; no keyboard shop picker.
    for shop in shop_entrances:
        shop_name, door = shop
        if door.collidepoint(mouse_position):
            pygame.draw.rect(screen, (255, 220, 130), door, 4)
            text(shop_name, font_medium, (255, 220, 130), door.centerx, door.centery, True)

    text("Click a shop to enter", font_small, (40, 34, 30), 25, 690)
    text("G: casino   |   ESC: next phase", font_small, (40, 34, 30), 865, 690)
    text("I: inventory", font_small, (40, 34, 30), 1120, 690)


def inside(mouse_position, current_shop):
    backgrounds = {
        "Propulsion": propulsion_background,
        "Life Support": life_support_background,
        "Supplies": supplies_background,
        "Electronics": electronics_background,
        "Safety": safety_background,
        "Base": base_background,
    }
    shop_background = backgrounds.get(current_shop)

    if shop_background is not None:
        screen.blit(shop_background, (0, 0))
    else:
        screen.fill((65, 48, 38))
        text("Interior image missing: " + current_shop, font_medium, (255, 230, 190), screen_width // 2, 350, True)

    text(current_shop.upper(), font_big, (255, 240, 210), screen_width // 2, 55, True)
    money_display()

    available_items = get_items(current_shop)
    clamp_scroll(current_shop)

    if available_items:
        # Clip cards to the same viewport used by the scroll limit. Partially
        # visible cards are drawn and remain clickable inside the viewport.
        previous_clip = screen.get_clip()
        screen.set_clip(shop_viewport)

        for item_number, item in enumerate(available_items):
            item_rect = get_button(item_number, item)
            if item_rect.colliderect(shop_viewport):
                item_button(item, item_number, mouse_position)

        screen.set_clip(previous_clip)

        track, thumb = get_scrollbar_rects(current_shop)
        if get_max_scroll(current_shop) > 0:
            pygame.draw.rect(screen, (42, 36, 31), track, border_radius=7)
            pygame.draw.rect(screen, (210, 185, 145), thumb, border_radius=7)
            pygame.draw.rect(screen, (255, 230, 185), thumb, width=2, border_radius=7)
    else:
        text("Everything in this shop has been purchased!", font_medium, (255, 245, 220), screen_width // 2, 365, True)

    if status_message:
        text(status_message, font_small, (255, 235, 180), screen_width // 2, 650, True)

    text("Mouse wheel or scrollbar: browse items", font_tiny, (245, 235, 220), 25, 685)
    text("ESC: back to shops   |   I: inventory", font_tiny, (245, 235, 220), 755, 685)


def inventory_screen():

    screen.fill((48, 38, 31))

    text("INVENTORY", font_big, (255, 230, 190), screen_width // 2, 55, True)

    money_display()

    text("Press I or ESC to return", font_small, (230, 215, 190), screen_width // 2, 95, True)

    if len(inventory) == 0:

        text("You have not bought anything yet.", font_medium, (255, 240, 215), screen_width // 2, 350, True)

    else:

        for item_number in range(len(inventory)):

            column = item_number % 2

            row = item_number // 2

            item_x = 55 + column * 610

            item_y = 130 + row * 32

            item_name = inventory[item_number][0]

            item_price = "£" + str(inventory[item_number][1])

            item_name_width = font_tiny.size(item_name)[0]
            item_price_width = font_tiny.size(item_price)[0]

            item_box_width = max(565, item_name_width + item_price_width + 45)
            item_box_width = min(item_box_width, 590)

            item_name_lines = wrap_text(item_name, font_tiny, item_box_width - item_price_width - 45)

            item_box_height = max(32, len(item_name_lines) * font_tiny.get_linesize() + 12)

            item_box = pygame.Rect(item_x, item_y, item_box_width, item_box_height)

            box(item_box, (70, 57, 45), (170, 135, 95))

            text_y = item_y + 6

            for item_name_line in item_name_lines:

                text(item_name_line, font_tiny, (255, 245, 225), item_x + 10, text_y)

                text_y += font_tiny.get_linesize()

            text(item_price, font_tiny, (255, 220, 150), item_box.right - item_price_width - 12, item_y + 6)


current_screen = "outside"
current_shop = ""
previous_screen = "outside"

# This flag tells main.py whether the player clicked the Gambling sign.
gambling_requested = False



async def run_phase1(screen_surface):
    """Run the shops on the display owned by main.py.

    Returns True when the player requests the casino, False when the
    shop phase is finished, or None when the window is closed.
    """
    global screen, current_screen, current_shop, previous_screen
    global gambling_requested, running, scroll_offset, status_message
    global scrollbar_dragging, scrollbar_drag_grab
    global money, food, water, water_capacity, oxygen, energy, power, rad, inventory

    screen = screen_surface
    running = True
    phase1_window_closed = False

    # Refresh state in case the player has just returned from Blackjack.
    money = global_variables.money
    food = global_variables.food
    water = global_variables.water
    water_capacity = getattr(global_variables, "water_capacity", max(100, water))
    oxygen = global_variables.oxygen
    energy = global_variables.energy
    power = global_variables.power
    rad = global_variables.rad
    inventory = global_variables.inventory

    current_screen = "outside"
    current_shop = ""
    previous_screen = "outside"
    gambling_requested = False
    scroll_offset = 0
    scrollbar_dragging = False
    scrollbar_drag_grab = 0
    status_message = ""

    shopping_music_started = audio_manager.start_music(
        shopping_music_path,
        volume=0.45,
        loops=-1
    )
    print(
        "[AUDIO] Phase 1 shopping music started:",
        shopping_music_started,
        "| mixer:",
        pygame.mixer.get_init(),
        flush=True
    )

    while running:
        clock.tick(fps)
        mouse_position = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.FINGERDOWN:
                finger_position = (
                    int(event.x * screen_width),
                    int(event.y * screen_height)
                )
                event = pygame.event.Event(
                    pygame.MOUSEBUTTONDOWN,
                    {"pos": finger_position, "button": 1}
                )

            if event.type == pygame.QUIT:
                phase1_window_closed = True
                running = False
                # Stop processing this batch immediately.
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g and current_screen == "outside":
                    # Keyboard fallback for the casino sign, useful in the browser.
                    gambling_requested = True
                    running = False
                    print("[GAMBLING] G key selected Blackjack.", flush=True)
                    break

                if event.key == pygame.K_ESCAPE:
                    if current_screen == "inventory":
                        current_screen = previous_screen
                    elif current_screen == "inside":
                        current_screen = "outside"
                        current_shop = ""
                        scroll_offset = 0
                        scrollbar_dragging = False
                        status_message = ""
                    else:
                        # ESC from the outside shop area advances to Phase 2.
                        # Break immediately so later queued events cannot turn
                        # this normal transition into a window-close exit.
                        running = False
                        print("[FLOW] Phase 1 exit requested with ESC.", flush=True)
                        break

                elif event.key == pygame.K_i:
                    if current_screen == "inventory":
                        current_screen = previous_screen
                    else:
                        previous_screen = current_screen
                        current_screen = "inventory"
                        scrollbar_dragging = False

                # Shop purchases remain mouse-driven. G is a casino shortcut
                # only while outside; ESC and I retain their original meanings.

            elif event.type == pygame.MOUSEWHEEL and current_screen == "inside":
                # Scroll when the pointer is over the item list or its bar.
                pointer = pygame.mouse.get_pos()
                track, _ = get_scrollbar_rects(current_shop)
                scroll_area = shop_viewport.union(track)
                if scroll_area.collidepoint(pointer):
                    scroll_offset -= int(event.y * scroll_pixels_per_wheel_notch)
                    clamp_scroll(current_shop)

            elif event.type == pygame.MOUSEBUTTONDOWN and current_screen == "inside":
                if event.button in (4, 5):
                    # Legacy wheel events on older Pygame/platform combinations.
                    scroll_offset += (-1 if event.button == 4 else 1) * scroll_pixels_per_wheel_notch
                    clamp_scroll(current_shop)
                    continue

                if event.button == 1:
                    track, thumb = get_scrollbar_rects(current_shop)

                    if get_max_scroll(current_shop) > 0 and thumb.collidepoint(event.pos):
                        scrollbar_dragging = True
                        scrollbar_drag_grab = event.pos[1] - thumb.y
                        continue

                    if get_max_scroll(current_shop) > 0 and track.collidepoint(event.pos):
                        scrollbar_drag_grab = thumb.height // 2
                        set_scroll_from_mouse(current_shop, event.pos[1], scrollbar_drag_grab)
                        scrollbar_dragging = True
                        continue

                    if shop_viewport.collidepoint(event.pos):
                        available_items = get_items(current_shop)
                        for item_number, item in enumerate(available_items):
                            item_rect = get_button(item_number, item)
                            if item_rect.colliderect(shop_viewport) and item_rect.collidepoint(event.pos):
                                buy(item)
                                clamp_scroll(current_shop)
                                break

            elif event.type == pygame.MOUSEMOTION and scrollbar_dragging and current_screen == "inside":
                set_scroll_from_mouse(current_shop, event.pos[1], scrollbar_drag_grab)

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                scrollbar_dragging = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and current_screen == "outside":
                # Clicking Gambling launches the Blackjack minigame.
                if gambling_button_rect.collidepoint(event.pos):
                    gambling_requested = True
                    running = False
                    print("[GAMBLING] Sign clicked at:", event.pos, flush=True)
                    break

                for shop_name, door in shop_entrances:
                    if door.collidepoint(event.pos):
                        current_screen = "inside"
                        current_shop = shop_name
                        scroll_offset = 0
                        scrollbar_dragging = False
                        status_message = ""
                        break

        if current_screen == "outside":
            outside(mouse_position)
        elif current_screen == "inside":
            inside(mouse_position, current_shop)
        elif current_screen == "inventory":
            inventory_screen()

        pygame.display.flip()
        await asyncio.sleep(0)

    # Fade out the shop music. Pygame itself stays running for the next phase.
    audio_manager.stop_music(fade_ms=1000)

    # Keep the player's resources available to every later phase.
    global_variables.money = money
    global_variables.food = food
    global_variables.water = water
    global_variables.water_capacity = water_capacity
    global_variables.oxygen = oxygen
    global_variables.energy = energy
    global_variables.power = power
    global_variables.rad = rad
    global_variables.inventory = inventory

    return None if phase1_window_closed else gambling_requested
