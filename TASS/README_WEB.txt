TOTALLY ACCURATE SPACEFLIGHT SIMULATOR
BROWSER / WEBSITE BUILD
=====================================

This package has been prepared for Pygbag, which packages the Pygame-CE
project so it can run in modern browsers using WebAssembly.

WHAT HAS BEEN PREPARED
----------------------
- Converted the game stages and cutscenes to asynchronous functions.
- Added browser event-loop yields to each interactive frame loop.
- Converted game audio to OGG, the recommended browser-friendly format.
- Extracted the two animated explosion effects into PNG frame sequences.
  This removes the runtime Pillow dependency.
- Updated the Python dependency to pygame-ce.
- Deferred title-screen music until the first keyboard or mouse interaction
  so the browser's audio autoplay policy is respected.
- Added Windows and macOS/Linux build/test launchers.

The original uploaded ZIP is not changed. This is a separate web-ready copy.

REQUIREMENTS
------------
- Python 3.10 or newer is recommended.
- Internet access is required the first time Pygbag is installed and when
  Pygbag downloads its browser runtime during a build/test.
- A current Chrome, Edge, Firefox or Safari browser for testing.

INSTALL PYGBAG
--------------
Open Command Prompt or PowerShell in this package's main folder and run:

    python -m pip install --upgrade pygbag pygame-ce

On Windows, you can then double-click RUN_WEB_TEST.bat.
It starts the local server. Open this address in your browser:

    http://localhost:8000

The first launch can take noticeably longer because Pygbag downloads and
caches its browser runtime. Use the browser developer console if the game
fails to load; runtime errors are useful for diagnosing any remaining issue.

BUILD THE FILES FOR YOUR WEBSITE
-------------------------------
Double-click BUILD_FOR_WEB.bat, or run:

    python -m pygbag --build --title "Totally Accurate Spaceflight Simulator" Llama_Space_Programme

The generated website files will be in:

    Llama_Space_Programme/build/web/

Copy the CONTENTS of build/web (including index.html and all accompanying
folders/files) into a folder named game in your existing website repository.
For the current GitHub Pages website, that means the website repository will
look broadly like this:

    Website/
      index.html
      style.css
      game/
        index.html
        ...all other files from build/web...

Do not copy only index.html. The WebAssembly, Python runtime support and game
assets alongside it are required.

EMBED THE GAME IN A WEBSITE PAGE
--------------------------------
Add this iframe wherever you want the game to appear:

    <iframe
        src="game/index.html"
        title="Totally Accurate Spaceflight Simulator"
        width="100%"
        height="720"
        style="display:block; width:100%; aspect-ratio:16/9; border:0;"
        allow="autoplay; fullscreen; gamepad"
        allowfullscreen>
    </iframe>

The path is relative, so it works on a GitHub Pages project site under
/Website/ as well as when previewed locally from the same site structure.
You can put the iframe on a dedicated play.html page instead of the homepage.

After copying the files into your website repository, commit and push the
changes. GitHub Pages will publish the game alongside the rest of the site.
The public address will be your website URL followed by /game/.

IMPORTANT TESTING NOTES
-----------------------
- This is a compatibility preparation, not a claim that a full browser
  play-through has already passed. Run RUN_WEB_TEST.bat and test the game.
- Test the full sequence: title, opening cutscenes, shops, Blackjack, rocket
  flight, transition cutscene, and Mars exploration.
- Test keyboard and mouse input, music, sound effects, fullscreen, and the
  browser's back/refresh behaviour.
- The game is designed around a 1280 x 720 display and keyboard controls.
  Desktop browsers are the first target; mobile needs separate testing.
- Browser saving is not currently implemented. Game state is shared between
  stages during one play session, but restarting the page starts a fresh run.
- Keep the game folder and all generated web files together. Do not rename
  files inside build/web after building.
