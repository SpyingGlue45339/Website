TOTALLY ACCURATE SPACEFLIGHT SIMULATOR - PHASE 2 + TITLE AUDIO FIX
==================================================================

WHAT WAS FIXED
--------------
1. Phase 2 crashed while loading "Images/Ship For movement.png".
   The file was not actually a PNG: its bytes were WebP data despite the
   .png extension. It has now been converted to a genuine RGBA PNG. Both
   Phase 2 code paths that load this ship use the corrected file.

2. The title screen now has a dedicated audio-unlock key:
   - Press M to initialise browser audio and play title.ogg.
   - Press M again to stop title music.
   - Press ENTER / SPACE or click START to begin the game.
   - Starting the game switches to musiccutscene.ogg from that same input
     event, so the opening story soundtrack starts from a user gesture.

3. The previous G shortcut for gambling is not present. The original
   clickable gambling sign and Escape navigation are retained.

INSTALL / BUILD ON WINDOWS
--------------------------
1. Stop any currently running Pygbag server with Ctrl+C.
2. Back up and delete the existing Llama_Space_Programme folder.
3. Extract the included Llama_Space_Programme folder directly into:

   C:\Users\epear\Documents\Website\TASS\

4. Open Command Prompt and run:

   cd /d "C:\Users\epear\Documents\Website\TASS"
   python -m pygbag --ume_block=1 --title "Totally Accurate Spaceflight Simulator" Llama_Space_Programme

5. Open http://localhost:8000
6. On the title screen, press M for the title music, then press ENTER or
   click START to play.

TESTING NOTES
-------------
- All 10 Python files passed Python syntax compilation.
- All image files were checked; no image-extension/content mismatches remain.
- The corrected ship image is verified as PNG RGBA, 212 x 212 pixels.
- Audio files are OGG/Vorbis, 24 kHz mono.
- A Pygbag browser runtime test was not available in the build environment.
