"""Browser-friendly entry point for Totally Accurate Spaceflight Simulator.

The opening title and cutscenes are loaded before the much larger game stages.
Each later stage is imported only when it is needed. This reduces the amount
of image/audio data that the browser has to load before the first cutscene.
"""

import asyncio
import os
import traceback
import pygame

from cutscene import run_cutscene
from title import run_title_screen


def start_cutscene_music(game_folder):
    """Start the shared cutscene soundtrack when browser audio is available."""
    music_path = os.path.join(game_folder, "musiccutscene.ogg")

    try:
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.set_volume(0.55)
        pygame.mixer.music.play(-1)
    except pygame.error as audio_error:
        # Audio must never prevent the game itself from running in a browser.
        print("Cutscene music could not be started:", audio_error)


def stop_cutscene_music():
    """Stop the cutscene soundtrack, if the audio subsystem is available."""
    try:
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()
    except pygame.error as audio_error:
        print("Cutscene music could not be stopped:", audio_error)


async def show_error_screen(screen, stage_name):
    """Keep a readable message on screen if a stage raises an exception."""
    try:
        title_font = pygame.font.Font(None, 52)
        body_font = pygame.font.Font(None, 30)
        small_font = pygame.font.Font(None, 24)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_RETURN):
                    return

            screen.fill((15, 13, 22))
            title_surface = title_font.render("THE SIMULATOR ENCOUNTERED AN ERROR", True, (255, 105, 105))
            stage_surface = body_font.render("Stage: " + stage_name, True, (245, 230, 205))
            detail_surface = small_font.render("Open the browser console (F12) for the Python traceback.", True, (205, 205, 215))
            exit_surface = small_font.render("Press ESC or ENTER to close.", True, (205, 205, 215))

            screen.blit(title_surface, title_surface.get_rect(center=(screen.get_width() // 2, 250)))
            screen.blit(stage_surface, stage_surface.get_rect(center=(screen.get_width() // 2, 325)))
            screen.blit(detail_surface, detail_surface.get_rect(center=(screen.get_width() // 2, 390)))
            screen.blit(exit_surface, exit_surface.get_rect(center=(screen.get_width() // 2, 430)))
            pygame.display.flip()
            await asyncio.sleep(0)
    except Exception:
        # If the display itself is the cause, retain the original traceback.
        return


async def main():
    game_folder = os.path.dirname(os.path.abspath(__file__))

    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Totally Accurate Spaceflight Simulator")

    current_stage = "Pygame startup"

    try:
        # Do not import phase1, gambling, phase2 or phase3 here.
        # Those modules load many large images and sounds at import time.
        # The browser only needs the title and opening cutscenes initially.

        current_stage = "Title screen"
        print("Starting Title Screen...")
        if not await run_title_screen(screen):
            return

        opening_cutscenes = [
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

        current_stage = "Opening cutscene soundtrack"
        print("Starting opening cutscene soundtrack...")
        start_cutscene_music(game_folder)

        for index, scene in enumerate(opening_cutscenes, start=1):
            current_stage = "Opening cutscene " + str(index)
            print("Starting Cutscene", index, "...")
            background, sprite, dialogue, motion, scale, position = scene
            sound_effect_filename = "cutscene" + str(index) + ".ogg"

            if not await run_cutscene(
                screen,
                background,
                sprite,
                dialogue,
                motion,
                sprite_scale=scale,
                sprite_position=position,
                sound_effect_filename=sound_effect_filename
            ):
                return

        stop_cutscene_music()

        # Import Phase 1 only when the player has finished the opening story.
        current_stage = "Loading Phase 1"
        print("Loading Phase 1...")
        import phase1

        while True:
            current_stage = "Phase 1: shops"
            print("Starting Phase 1...")
            gambling_requested = await phase1.run_phase1(screen)

            if gambling_requested is None:
                return

            if not gambling_requested:
                print("Phase 1 finished. Continuing to the next cutscene...")
                break

            current_stage = "Loading Blackjack"
            print("Loading The Golden Ace - Blackjack...")
            import gambling

            current_stage = "Blackjack"
            if not await gambling.run_blackjack(screen):
                return
            print("Returning to Phase 1...")

        current_stage = "Cutscene 7 soundtrack"
        print("Starting Cutscene 7...")
        start_cutscene_music(game_folder)

        current_stage = "Cutscene 7"
        if not await run_cutscene(
            screen,
            "cutscene7.png",
            "sprite7.png",
            "You must build your rocket, travel to Mars, and conquer space for the llama race...",
            "zoom_in",
            sprite_scale=1,
            sprite_position=(400, 300),
            sound_effect_filename="cutscene7.ogg"
        ):
            return

        stop_cutscene_music()

        current_stage = "Loading Phase 2"
        print("Loading Phase 2...")
        import phase2

        current_stage = "Phase 2"
        print("Starting Phase 2...")
        if not await phase2.run_phase2(screen):
            return

        current_stage = "Cutscene 8 soundtrack"
        print("Starting Cutscene 8 soundtrack...")
        start_cutscene_music(game_folder)

        current_stage = "Cutscene 8"
        print("Starting Cutscene 8 (Phase 2 to Phase 3)...")
        if not await run_cutscene(
            screen,
            "cutscene5.png",
            "sprite7.png",
            "Congratulations! Your mission has brought you one step closer to the stars. But the real adventure is only just beginning...",
            "zoom_in",
            sprite_scale=1.2,
            sprite_position=(400, 400),
            sound_effect_filename="cutscene8.ogg"
        ):
            return

        stop_cutscene_music()

        current_stage = "Loading Phase 3"
        print("Loading Phase 3...")
        import phase3

        current_stage = "Phase 3"
        print("Starting Phase 3...")
        if not await phase3.run_phase3(screen):
            return

        print("Game finished!")

    except Exception:
        print("\n============================================================")
        print("THE GAME CRASHED DURING:", current_stage)
        print("Full Python traceback:")
        traceback.print_exc()
        print("============================================================\n")
        await show_error_screen(screen, current_stage)

    finally:
        try:
            if pygame.mixer.get_init():
                pygame.mixer.music.stop()
        except pygame.error:
            pass
        pygame.quit()


if __name__ == "__main__":
    asyncio.run(main())
