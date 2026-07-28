import pygame
import widgets

WHITE=(255,255,255)
BLACK=(0,0,0)
GREY=(200,200,200)
LIGHTGREY=(230,230,230)

playRect=pygame.Rect(250,220,300,70)
rulesRect=pygame.Rect(250,310,300,70)
quitRect=pygame.Rect(250,400,300,70)
titleImage = pygame.image.load(
    "assets/images/title.png"
)


def DrawMainMenu(screen):

    background = pygame.image.load(
        "assets/images/menu_background.png"
    ).convert()

    background = pygame.transform.scale(
        background,
        (800,560)
    )

    screen.blit(background,(0,0))

    overlay = pygame.Surface(screen.get_size())
    overlay.set_alpha(60)
    overlay.fill((0,0,0))

    screen.blit(overlay,(0,0))

    titleRect = titleImage.get_rect(center=(400,90))
    screen.blit(titleImage,titleRect)

    widgets.DrawButton(
        screen,
        playRect,
        "Play"
    )

    widgets.DrawButton(
        screen,
        rulesRect,
        "Rules"
    )

    widgets.DrawButton(
        screen,
        quitRect,
        "Quit"
    )

def HandleMainMenuClick():

    mx,my=pygame.mouse.get_pos()

    if playRect.collidepoint(mx,my):
        return "PLAY"

    if rulesRect.collidepoint(mx,my):
        return "RULES"

    if quitRect.collidepoint(mx,my):
        return "QUIT"

    return None