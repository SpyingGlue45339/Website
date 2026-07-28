import pygame
import asyncio

import engine
import menus
import mainmenu
import events
import logic
import draw
import audio
print("Main started")

pygame.init()

pygame.mixer.init()

pygame.mixer.music.load("assets/sounds/mainmenu.ogg")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

SQUARE = 60

BOARD_WIDTH = 9 * SQUARE
BOARD_HEIGHT = 9 * SQUARE

SIDEBAR = 260

WIDTH = BOARD_WIDTH + SIDEBAR
HEIGHT = BOARD_HEIGHT

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mallard Mash")

selectedX = None
selectedY = None

currentOrientation = 0
currentPlayer = 1

aiMoveTime = 0

gameState = "MAINMENU"

gameOver = False
winner = ""

engine.ResetBoard(engine.selectedMap)

running = True


async def main():

    global running
    global gameState
    global currentPlayer
    global currentOrientation
    global selectedX
    global selectedY
    global gameOver
    global winner
    global aiMoveTime

    running = True

    while running:

        (
            gameState,
            selectedX,
            selectedY,
            currentOrientation,
            currentPlayer,
            aiMoveTime,
            gameOver,
            winner,
            running
        ) = events.HandleEvents(
            gameState,
            selectedX,
            selectedY,
            currentOrientation,
            currentPlayer,
            aiMoveTime,
            gameOver,
            winner,
            running,
            SQUARE
        )

        (
            currentPlayer,
            aiMoveTime,
            gameOver,
            winner
        ) = logic.Update(
            gameState,
            currentPlayer,
            aiMoveTime,
            gameOver,
            winner
        )
        
        draw.Draw(
            screen,
            gameState,
            selectedX,
            selectedY,
            currentOrientation,
            currentPlayer,
            gameOver,
            winner,
            SQUARE
        )

        pygame.display.flip()

        await asyncio.sleep(0)


asyncio.run(main())

