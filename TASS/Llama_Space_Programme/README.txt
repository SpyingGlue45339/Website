LLAMA SPACE PROGRAMME - INTEGRATED VERSION
=========================================

RUNNING ON DESKTOP
------------------
1. Keep all files and asset folders together as they are in this package.
2. Install the required package:

       python -m pip install -r requirements.txt

3. Start the game:

       python main.py

The requirements file uses pygame-ce. It is imported in Python code using
`import pygame`, just like the original Pygame package.

DISPLAY
-------
The shared display is a fixed 1280 x 720 window. This matches the existing
shop, rocket-flight and Mars layouts, so every phase uses the same display.

GAME STRUCTURE
--------------
- main.py owns the Pygame lifecycle and runs the title screen and game stages.
- title.py contains the title screen.
- cutscene.py contains the animated story scenes.
- phase1.py contains the shops and inventory.
- gambling.py contains the Blackjack minigame.
- phase2.py contains rocket flight.
- phase3.py contains Mars exploration.
- global_variables.py stores resources shared between game stages.
- events.py contains the random Mars events.

BROWSER VERSION
---------------
This folder has also been adapted for Pygbag/WebAssembly:
- Interactive game stages are asynchronous and yield to the browser.
- Audio is stored in OGG format.
- Explosion animations use PNG frame sequences, so Pillow is not required.
- The title soundtrack waits for the first keyboard or mouse interaction.

See the separate README_WEB.txt in the parent folder for the exact Pygbag
commands and instructions for embedding the built game in a website.

CONTROLS
--------
The game is designed around a 1280 x 720 display and keyboard/mouse input.
The shops, Blackjack, rocket flight, cutscenes and Mars exploration all share
the same Pygame display and session resources.
