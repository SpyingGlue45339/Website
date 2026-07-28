import pygame

import engine
import mapmenu
import aimenu
import mainmenu
import rules
import audio

pygame.mixer.init()

def HandleEvents(
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
):

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # ==========================
        # MAIN MENU
        # ==========================

        if gameState == "MAINMENU":

            if event.type == pygame.MOUSEBUTTONDOWN:

                action = mainmenu.HandleMainMenuClick()

                if action == "PLAY":
                    audio.buttonClick.play()
                    selectedX = None
                    selectedY = None

                    currentOrientation = 0
                    currentPlayer = 1

                    gameOver = False
                    winner = ""
                    aiMoveTime = 0

                    gameState = "MAPSELECT"

                    pygame.event.clear()
                elif action=="RULES":
                    audio.buttonClick.play()
                    gameState="RULES"

                elif action == "QUIT":
                    audio.buttonClick.play()
                    running = False

            continue
        # ==========================
        # RULES
        # ==========================

        if gameState=="RULES":

            if event.type==pygame.MOUSEBUTTONDOWN:

                action=rules.HandleRulesClick(event)

                if action=="BACK":

                    gameState="MAINMENU"
                    audio.buttonClick.play()

            continue
        # ==========================
        # MAP SELECT
        # ==========================

        if gameState == "MAPSELECT":

            if event.type == pygame.MOUSEBUTTONDOWN:
                audio.buttonClick.play()
                print("Map menu clicked")

                choice = mapmenu.HandleMapClick(event)

                if choice != None:

                    engine.selectedMap = choice

                    engine.ResetBoard(engine.selectedMap)

                    selectedX = None
                    selectedY = None

                    currentOrientation = 0
                    currentPlayer = 1

                    gameOver = False
                    winner = ""
                    aiMoveTime = 0

                    gameState = "AISELECT"

            continue

        # ==========================
        # AI SELECT
        # ==========================

        if gameState == "AISELECT":

            if event.type == pygame.MOUSEBUTTONDOWN:

                audio.buttonClick.play()

                choice = aimenu.HandleAIClick(event)

                if choice == "PREVIOUS":

                    engine.selectedAI = (
                        engine.selectedAI - 1
                    ) % len(aimenu.AIs)

                elif choice == "NEXT":

                    engine.selectedAI = (
                        engine.selectedAI + 1
                    ) % len(aimenu.AIs)

                elif choice == "PLAY":

                    engine.ResetBoard(engine.selectedMap)

                    selectedX = None
                    selectedY = None

                    currentOrientation = 0
                    currentPlayer = 1

                    gameOver = False
                    winner = ""
                    aiMoveTime = 0

                    gameState = "GAME"

                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("assets/sounds/ingame.ogg")
                    pygame.mixer.music.set_volume(0.3)
                    pygame.mixer.music.play(-1)

            continue

        # ==========================
        # GAME
        # ==========================

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_r and not gameOver:
                audio.rotateDuck.play()
                currentOrientation = (currentOrientation + 1) % 8

            elif event.key == pygame.K_n:

                engine.ResetBoard(engine.selectedMap)

                selectedX = None
                selectedY = None

                currentOrientation = 0
                currentPlayer = 1

                winner = ""
                gameOver = False
                aiMoveTime = 0

        elif event.type == pygame.MOUSEBUTTONDOWN:

            if gameOver:
                continue
                

            if currentPlayer != 1:
                continue

            mx, my = pygame.mouse.get_pos()

            x = mx // SQUARE
            y = my // SQUARE

            if not engine.SquareExists(x, y):
                continue

            if event.button == 1:

                selectedX = x
                selectedY = y

            elif event.button == 3:

                if selectedX != None:

                    if engine.CheckMove(
                        selectedX,
                        selectedY,
                        currentOrientation,
                        currentPlayer
                    ):

                        engine.PlaceDuck(
                            selectedX,
                            selectedY,
                            currentOrientation,
                            currentPlayer
                        )
                        audio.duckPlace.play()

                        selectedX = None
                        selectedY = None

                        currentPlayer = 2
                        aiMoveTime = pygame.time.get_ticks() + 1000
    return (
        gameState,
        selectedX,
        selectedY,
        currentOrientation,
        currentPlayer,
        aiMoveTime,
        gameOver,
        winner,
        running
    )