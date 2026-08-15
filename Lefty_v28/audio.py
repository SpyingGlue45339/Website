from pathlib import Path
import random
import pygame

# ============================================================
# LEFTY AUDIO SYSTEM — V28
# ============================================================
# The audio system is deliberately tolerant: missing audio never
# prevents the game from starting.
#
# Interactive probabilities:
#   Voice lines = 15%
#   Button      = 60%
#   Newspaper   = 25%
#
# Voice lines use a shuffled no-repeat bag. Every available voice
# line is played once before the bag is reshuffled.
#
# V28 changes:
#   • larger mixer buffer for smoother browser/Pygbag playback
#   • preload all interactive audio at startup
#   • SystemRandom for genuinely fresh shuffles/choices
#   • first voice line is chosen independently and randomly
#   • failed files are excluded from future playback attempts
#   • dedicated voice/SFX channels retained
# ============================================================

AUDIO_DIR = Path(__file__).resolve().parent / "photos" / "audio"
BACKGROUND = AUDIO_DIR / "background.mp3"
SUPPORTED_AUDIO = {".mp3", ".wav", ".ogg"}

AUDIO_GROUPS = (
    ("voice lines", 0.15),
    ("button", 0.60),
    ("newspaper", 0.25),
)

_ready = False
_cache = {}
_failed = set()
_voice_line_bag = []
_sfx_channel = None
_voice_channel = None

# Do not use the module-global pseudo-random sequence for the audio bag.
# SystemRandom gets fresh OS entropy and avoids a repeatable-looking first bag.
_rng = random.SystemRandom()


def initialise():
    """Initialise audio, preload sounds, and start optional background music."""
    global _ready, _sfx_channel, _voice_channel

    try:
        if not pygame.mixer.get_init():
            # A larger buffer is intentional. It trades a tiny amount of
            # latency for much more forgiving timing under Pygbag/browser load.
            pygame.mixer.init(
                frequency=44100,
                size=-16,
                channels=2,
                buffer=2048,
            )

        pygame.mixer.set_num_channels(8)
        _sfx_channel = pygame.mixer.Channel(1)
        _voice_channel = pygame.mixer.Channel(2)
        _ready = True

        print("[Lefty audio] Mixer initialised (buffer=2048).")
        _report_audio_inventory()
        _preload_interactive_audio()
        _reset_voice_bag()
        play_background()

    except (pygame.error, OSError) as exc:
        _ready = False
        print(f"[Lefty audio] Mixer could not initialise: {exc}")


def play_background():
    """Start looping optional background music."""
    if not _ready or not BACKGROUND.exists():
        return

    try:
        pygame.mixer.music.load(str(BACKGROUND))
        pygame.mixer.music.set_volume(0.45)
        pygame.mixer.music.play(-1)
        print(f"[Lefty audio] Background music playing: {BACKGROUND.name}")
    except (pygame.error, OSError) as exc:
        print(f"[Lefty audio] Could not play background music: {exc}")


def stop_background():
    if not _ready:
        return
    try:
        pygame.mixer.music.stop()
    except pygame.error:
        pass


def set_background_volume(volume):
    if not _ready:
        return
    try:
        pygame.mixer.music.set_volume(max(0.0, min(1.0, float(volume))))
    except pygame.error:
        pass


def _files_in(folder_name):
    folder = AUDIO_DIR / folder_name
    if not folder.exists() or not folder.is_dir():
        return []

    try:
        return sorted(
            [
                p for p in folder.iterdir()
                if p.is_file() and p.suffix.lower() in SUPPORTED_AUDIO
            ],
            key=lambda p: p.name.lower(),
        )
    except OSError as exc:
        print(f"[Lefty audio] Could not read {folder}: {exc}")
        return []


def _report_audio_inventory():
    if not _ready:
        return

    print("\n[Lefty audio] ===============================")
    print("[Lefty audio] AUDIO INVENTORY — V28")
    print("[Lefty audio] ===============================")

    total = 0
    for name, _weight in AUDIO_GROUPS:
        files = _files_in(name)
        print(f"[Lefty audio] {name}: {len(files)} file(s)")
        for path in files:
            print(f"[Lefty audio]     - {path.name}")
        total += len(files)

    print(f"[Lefty audio] Total interactive files: {total}")
    print("[Lefty audio] Voice-line probability: 15%")
    print("[Lefty audio] Button probability: 60%")
    print("[Lefty audio] Newspaper probability: 25%")
    print("[Lefty audio] ===============================\n")


