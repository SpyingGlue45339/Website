TOTALLY ACCURATE SPACEFLIGHT SIMULATOR
======================================

RUNNING ON DESKTOP
------------------
1. Keep the Llama_Space_Programme folder and its assets together.
2. Install the required package:

       python -m pip install -r requirements.txt

3. Start the game:

       python main.py

BROWSER BUILD
-------------
This folder is adapted for Pygbag/WebAssembly:
- Every interactive stage is asynchronous and yields to the browser.
- Audio uses OGG files.
- Explosion animations use PNG frame sequences rather than Pillow at runtime.
- The display and mixer are each shared by every stage.
- Press M on the title screen to initialise browser audio and play title.ogg.
- Press ENTER or click START to begin the opening soundtrack.
- The ship sprite is stored as a genuine PNG (not WebP data with a .png suffix).

For the local browser test and GitHub Pages build, use the BAT files in the
parent folder and read README_RADICAL_FIX.txt there.

GAME STRUCTURE
--------------
- main.py owns the shared display, stage sequence and Pygame lifecycle.
- audio_manager.py owns the single shared audio mixer and music/effect helpers.
- title.py contains the title screen.
- cutscene.py contains the animated story scenes.
- phase1.py contains the shops and inventory.
- gambling.py contains The Golden Ace Blackjack minigame.
- phase2.py contains rocket flight.
- phase3.py contains Mars exploration.
- global_variables.py stores resources shared between game stages.
- events.py contains the random Mars events.

DISPLAY AND INPUT
-----------------
The game uses a shared 1280 x 720 display. The shops, Blackjack, rocket flight,
cutscenes and Mars exploration all run in this same Pygame session.


AUDIO / INPUT UPDATE
- Gambling is opened by clicking the Gambling sign. The G key intentionally does nothing.
- Music and effects are stored as OGG Vorbis, re-encoded from the original project audio.
- The shared mixer uses 44.1 kHz stereo and a 2048-sample buffer to reduce browser audio underruns.
