import game
import mainmenu
import mapmenu
import aimenu
import rules

def Draw(
    screen,
    gameState,
    selectedX,
    selectedY,
    currentOrientation,
    currentPlayer,
    gameOver,
    winner,
    SQUARE
):

    if gameState == "MAINMENU":

        mainmenu.DrawMainMenu(screen)

    elif gameState == "MAPSELECT":

        mapmenu.DrawMapMenu(screen)

    elif gameState == "RULES":

        rules.DrawRules(screen)

    elif gameState == "AISELECT":

        aimenu.DrawAIMenu(screen)

    elif gameState == "GAME":

        game.DrawGame(
            screen,
            selectedX,
            selectedY,
            currentOrientation,
            currentPlayer,
            gameOver,
            winner,
            SQUARE
        )