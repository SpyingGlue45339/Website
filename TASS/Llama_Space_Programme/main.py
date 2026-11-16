"""Main stage controller for Totally Accurate Spaceflight Simulator.

One Pygame display and one mixer are shared by every stage. Each playable
stage is asynchronous and yields to the browser every frame.
"""

import asyncio
import os
import traceback

import pygame

import audio_manager
from cutscene import run_cutscene
from title import run_title_screen


OPENING_CUTSCENES = [
    (
        "cutscene1.png", "sprite.png",
        "You are Professor Leopold Livingstone Llama, a lecturer emeritus in mammalian 17th Century literature. But in your many readings and musings of critical theory, you discovered a terrible truth...",
        "pan_left", 1.1, (100, 400)
    ),
    (
        "cutscene2.png", "sprite2.png",
        "Many animals have travelled into space. Dogs. Monkeys. Cats. Even the humble tardigrade...",
        "pan_right", 1.1, (100, 400)
    ),
    (
        "cutscene3.png", "sprite3.png",
        "But despite President L Bee J's civil rights advancements, no llamas have ever been to space...",
        "zoom_in", 0.8, (600, 200)
    ),
    (
        "cutscene4.png", "sprite2.png",
        "Inspired by the LLM movement, you seek to right this historic wrong...",
        "pan_right", 0.4, None
    ),
    (
        "cutscene5.png", "sprite2.png",
        "You must build your rocket, travel to Mars, and conquer space for the llama race.",
        "pan_left", 0.4, None
    ),
]


