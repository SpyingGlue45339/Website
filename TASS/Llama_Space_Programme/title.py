
import asyncio
import pygame
import os


async def run_title_screen(screen):

    # Get screen dimensions
    screen_width = screen.get_width()
    screen_height = screen.get_height()

    # Find folder containing images and music
    game_folder = os.path.dirname(os.path.abspath(__file__))

    # Load title music
    pygame.mixer.music.load(
        os.path.join(game_folder, "title.ogg")
    )

    # Browsers block autoplay until the player interacts with the game.
    # Start the soundtrack on the first key press or mouse click instead.
    pygame.mixer.music.set_volume(0.5)
    title_music_started = False

    # Load background
    background_image = pygame.image.load(
        os.path.join(game_folder, "background.png")
    ).convert()

    background_image = pygame.transform.scale(
        background_image,
        (screen_width, screen_height)
    )

    # Load logo
    logo_image = pygame.image.load(
        os.path.join(game_folder, "logo.png")
    ).convert_alpha()

    # Resize logo
    logo_width = int(screen_width * 0.65)
    logo_height = int(
        logo_image.get_height() * (logo_width / logo_image.get_width())
    )

    logo_image = pygame.transform.scale(
        logo_image,
        (logo_width, logo_height)
    )

    # Position logo
    logo_x = (screen_width - logo_width) // 2
    logo_y = (screen_height - logo_height) // 2 - 80

    # Button dimensions
    button_width = 240
    button_height = 75

    button_x = (screen_width - button_width) // 2
    button_y = logo_y + logo_height + 40

    # Button colours - retro sunset theme
    button_colour = (190, 65, 100)
    button_hover_colour = (245, 105, 90)
    button_border_colour = (55, 20, 65)
    button_highlight = (255, 185, 100)

    # Font
    font = pygame.font.Font(None, 60)

    # Render button text once
    start_text = font.render("START", False, (255, 235, 195))

    running = True

    while running:

        mouse_position = pygame.mouse.get_pos()

        button_rectangle = pygame.Rect(
            button_x,
            button_y,
            button_width,
            button_height
        )

        mouse_over_button = button_rectangle.collidepoint(mouse_position)

        # Events
        for event in pygame.event.get():

            if (
                not title_music_started
                and event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN)
            ):
                pygame.mixer.music.play(-1)
                title_music_started = True

            if event.type == pygame.QUIT:

                pygame.mixer.music.fadeout(500)
                return False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.fadeout(500)
                    return False

                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    pygame.mixer.music.fadeout(1000)
                    return True

            if event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1 and mouse_over_button:

                    pygame.mixer.music.fadeout(1000)
                    return True

        # Draw background
        screen.blit(background_image, (0, 0))

        # Draw logo
        screen.blit(logo_image, (logo_x, logo_y))

        # Button colour
        if mouse_over_button:
            current_button_colour = button_hover_colour
        else:
            current_button_colour = button_colour

        # Draw button
        pygame.draw.rect(
            screen,
            current_button_colour,
            button_rectangle
        )

        # Dark outline
        pygame.draw.rect(
            screen,
            button_border_colour,
            button_rectangle,
            6
        )

        # Pixel-style highlights
        pygame.draw.rect(
            screen,
            button_highlight,
            (button_x + 8, button_y + 8, button_width - 16, 5)
        )

        # Button text - perfectly centred
        start_text_rectangle = start_text.get_rect()

        start_text_rectangle.centerx = button_rectangle.centerx
        start_text_rectangle.centery = button_rectangle.centery + 5

        screen.blit(start_text, start_text_rectangle)

        pygame.display.flip()
        await asyncio.sleep(0)
