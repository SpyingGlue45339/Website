import pygame
import engine


def Update(
    gameState,
    currentPlayer,
    aiMoveTime,
    gameOver,
    winner
):

    if gameState=="GAME":

        if not gameOver and currentPlayer==1:

            if len(engine.FindAllMoves(1))==0:

                winner="AI Wins!"
                gameOver=True

        if not gameOver and currentPlayer==2:

            if pygame.time.get_ticks()>=aiMoveTime:

                if engine.AI(2)==False:

                    winner="You Win!"
                    gameOver=True

                else:

                    currentPlayer=1

    return (
        currentPlayer,
        aiMoveTime,
        gameOver,
        winner
    )