async def show_error_screen(screen, stage_name, error_details):
    """Show the actual Python traceback on-screen so browser tools are optional."""
    title_font = pygame.font.Font(None, 42)
    stage_font = pygame.font.Font(None, 27)
    body_font = pygame.font.Font(None, 19)
    hint_font = pygame.font.Font(None, 20)

    screen_width, screen_height = screen.get_size()
    margin_x = 34
    text_width = screen_width - margin_x * 2

    # Wrap each traceback line by measured pixel width, not character count.
    wrapped_lines = []
    for original_line in str(error_details).splitlines():
        remaining = original_line if original_line else " "
        current = ""
        for word in remaining.split(" "):
            candidate = word if not current else current + " " + word
            if body_font.size(candidate)[0] <= text_width:
                current = candidate
            else:
                if current:
                    wrapped_lines.append(current)
                current = word
        if current:
            wrapped_lines.append(current)

    if not wrapped_lines:
        wrapped_lines = ["No traceback text was captured."]

    line_height = body_font.get_linesize() + 2
    visible_line_count = max(1, (screen_height - 245) // line_height)
    scroll_offset = max(0, len(wrapped_lines) - visible_line_count)
    clock = pygame.time.Clock()

    print("[CRASH] Error details shown on the game screen.", flush=True)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_SPACE):
                    return
                if event.key in (pygame.K_UP, pygame.K_PAGEUP):
                    scroll_offset = max(0, scroll_offset - 3)
                elif event.key in (pygame.K_DOWN, pygame.K_PAGEDOWN):
                    scroll_offset = min(
                        max(0, len(wrapped_lines) - visible_line_count),
                        scroll_offset + 3
                    )
                elif event.key == pygame.K_HOME:
                    scroll_offset = 0
                elif event.key == pygame.K_END:
                    scroll_offset = max(0, len(wrapped_lines) - visible_line_count)

        screen.fill((15, 13, 22))
        title_surface = title_font.render(
            "THE SIMULATOR ENCOUNTERED AN ERROR", True, (255, 105, 105)
        )
        screen.blit(title_surface, title_surface.get_rect(center=(screen_width // 2, 36)))

        stage_surface = stage_font.render("Stage: " + str(stage_name), True, (245, 230, 205))
        screen.blit(stage_surface, stage_surface.get_rect(center=(screen_width // 2, 78)))

        hint = hint_font.render(
            "Python traceback (UP/DOWN to scroll; ESC to close)",
            True, (205, 205, 215)
        )
        screen.blit(hint, (margin_x, 112))

        visible_lines = wrapped_lines[scroll_offset:scroll_offset + visible_line_count]
        y = 145
        for line in visible_lines:
            line_surface = body_font.render(line, True, (235, 235, 240))
            screen.blit(line_surface, (margin_x, y))
            y += line_height

        footer = hint_font.render(
            "Lines {}–{} of {}".format(
                scroll_offset + 1,
                min(len(wrapped_lines), scroll_offset + visible_line_count),
                len(wrapped_lines)
            ),
            True, (150, 150, 165)
        )
        screen.blit(footer, (margin_x, screen_height - 34))

        pygame.display.flip()
        clock.tick(30)
        await asyncio.sleep(0)


async def play_cutscene(
    screen,
    stage_name,
    background,
    sprite,
    dialogue,
    motion,
    scale,
    position,
    sound_effect
):
    """Run one cutscene with a consistent set of diagnostics."""
    print("[FLOW] ENTER:", stage_name, flush=True)

    completed = await run_cutscene(
        screen,
        background,
        sprite,
        dialogue,
        motion,
        sprite_scale=scale,
        sprite_position=position,
        sound_effect_filename=sound_effect
    )

    print("[FLOW] EXIT:", stage_name, "| completed:", completed, flush=True)
    return completed


async def main():
    game_folder = os.path.dirname(os.path.abspath(__file__))
    current_stage = "Pygame startup"

    # Pygbag's media-engagement gate is enabled in the launch scripts. The
    # browser therefore waits for its first real page interaction before this
    # code starts. Initialise Pygame normally at that point so SDL's audio
    # device is created inside the browser's permitted media session.
    pygame.mixer.pre_init(44100, -16, 2, 4096)
    initialised_count, failed_count = pygame.init()

    print(
        "[BOOT] pygame.init() completed | initialised:",
        initialised_count,
        "| failed:",
        failed_count,
        flush=True
    )

    mixer_details = pygame.mixer.get_init()
    print("[AUDIO] Mixer at startup:", mixer_details, flush=True)

    if mixer_details is not None:
        pygame.mixer.set_num_channels(16)

    if mixer_details is None:
        try:
            pygame.mixer.init(44100, -16, 2, 4096)
            pygame.mixer.set_num_channels(16)
            print("[AUDIO] Explicit mixer fallback succeeded:", pygame.mixer.get_init(), flush=True)
        except pygame.error as audio_error:
            print("[AUDIO] Explicit mixer fallback failed:", audio_error, flush=True)

    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Totally Accurate Spaceflight Simulator")

    print("============================================================", flush=True)
    print("TOTALLY ACCURATE SPACEFLIGHT SIMULATOR", flush=True)
    print("[BOOT] Main Python entry point is running.", flush=True)
    print("[BOOT] Display created: 1280 x 720.", flush=True)
    print("============================================================", flush=True)

    try:
        # Import all stages after the single display and mixer exist, but
        # before the player starts. This catches missing assets/import errors
        # at startup rather than halfway through a game transition.
        current_stage = "Loading game modules"
        print("[BOOT] Loading Phase 1, Blackjack, Phase 2 and Phase 3.", flush=True)
        import phase1
        import gambling
        import phase2
        import phase3
        print("[BOOT] All game modules imported successfully.", flush=True)

        opening_music_path = os.path.join(game_folder, "musiccutscene.ogg")
        current_stage = "Title screen"
        print("[FLOW] ENTER: Title screen", flush=True)
        title_accepted = await run_title_screen(screen)
        print("[FLOW] EXIT: Title screen | accepted:", title_accepted, flush=True)

        if not title_accepted:
            print("[FLOW] Game ended at the title screen.", flush=True)
            return

        # title.py starts this track directly from the START input event.
        # Do not load/restart it here: keeping the same stream avoids cutting
        # off the beginning of the music or losing the browser gesture.

        # ------------------------------------------------------------
        # OPENING STORY: five scenes, one continuous music track.
        # ------------------------------------------------------------
        for index, scene in enumerate(OPENING_CUTSCENES, start=1):
            (
                background,
                sprite,
                dialogue,
                motion,
                scale,
                position
            ) = scene

            current_stage = "Opening cutscene " + str(index)
            sound_effect = "cutscene" + str(index) + ".ogg"

            completed = await play_cutscene(
                screen,
                current_stage,
                background,
                sprite,
                dialogue,
                motion,
                scale,
                position,
                sound_effect
            )

            if not completed:
                print("[FLOW] Opening story cancelled by the player.", flush=True)
                return

        audio_manager.stop_music(fade_ms=700)
        print("[FLOW] Opening story complete.", flush=True)

        # ------------------------------------------------------------
        # PHASE 1 AND BLACKJACK.
        # False = leave the shops and continue to Cutscene 7.
        # True  = the player selected gambling; return to the shops after it.
        # None  = the game/window was closed.
        # ------------------------------------------------------------
        current_stage = "Loading Phase 1"
        print("[FLOW] Phase 1 module is ready.", flush=True)

        while True:
            current_stage = "Phase 1: shops"
            print("[FLOW] ENTER: Phase 1 shops.", flush=True)

            phase1_result = await phase1.run_phase1(screen)

            print(
                "[FLOW] EXIT: Phase 1 shops | result:",
                repr(phase1_result),
                flush=True
            )

            if phase1_result is None:
                print("[FLOW] Phase 1 ended because the game window was closed.", flush=True)
                return

            if phase1_result is False:
                print("[FLOW] Phase 1 complete. Next stage is Cutscene 7.", flush=True)
                break

            if phase1_result is True:
                current_stage = "Loading Blackjack"
                print("[FLOW] Gambling selected. Blackjack module is ready.", flush=True)

                current_stage = "Blackjack"
                print("[FLOW] ENTER: Blackjack.", flush=True)
                blackjack_returned = await gambling.run_blackjack(screen)
                print("[FLOW] EXIT: Blackjack | returned:", blackjack_returned, flush=True)

                if not blackjack_returned:
                    print("[FLOW] Blackjack window was closed.", flush=True)
                    return

                print("[FLOW] Returning from Blackjack to the Phase 1 shops.", flush=True)
                continue

            raise RuntimeError(
                "Phase 1 returned an unexpected result: " + repr(phase1_result)
            )

        # ------------------------------------------------------------
        # CUTSCENE 7: this must run after ESC from the outside shop screen.
        # ------------------------------------------------------------
        current_stage = "Cutscene 7 music"
        audio_manager.start_music(
            opening_music_path,
            volume=0.55,
            loops=-1,
            restart=True
        )

        current_stage = "Cutscene 7"
        completed = await play_cutscene(
            screen,
            "Cutscene 7",
            "cutscene7.png",
            "sprite7.png",
            "Your journey continues... into outer space!",
            "zoom_in",
            1,
            (400, 300),
            "cutscene7.ogg"
        )

        if not completed:
            print("[FLOW] Cutscene 7 was cancelled.", flush=True)
            return

        audio_manager.stop_music(fade_ms=700)

        # ------------------------------------------------------------
        # PHASE 2: rocket launch and flight.
        # ------------------------------------------------------------
        current_stage = "Loading Phase 2"
        print("[FLOW] Phase 2 module is ready.", flush=True)

        current_stage = "Phase 2"
        print("[FLOW] ENTER: Phase 2 rocket flight.", flush=True)
        phase2_completed = await phase2.run_phase2(screen)
        print("[FLOW] EXIT: Phase 2 | completed:", phase2_completed, flush=True)

        if not phase2_completed:
            print("[FLOW] Phase 2 did not complete; stopping here as designed.", flush=True)
            return

        # ------------------------------------------------------------
        # CUTSCENE 8 AND PHASE 3.
        # ------------------------------------------------------------
        current_stage = "Cutscene 8 music"
        audio_manager.start_music(
            opening_music_path,
            volume=0.55,
            loops=-1,
            restart=True
        )

        current_stage = "Cutscene 8"
        completed = await play_cutscene(
            screen,
            "Cutscene 8",
            "cutscene5.png",
            "sprite7.png",
            "Congratulations! Your mission has brought you one step closer to the stars. But the real adventure is only just beginning...",
            "zoom_in",
            1.2,
            (400, 400),
            "cutscene8.ogg"
        )

        if not completed:
            print("[FLOW] Cutscene 8 was cancelled.", flush=True)
            return

        audio_manager.stop_music(fade_ms=700)

        current_stage = "Loading Phase 3"
        print("[FLOW] Phase 3 module is ready.", flush=True)

        current_stage = "Phase 3"
        print("[FLOW] ENTER: Phase 3 Mars exploration.", flush=True)
        phase3_completed = await phase3.run_phase3(screen)
        print("[FLOW] EXIT: Phase 3 | completed:", phase3_completed, flush=True)

        if phase3_completed:
            print("[FLOW] GAME COMPLETE.", flush=True)
        else:
            print("[FLOW] Phase 3 ended early.", flush=True)

    except Exception:
        error_details = traceback.format_exc()
        print("\n============================================================", flush=True)
        print("[CRASH] THE GAME CRASHED DURING:", current_stage, flush=True)
        print("[CRASH] Full Python traceback:", flush=True)
        print(error_details, flush=True)
        print("============================================================\n", flush=True)
        await show_error_screen(screen, current_stage, error_details)

    finally:
        audio_manager.stop_music()
        pygame.quit()
        print("[BOOT] Pygame shut down.", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
