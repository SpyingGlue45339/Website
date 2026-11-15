TOTALLY ACCURATE SPACEFLIGHT SIMULATOR - BROWSER VERSION
========================================================

WHAT CHANGED IN THIS FIX
------------------------
- The title screen and opening cutscenes load before the larger game stages.
- Phase 1, Blackjack, Phase 2 and Phase 3 are imported only when needed.
  This reduces startup memory use and avoids loading all stages before the
  opening cutscenes.
- Audio is treated as optional. If a browser audio device or file cannot be
  loaded, the game should continue without that sound rather than stopping.
- If a Python exception occurs, the screen displays the stage where it failed.
  Open the browser developer console (F12 -> Console) to see the traceback.

IMPORTANT: BUILD THE GAME FOLDER, NOT THE PYTHON FILE
-----------------------------------------------------
The Llama_Space_Programme folder contains main.py and all the assets.
Run Pygbag against that folder.

EASIEST METHOD ON WINDOWS
-------------------------
1. Extract this ZIP into your Website/TASS folder.
2. Open the TASS folder.
3. Double-click RUN_WEB_TEST.bat.
4. Open http://localhost:8000 when the server is ready.

MANUAL TEST COMMAND
-------------------
Open a terminal in the folder containing Llama_Space_Programme and run:

    python -m pygbag Llama_Space_Programme

BUILD FOR GITHUB PAGES
----------------------
Double-click BUILD_FOR_WEB.bat, or run:

    python -m pygbag --build Llama_Space_Programme

The browser files are generated in:

    Llama_Space_Programme/build/web/

Copy the CONTENTS of build/web into your website folder:

    Website/TASS/game/

Your website iframe should then use:

    <iframe src="TASS/game/index.html" width="100%" height="720"
            allow="autoplay; fullscreen" allowfullscreen></iframe>

IF IT STILL FAILS
-----------------
1. Open the local test URL or published game URL.
2. Press F12 and select the Console tab.
3. Refresh the page and wait for the crash.
4. Copy the first red error and the traceback that follows it.

The game has been statically checked for Python syntax. This package has not
been confirmed by a complete WebAssembly/browser play-through in this
build environment, so test it locally before replacing the live website copy.
