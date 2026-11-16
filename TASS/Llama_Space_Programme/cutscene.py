import asyncio
import pygame
import os

import audio_manager


async def run_cutscene(
    screen,
    background_filename,
    sprite_filename,
    dialogue,
    camera_motion="none",
    sprite_scale=0.4,
    sprite_position=None,
    sound_effect_filename=None
):

    # ----------------------------------
    # SCREEN SETTINGS
    # ----------------------------------

    screen_width = screen.get_width()
    screen_height = screen.get_height()

    game_folder = os.path.dirname(os.path.abspath(__file__))

    clock = pygame.time.Clock()

    # ----------------------------------
    # LOAD BACKGROUND
    # ----------------------------------

    background_image = pygame.image.load(
        os.path.join(game_folder, background_filename)
    ).convert()

    background_image = pygame.transform.scale(
        background_image,
        (screen_width, screen_height)
    )

    # ----------------------------------
    # LOAD SPRITE
    # ----------------------------------

    sprite_image = pygame.image.load(
        os.path.join(game_folder, sprite_filename)
    ).convert_alpha()

    # Calculate sprite dimensions
    sprite_width = int(sprite_image.get_width() * sprite_scale)
    sprite_height = int(sprite_image.get_height() * sprite_scale)

    # Resize sprite
    sprite_image = pygame.transform.scale(
        sprite_image,
        (sprite_width, sprite_height)
    )

    # Set default sprite position
    if sprite_position is None:

        sprite_position = (
            screen_width // 2,
            screen_height // 2
        )

    # Calculate sprite top-left corner
    sprite_x = sprite_position[0] - sprite_width // 2
    sprite_y = sprite_position[1] - sprite_height // 2

    # ----------------------------------
    # CREATE SCENE
    # ----------------------------------

    scene_surface = pygame.Surface(
        (screen_width, screen_height)
    )

    scene_surface.blit(
        background_image,
        (0, 0)
    )

    scene_surface.blit(
        sprite_image,
        (sprite_x, sprite_y)
    )

    # ----------------------------------
    # LOAD OPTIONAL SOUND EFFECT
    # ----------------------------------

    sound_effect = None
    sound_effect_channel = None

    if sound_effect_filename is not None:

        sound_effect_path = os.path.join(
            game_folder,
            sound_effect_filename
        )

        if os.path.isfile(sound_effect_path):
            sound_effect = audio_manager.load_sound(sound_effect_path, volume=0.8)
            if sound_effect is None:
                print("[AUDIO] Cutscene sound effect unavailable:", sound_effect_filename, flush=True)
        else:
            print("[AUDIO] Cutscene sound effect was not found: " + sound_effect_filename, flush=True)

    def stop_sound_effect():

        if sound_effect_channel is not None:
            try:
                sound_effect_channel.stop()
            except pygame.error:
                pass

    # ----------------------------------
    # DIALOGUE BOX SETTINGS
    # ----------------------------------

    # Dialogue font
    dialogue_font = pygame.font.SysFont(
        "Comic Sans MS",
        38,
        bold=True
    )

    # Dialogue text colour
    text_colour = (40, 30, 25)

    # Dialogue box colours
    box_colour = (245, 225, 185)
    box_outline_colour = (55, 35, 25)

    # Box settings
    horizontal_padding = 60
    vertical_padding = 35

    # Maximum width of dialogue box
    maximum_box_width = int(screen_width * 0.8)

    # Maximum width available for text
    maximum_text_width = maximum_box_width - horizontal_padding * 2

    # Split dialogue into individual words
    words = dialogue.split()

    # Store dialogue lines
    dialogue_lines = []

    # Start with an empty line
    current_line = ""

    # Work through every word
    for word in words:

        # Test what happens if we add this word
        if current_line == "":
            test_line = word
        else:
            test_line = current_line + " " + word

        # Measure the width of the test line
        test_width = dialogue_font.size(test_line)[0]

        # Check whether the word fits
        if test_width <= maximum_text_width:

            current_line = test_line

        else:

            # Save the previous line
            if current_line != "":
                dialogue_lines.append(current_line)

            # Start a new line
            current_line = word

    # Add final line
    if current_line != "":
        dialogue_lines.append(current_line)

    # ----------------------------------
    # CALCULATE BOX SIZE
    # ----------------------------------

    # Find the widest line
    widest_line_width = 0

    for line in dialogue_lines:

        line_width = dialogue_font.size(line)[0]

        if line_width > widest_line_width:
            widest_line_width = line_width

    # Calculate total text height
    line_height = dialogue_font.get_height()

    total_text_height = len(dialogue_lines) * line_height

    # Calculate box dimensions
    box_width = widest_line_width + horizontal_padding * 2
    box_height = total_text_height + vertical_padding * 2

    # Position box at bottom centre
    box_x = (screen_width - box_width) // 2
    box_y = screen_height - box_height - 45

    # Create dialogue rectangle
    dialogue_box = pygame.Rect(
        box_x,
        box_y,
        box_width,
        box_height
    )

    # ----------------------------------
    # CAMERA SETTINGS
    # ----------------------------------

    valid_camera_motions = [
        "none",
        "pan_left",
        "pan_right",
        "zoom_in",
        "zoom_out"
    ]

    if camera_motion not in valid_camera_motions:

        raise ValueError(
            "Invalid camera motion: " + camera_motion
        )

    motion_duration = 8.0

    maximum_zoom = 1.2

    animation_time = 0

    # ----------------------------------
    # DRAW SCENE FUNCTION
    # ----------------------------------

    def draw_scene(camera_progress, fade_alpha):

        # Keep camera progress between 0 and 1
        camera_progress = max(
            0,
            min(1, camera_progress)
        )

        # ----------------------------------
        # DETERMINE ZOOM
        # ----------------------------------

        zoom = 1.0

        if camera_motion == "zoom_in":

            zoom = 1.0 + (maximum_zoom - 1.0) * camera_progress

        elif camera_motion == "zoom_out":

            zoom = maximum_zoom - (maximum_zoom - 1.0) * camera_progress

        elif camera_motion in ["pan_left", "pan_right"]:

            zoom = maximum_zoom

        # ----------------------------------
        # RESIZE SCENE
        # ----------------------------------

        scaled_width = int(screen_width * zoom)
        scaled_height = int(screen_height * zoom)

        scaled_scene = pygame.transform.scale(
            scene_surface,
            (scaled_width, scaled_height)
        )

        # ----------------------------------
        # CALCULATE CAMERA POSITION
        # ----------------------------------

        maximum_camera_x = scaled_width - screen_width
        maximum_camera_y = scaled_height - screen_height

        camera_x = maximum_camera_x // 2
        camera_y = maximum_camera_y // 2

        if camera_motion == "pan_left":

            camera_x = int(
                maximum_camera_x * (1 - camera_progress)
            )

        elif camera_motion == "pan_right":

            camera_x = int(
                maximum_camera_x * camera_progress
            )

        # ----------------------------------
        # DRAW BACKGROUND AND SPRITE
        # ----------------------------------

        screen.blit(
            scaled_scene,
            (-camera_x, -camera_y)
        )

        # ----------------------------------
        # DRAW DIALOGUE BOX
        # ----------------------------------

        pygame.draw.rect(
            screen,
            box_colour,
            dialogue_box,
            border_radius=20
        )

        pygame.draw.rect(
            screen,
            box_outline_colour,
            dialogue_box,
            width=5,
            border_radius=20
        )

        # ----------------------------------
        # DRAW DIALOGUE TEXT
        # ----------------------------------

        line_height = dialogue_font.get_height()

        total_text_height = len(dialogue_lines) * line_height

        text_y = dialogue_box.centery - total_text_height // 2

        for line in dialogue_lines:

            rendered_text = dialogue_font.render(
                line,
                False,
                text_colour
            )

            text_rectangle = rendered_text.get_rect(
                centerx=dialogue_box.centerx,
                y=text_y
            )

            screen.blit(
                rendered_text,
                text_rectangle
            )

            text_y += line_height

        # ----------------------------------
        # FADE OVERLAY
        # ----------------------------------

        if fade_alpha > 0:

            fade_surface = pygame.Surface(
                (screen_width, screen_height)
            )

            fade_surface.fill((0, 0, 0))

            fade_surface.set_alpha(
                int(fade_alpha)
            )

            screen.blit(
                fade_surface,
                (0, 0)
            )

        pygame.display.flip()

    # ----------------------------------
    # START OPTIONAL SOUND EFFECT
    # ----------------------------------

    # This plays once alongside the background music.
    # The background soundtrack itself is controlled by main.py.
    if sound_effect is not None:
        sound_effect_channel = audio_manager.play_sound(sound_effect)
        print(
            "[AUDIO] Cutscene effect:",
            sound_effect_filename,
            "| channel started:",
            sound_effect_channel is not None,
            flush=True
        )

    # ----------------------------------
    # FADE IN
    # ----------------------------------

    fade_alpha = 255

    fade_speed = 350

    while fade_alpha > 0:

        delta_time = clock.tick(60) / 1000

        animation_time += delta_time

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                stop_sound_effect()
                return False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    stop_sound_effect()
                    return False

        camera_progress = animation_time / motion_duration

        draw_scene(
            camera_progress,
            fade_alpha
        )

        fade_alpha -= fade_speed * delta_time

        if fade_alpha < 0:
            fade_alpha = 0

        await asyncio.sleep(0)

    # ----------------------------------
    # WAIT FOR PLAYER
    # ----------------------------------

    scene_finished = False

    while not scene_finished:

        delta_time = clock.tick(60) / 1000

        animation_time += delta_time

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                stop_sound_effect()
                return False

            if event.type == pygame.KEYDOWN:

                if event.key in [
                    pygame.K_SPACE, pygame.K_RETURN,
                    pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d,
                    pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT
                ]:
                    scene_finished = True

                if event.key == pygame.K_ESCAPE:
                    stop_sound_effect()
                    return False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    scene_finished = True

            if event.type == pygame.FINGERDOWN:
                scene_finished = True

        camera_progress = animation_time / motion_duration

        draw_scene(
            camera_progress,
            0
        )

        await asyncio.sleep(0)

    # ----------------------------------
    # FADE OUT
    # ----------------------------------

    fade_alpha = 0

    while fade_alpha < 255:

        delta_time = clock.tick(60) / 1000

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                stop_sound_effect()
                return False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    stop_sound_effect()
                    return False

        camera_progress = animation_time / motion_duration

        draw_scene(
            camera_progress,
            fade_alpha
        )

        fade_alpha += fade_speed * delta_time

        if fade_alpha > 255:
            fade_alpha = 255

        await asyncio.sleep(0)

    # Stop the optional one-shot clip when this scene finishes so that it
    # cannot spill into the next cutscene.
    stop_sound_effect()

    return True
