# game.py

import pygame
import engine
import widgets


def DrawGame(
    screen,
    selectedX,
    selectedY,
    currentOrientation,
    currentPlayer,
    gameOver,
    winner,
    SQUARE
):

    widgets.DrawBackground(screen)

    DrawBoard(screen,SQUARE)

    DrawGhostDuck(
        screen,
        selectedX,
        selectedY,
        currentOrientation,
        currentPlayer,
        gameOver,
        SQUARE
    )

    DrawSidePanel(
        screen,
        currentPlayer,
        gameOver,
        winner
    )

def DrawBoard(screen,SQUARE):

    for y in range(9):
        for x in range(9):

            value = engine.board[y][x]

            if value == engine.INVALID:
                colour = (90,90,90)

            elif value == engine.EMPTY:
                colour = (255,255,255)

            elif value == engine.PLAYER1BODY:
                colour = (255,230,100)

            elif value == engine.PLAYER1BEAK:
                colour = (255,150,0)

            elif value == engine.PLAYER2BODY:
                colour = (120,200,255)

            elif value == engine.PLAYER2BEAK:
                colour = (30,90,200)

            pygame.draw.rect(
                screen,
                colour,
                (
                    x*SQUARE+2,
                    y*SQUARE+2,
                    SQUARE-4,
                    SQUARE-4
                ),
                border_radius=8
            )
def DrawGhostDuck(
    screen,
    selectedX,
    selectedY,
    currentOrientation,
    currentPlayer,
    gameOver,
    SQUARE
):

    if (
        selectedX is None
        or currentPlayer != 1
        or gameOver
    ):
        return

    legal = engine.CheckMove(
        selectedX,
        selectedY,
        currentOrientation,
        currentPlayer
    )

    if legal:

        bodyColour = (170,255,170)
        beakColour = (0,200,0)

    else:

        bodyColour = (255,170,170)
        beakColour = (220,0,0)

    for i,(dx,dy) in enumerate(
        engine.duckOrientations[currentOrientation]
    ):

        xx = selectedX + dx
        yy = selectedY + dy

        if engine.SquareExists(xx,yy):

            colour = beakColour if i==0 else bodyColour

            pygame.draw.rect(
                screen,
                colour,
                (
                    xx*SQUARE+10,
                    yy*SQUARE+10,
                    SQUARE-20,
                    SQUARE-20
                ),
                border_radius=12
            )

def DrawSidePanel(
    screen,
    currentPlayer,
    gameOver,
    winner
):

    board = pygame.transform.scale(
        widgets.infoBox,
        (250,500)
    )

    panelRect = board.get_rect(
        topleft=(540,20)
    )

    screen.blit(
        board,
        panelRect
    )

    titleFont = pygame.font.Font(
        "assets/fonts/pixel.ttf",
        24
    )

    textFont = pygame.font.Font(
        "assets/fonts/pixel.ttf",
        18
    )

    if gameOver:

        title = winner

    elif currentPlayer == 1:

        title = "Your Turn"

    else:

        title = "AI Thinking..."

    shadow = titleFont.render(
        title,
        True,
        (70,40,20)
    )

    text = titleFont.render(
        title,
        True,
        (245,225,170)
    )

    screen.blit(shadow,(565,45))
    screen.blit(text,(563,43))

    # Portrait placeholder

    pygame.draw.rect(
        screen,
        (210,210,210),
        (565,90,200,180),
        border_radius=12
    )