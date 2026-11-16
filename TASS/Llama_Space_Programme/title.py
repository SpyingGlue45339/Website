"""Title screen with an explicit browser-friendly music unlock key."""

import asyncio
import os
import pygame

import audio_manager


async def run_title_screen(screen):
    """Display the title screen until START or quit is selected.

    Press M once to initialise browser audio and start the title soundtrack.
    START also begins the opening cutscene soundtrack directly from the
    player's click/keypress, so audio can still start without pressing M.
    """

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
    hint_font = pygame.font.Font(None, 28)
    status_font = pygame.font.Font(None, 25)

    start_text = font.render("START", False, (255, 235, 195))
    button_rectangle = pygame.Rect(
        button_x,
        button_y,
        button_width,
        button_height
    )

    title_music_path = os.path.join(game_folder, "title.ogg")
    opening_music_path = os.path.join(game_folder, "musiccutscene.ogg")
    title_music_enabled = False
    audio_status = "PRESS M TO ENABLE TITLE MUSIC"

    def enable_title_music():
        nonlocal title_music_enabled, audio_status

        # This function is called from a real KEYDOWN event. That is the
        # browser user gesture needed to unlock Web Audio playback.
        mixer_ready = audio_manager.initialise_from_user_action()
        if not mixer_ready:
            title_music_enabled = False
            audio_status = "AUDIO INITIALISATION FAILED - SEE GAME LOG"
            print("[TITLE AUDIO] Mixer could not be initialised.", flush=True)
            return False

        music_started = audio_manager.start_music(
            title_music_path,
            volume=0.50,
            loops=-1,
            restart=True
        )

        title_music_enabled = bool(music_started)
        if title_music_enabled:
            audio_status = "TITLE MUSIC ENABLED"
        else:
            audio_status = "TITLE MUSIC FAILED TO LOAD - CHECK title.ogg"

        print(
            "[TITLE AUDIO] M pressed | mixer:", pygame.mixer.get_init(),
            "| title music started:", music_started,
            flush=True
        )
        return title_music_enabled

    def start_game_from_user_gesture():
        """Start the opening soundtrack from the START click/keypress."""
        nonlocal title_music_enabled, audio_status

        mixer_ready = audio_manager.initialise_from_user_action()
        print("[TITLE AUDIO] Mixer ready on START:", mixer_ready, flush=True)

        music_started = audio_manager.start_music(
            opening_music_path,
            volume=0.55,
            loops=-1,
            restart=True
        )
        title_music_enabled = bool(music_started)
        audio_status = "OPENING MUSIC ENABLED" if music_started else "OPENING MUSIC UNAVAILABLE"

        print(
            "[TITLE] START accepted | opening music started:", music_started,
            "| mixer:", pygame.mixer.get_init(),
            flush=True
        )
        print("[FLOW] START accepted; opening story is beginning.", flush=True)
        return True

    print("[TITLE] Waiting for START. Press M to enable title music.", flush=True)

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

                if event.key == pygame.K_m:
                    # M toggles title music on/off; the first press unlocks
                    # browser audio inside a real user keypress event.
                    if title_music_enabled:
                        audio_manager.stop_music()
                        title_music_enabled = False
                        audio_status = "TITLE MUSIC OFF - PRESS M TO ENABLE"
                        print("[TITLE AUDIO] M pressed | title music stopped.", flush=True)
                    else:
                        enable_title_music()
                    continue

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
        pygame.draw.rect(screen, button_border_colour, button_rectangle, 6)
        pygame.draw.rect(
            screen,
            button_highlight,
            (button_x + 8, button_y + 8, button_width - 16, 5)
        )

        start_text_rectangle = start_text.get_rect()
        start_text_rectangle.centerx = button_rectangle.centerx
        start_text_rectangle.centery = button_rectangle.centery + 5
        screen.blit(start_text, start_text_rectangle)

        hint_surface = hint_font.render(
            "PRESS M FOR MUSIC  |  ENTER TO START",
            True,
            (235, 225, 205)
        )
        hint_rectangle = hint_surface.get_rect(
            center=(screen_width // 2, min(button_y + button_height + 34, screen_height - 48))
        )
        screen.blit(hint_surface, hint_rectangle)

        status_surface = status_font.render(
            audio_status,
            True,
            (150, 225, 170) if title_music_enabled else (175, 175, 190)
        )
        status_rectangle = status_surface.get_rect(
            center=(screen_width // 2, screen_height - 22)
        )
        screen.blit(status_surface, status_rectangle)

        pygame.display.flip()
        await asyncio.sleep(0)
