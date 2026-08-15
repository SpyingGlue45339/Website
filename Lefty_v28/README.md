# Political Compass — Lefty Simulator V27

Run from this folder:
    python main.py

If necessary:
    pip install pygame-ce

The `sections` folder is REQUIRED and contains `__init__.py` plus the four question files.

Architecture:
main.py → title → section intro → questions → intermissions → results

Scoring is isolated in scoring.py. Question data is isolated by section.
The project remains pure Pygame and therefore remains suitable for Pygbag.

Pygbag:
    python -m pygbag main.py

V27 keeps the current 38 questions and their current X/Y scalings.

## Results-page changes

- Main result uses the available page space more effectively.
- The main compass is compact rather than a wide banner.
- Overall result writing is more substantial and personalised to the user's own result.
- Analysis cards retain the hover expansion/highlight effect.
- The analysis action is anchored to the right of each card.
- Section sliders now show their directional labels at the correct left/right ends.
- Economy explicitly treats its vertical measure as economic intervention rather than liberty/authority.

## Audio

Interactive sound probabilities are:
- voice lines = 15%
- button = 60%
- newspaper = 25%

Voice lines use a shuffled no-repeat bag. Audio loading now retries a fallback file if
one selected sound cannot be decoded. WAV/OGG/MP3 work directly; MP4/M4A voice files
are converted to WAV on desktop when FFmpeg is available.

The project reports the number of discovered audio files at startup. Optional audio files
must actually be present in `photos/audio/voice lines`, `photos/audio/button`, or
`photos/audio/newspaper`; empty folders cannot produce sound.

## Answer choices

STRONGLY DISAGREE · DISAGREE · AGREE · STRONGLY AGREE