def _load_sound(path):
    """Load once and retain the decoded Sound object for the whole game."""
    if path is None or path in _failed:
        return None
    if not path.exists():
        _failed.add(path)
        return None
    if path in _cache:
        return _cache[path]

    try:
        sound = pygame.mixer.Sound(str(path))
        _cache[path] = sound
        return sound
    except (pygame.error, OSError) as exc:
        _failed.add(path)
        print(f"[Lefty audio] FAILED TO LOAD {path.name}: {exc}")
        return None


def _preload_interactive_audio():
    """Decode all available interactive files before gameplay begins."""
    loaded = 0
    failed = 0

    for name, _weight in AUDIO_GROUPS:
        for path in _files_in(name):
            before = path in _cache
            sound = _load_sound(path)
            if sound is not None and not before:
                loaded += 1
            elif sound is None:
                failed += 1

    print(
        f"[Lefty audio] Preloaded {loaded} interactive sound(s)"
        + (f"; {failed} failed." if failed else ".")
    )


def _reset_voice_bag():
    """Create a fresh random permutation of all currently loadable voice lines."""
    global _voice_line_bag
    files = [p for p in _files_in("voice lines") if p in _cache]
    _voice_line_bag = files[:]
    _rng.shuffle(_voice_line_bag)

    if _voice_line_bag:
        print(f"[Lefty audio] Voice bag created: {len(_voice_line_bag)} line(s).")
        print(f"[Lefty audio] First voice line this cycle: {_voice_line_bag[-1].name}")


def _next_voice_line():
    """Pop a line from the no-repeat bag; refill only when exhausted."""
    global _voice_line_bag

    available = [p for p in _files_in("voice lines") if p in _cache and p not in _failed]
    if not available:
        return None

    available_set = set(available)
    _voice_line_bag = [p for p in _voice_line_bag if p in available_set]

    if not _voice_line_bag:
        _voice_line_bag = available[:]
        _rng.shuffle(_voice_line_bag)

    return _voice_line_bag.pop()


def _play_sound(path, channel, volume):
    if path is None or not _ready:
        return False

    sound = _load_sound(path)
    if sound is None:
        return False

    try:
        sound.set_volume(max(0.0, min(1.0, float(volume))))
        if channel is not None:
            channel.play(sound)
        else:
            sound.play()
        return True
    except (pygame.error, OSError) as exc:
        print(f"[Lefty audio] FAILED TO PLAY {path.name}: {exc}")
        return False


def _populated_groups():
    result = []
    for name, _weight in AUDIO_GROUPS:
        files = [p for p in _files_in(name) if p in _cache and p not in _failed]
        if files:
            result.append((name, files))
    return result


def play_random_sound():
    """Play one interactive sound using the 15/60/25 category odds."""
    if not _ready:
        return False

    populated = _populated_groups()
    if not populated:
        return False

    weight_lookup = dict(AUDIO_GROUPS)
    names = [name for name, _files in populated]
    weights = [weight_lookup[name] for name in names]
    chosen = _rng.choices(names, weights=weights, k=1)[0]

    print(f"[Lefty audio] Selected category: {chosen}")

    if chosen == "voice lines":
        # The bag has already been shuffled at startup. Pop exactly one item.
        # If an item somehow fails, try the remaining bag items, but do not
        # put a successfully attempted line back into the current cycle.
        while True:
            path = _next_voice_line()
            if path is None:
                return False
            if _play_sound(path, _voice_channel, 1.0):
                print(f"[Lefty audio] PLAYING VOICE LINE: {path.name}")
                return True
            _failed.add(path)

    files = next(files for name, files in populated if name == chosen)
    candidates = files[:]
    _rng.shuffle(candidates)

    for path in candidates:
        if _play_sound(path, _sfx_channel, 0.80):
            print(f"[Lefty audio] Playing {chosen}: {path.name}")
            return True

    return False


# Existing game code can continue using either name.
play_random_noise = play_random_sound
