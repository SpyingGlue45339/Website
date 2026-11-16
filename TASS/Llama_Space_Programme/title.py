import asyncio
import os
import pygame

import audio_manager


async def run_title_screen(screen):
    """Show the title card and unlock audio from the START user gesture."""

    screen_width = screen.get_width()
    screen_height = screen.get_height()
    game_folder = os.path.dirname(os.path.abspath(__file__))

    background_image = pygame.image.load(
        os.path.join(game_folder, "background.png")
    ).convert()
    background_image = pygame.transform.scale(
        background_image,
        (screen_width, screen_height)
    )

    logo_image = pygame.image.load(
        os.path.join(game_folder, "logo.png")
    ).convert_alpha()

    logo_width = int(screen_width * 0.65)
    logo_height = int(
        logo_image.get_height() * (logo_width / logo_image.get_width())
    )
    logo_image = pygame.transform.scale(logo_image, (logo_width, logo_height))

    logo_x = (screen_width - logo_width) // 2
    logo_y = (screen_height - logo_height) // 2 - 80

    button_width = 240
    button_height = 75
    button_x = (screen_width - button_width) // 2
    button_y = logo_y + logo_height + 40

    button_colour = (190, 65, 100)
    button_hover_colour = (245, 105, 90)
    button_border_colour = (55, 20, 65)
    button_highlight = (255, 185, 100)

    font = pygame.font.Font(None, 60)
    start_text = font.render("START", False, (255, 235, 195))

    button_rectangle = pygame.Rect(
        button_x,
        button_y,
        button_width,
        button_height
    )

    def start_game_from_user_gesture():
        """Start the opening soundtrack in the actual START input event.

        Pygbag has already passed its media-engagement gate and main.py has
        initialised the shared mixer. Starting the track here keeps playback
        directly tied to the player's START click or keypress.
        """
        opening_music = os.path.join(game_folder, "musiccutscene.ogg")
        music_started = audio_manager.start_music(
            opening_music,
            volume=0.55,
            loops=-1,
            restart=True
        )
        print(
            "[TITLE] START accepted | opening music started:",
            music_started,
            "| mixer:",
            pygame.mixer.get_init(),
            flush=True
        )
        print("[FLOW] START accepted; opening story is beginning.", flush=True)
        return True

    print("[TITLE] Waiting for START input.", flush=True)

    while True:
        mouse_position = pygame.mouse.get_pos()
        mouse_over_button = button_rectangle.collidepoint(mouse_position)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("[TITLE] Window close requested.", flush=True)
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("[TITLE] ESC pressed; leaving game.", flush=True)
                    return False

                if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                    return start_game_from_user_gesture()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click_position = getattr(event, "pos", pygame.mouse.get_pos())
                if button_rectangle.collidepoint(click_position):
                    return start_game_from_user_gesture()

            if event.type == pygame.FINGERDOWN:
                finger_position = (
                    int(event.x * screen_width),
                    int(event.y * screen_height)
                )
                if button_rectangle.collidepoint(finger_position):
                    return start_game_from_user_gesture()

        screen.blit(background_image, (0, 0))
        screen.blit(logo_image, (logo_x, logo_y))

        current_button_colour = (
            button_hover_colour if mouse_over_button else button_colour
        )

        pygame.draw.rect(screen, current_button_colour, button_rectangle)
        pygame.draw.rect(
            screen,
            button_border_colour,
            button_rectangle,
            6
        )
        pygame.draw.rect(
            screen,
            button_highlight,
            (button_x + 8, button_y + 8, button_width - 16, 5)
        )

        start_text_rectangle = start_text.get_rect()
        start_text_rectangle.centerx = button_rectangle.centerx
        start_text_rectangle.centery = button_rectangle.centery + 5
        screen.blit(start_text, start_text_rectangle)

        pygame.display.flip()
        await asyncio.sleep(0)
