TOTALLY ACCURATE SPACEFLIGHT SIMULATOR
RADICAL BROWSER REBUILD
======================================

THIS IS A COMPLETE SOURCE PROJECT
----------------------------------
The Llama_Space_Programme folder contains main.py, every game stage, every
image, every audio file, the font, and the extracted PNG frames used by Phase 2.
There are no separate patch files to merge.

INSTALLATION
------------
1. Close any running Pygbag test server.
2. In Website/TASS, remove the old Llama_Space_Programme folder and the old
   RUN_WEB_TEST.bat / BUILD_FOR_WEB.bat files.
3. Extract this ZIP directly into Website/TASS.
4. You should then have this layout:

   Website/
     index.html
     projects.html
     style.css
     TASS/
       RUN_WEB_TEST.bat
       BUILD_FOR_WEB.bat
       README_RADICAL_FIX.txt
       Llama_Space_Programme/
         main.py
         title.py
         cutscene.py
         phase1.py
         gambling.py
         phase2.py
         phase3.py
         audio_manager.py
         ...all assets...

Do not delete Website/index.html, projects.html, or style.css. Only replace the
old game project and its old build scripts.

REQUIREMENTS
------------
Use the same Python installation in which Pygbag is installed. If needed:

   python -m pip install --upgrade pygbag pygame-ce

LOCAL BROWSER TEST
------------------
Double-click RUN_WEB_TEST.bat.
When Pygbag is ready, open:

   http://localhost:8000

On first load, Pygbag may show its own prompt asking you to click or tap the
page to enable browser media. Click once there. When the game title screen
appears, click START as a separate action. Keep the black Command Prompt
window open during play.

The game title screen is intentionally silent. The Pygbag launch scripts use
its normal media-engagement gate (UME=1), so the browser first asks for a click
or tap to enable media before starting the Python game. Pygame and its mixer
are then initialised normally at startup. When START is pressed, the opening
soundtrack begins inside that actual click/keypress event. The five opening
cutscenes share musiccutscene.ogg, and each scene has its matching cutsceneN.ogg
sound effect.

GAME FLOW
---------
Title -> Opening Cutscenes 1-5 -> Phase 1 Shops

From the Phase 1 exterior:
  - click the Gambling sign, or press G while outside, to enter Blackjack;
  - use ESC as before to leave the exterior and advance to Cutscene 7;
  - inside a shop, ESC returns to the exterior as before;
  - Blackjack returns to the shops and saves the updated balance.

Cutscene 7 -> Phase 2 Rocket Flight -> Cutscene 8 -> Phase 3 Mars.

Phase 2 still checks that the player bought a fuel item, a Gallon of water,
and a rocket engine. If any are missing, it displays the launch-failure screen.

WHAT HAS BEEN REWORKED
----------------------
- One shared Pygame display is created by main.py and reused by all stages.
- One shared Pygame mixer is created at startup after Pygbag's browser
  media-engagement gate and reused by all stages. No phase tears it down.
- All game-stage loops are async-aware and yield with asyncio.sleep(0), as
  required by Pygbag's browser event loop.
- All audio assets used by the game are OGG files for browser compatibility.
- Cutscene soundtrack and sound effects are handled through audio_manager.py.
- Phase 1 shop navigation is preserved; no extra shop-navigation buttons have
  been added.
- Blackjack has explicit entry/exit logging and returns the updated balance.
- Phase 2 loads the asteroid explosion sound once rather than reloading it for
  every collision.
- The main controller prints a clear [FLOW] line at each stage transition.
  If a stage fails, the browser console also receives the Python traceback
  and the game displays an error screen naming the failed stage.

BUILD FOR GITHUB PAGES
----------------------
Double-click BUILD_FOR_WEB.bat.
The generated web build is:

   Llama_Space_Programme/build/web/

Copy the CONTENTS of that folder into your website folder:

   Website/TASS/game/

Your website iframe can then use:

   <iframe src="TASS/game/index.html" width="100%" height="720"
           allow="autoplay; fullscreen" allowfullscreen></iframe>

IMPORTANT TEST NOTE
-------------------
This package has been syntax-checked and its assets have been checked for
presence and valid audio encoding. A full Pygbag/WebAssembly/browser playthrough
cannot be executed in this environment. Please test locally before replacing
the live GitHub Pages build.

If anything fails, send the lines beginning [BOOT], [FLOW], [AUDIO],
[GAMBLING], [PHASE 2], or [CRASH] from the browser console. Those lines now
identify exactly how far the game got.
