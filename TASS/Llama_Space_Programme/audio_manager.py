"""One shared, browser-friendly audio manager for the whole game.

Pygbag's media-engagement gate is enabled for browser builds. main.py
initialises Pygame once after that gate, and every phase reuses the same SDL
mixer; no phase quits or recreates it. The title START event begins the story
soundtrack.
"""

import os
import pygame

AUDIO_READY = False
CURRENT_MUSIC_PATH = None

# Use a conventional browser output format and a larger SDL audio buffer.
# The old 512-sample buffer was particularly susceptible to brief underruns
# during heavier Phase 1 and Phase 3 frames.
MIXER_FREQUENCY = 44100
MIXER_CHANNELS = 2
MIXER_BUFFER = 4096


def initialise_from_user_action():
    """Initialise the shared mixer if startup did not create it."""
    global AUDIO_READY

    try:
        if pygame.mixer.get_init() is None:
            pygame.mixer.init(
                frequency=MIXER_FREQUENCY,
                size=-16,
                channels=MIXER_CHANNELS,
                buffer=MIXER_BUFFER
            )
            pygame.mixer.set_num_channels(16)

        AUDIO_READY = pygame.mixer.get_init() is not None

        if AUDIO_READY:
            pygame.mixer.set_num_channels(16)
            print(
                "[AUDIO] Shared mixer is ready:",
                MIXER_FREQUENCY, "Hz,", MIXER_CHANNELS, "channels,",
                "buffer", MIXER_BUFFER,
                flush=True
            )
        else:
            print("[AUDIO] Mixer initialisation returned no active device.", flush=True)

        return AUDIO_READY

    except pygame.error as audio_error:
        AUDIO_READY = False
        print("[AUDIO] Mixer initialisation failed:", audio_error, flush=True)
        return False


def ensure_audio():
    """Ensure audio exists for later phases; never let audio stop gameplay."""
    global AUDIO_READY

    try:
        AUDIO_READY = pygame.mixer.get_init() is not None
    except pygame.error:
        AUDIO_READY = False

    if AUDIO_READY:
        return True

    return initialise_from_user_action()


def start_music(file_path, volume=0.5, loops=-1, restart=True):
    """Safely load and play one looping music track."""
    global CURRENT_MUSIC_PATH

    if not os.path.isfile(file_path):
        print("[AUDIO] Music file not found:", file_path, flush=True)
        return False

    if not ensure_audio():
        print("[AUDIO] Cannot play music because the mixer is unavailable.", flush=True)
        return False

    absolute_path = os.path.abspath(file_path)

    try:
        if (
            not restart
            and CURRENT_MUSIC_PATH == absolute_path
            and pygame.mixer.music.get_busy()
        ):
            pygame.mixer.music.set_volume(volume)
            return True

        pygame.mixer.music.stop()
        pygame.mixer.music.load(absolute_path)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(loops)
        CURRENT_MUSIC_PATH = absolute_path

        print(
            "[AUDIO] Playing:",
            os.path.basename(absolute_path),
            "| busy:",
            pygame.mixer.music.get_busy(),
            flush=True
        )
        return True

    except pygame.error as audio_error:
        CURRENT_MUSIC_PATH = None
        print("[AUDIO] Could not play", os.path.basename(file_path), ":", audio_error, flush=True)
        return False


def stop_music(fade_ms=0):
    """Stop the music stream without shutting down the shared mixer."""
    global CURRENT_MUSIC_PATH

    try:
        if pygame.mixer.get_init() is not None:
            if fade_ms > 0:
                pygame.mixer.music.fadeout(fade_ms)
            else:
                pygame.mixer.music.stop()
    except pygame.error as audio_error:
        print("[AUDIO] Could not stop music:", audio_error, flush=True)

    CURRENT_MUSIC_PATH = None


def load_sound(file_path, volume=0.8):
    """Load a short OGG effect, returning None if audio is unavailable."""
    if not os.path.isfile(file_path):
        print("[AUDIO] Sound file not found:", file_path, flush=True)
        return None

    if not ensure_audio():
        return None

    try:
        sound = pygame.mixer.Sound(file_path)
        sound.set_volume(volume)
        return sound
    except pygame.error as audio_error:
        print("[AUDIO] Could not load", os.path.basename(file_path), ":", audio_error, flush=True)
        return None


def play_sound(sound):
    """Play an already-loaded sound effect safely."""
    if sound is None:
        return None

    if not ensure_audio():
        return None

    try:
        return sound.play()
    except pygame.error as audio_error:
        print("[AUDIO] Sound effect could not play:", audio_error, flush=True)
        return None
