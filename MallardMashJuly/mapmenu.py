import pygame
import widgets

BLACK=(0,0,0)
GREY=(200,200,200)
LIGHTGREY=(230,230,230)

mapRects = [
    pygame.Rect(250,170,300,70),
    pygame.Rect(250,260,300,70),
    pygame.Rect(250,350,300,70)
]


def DrawMapMenu(screen):

    titleFont=pygame.font.SysFont(None,72)

    background=pygame.image.load(
        "assets/images/menu_background.png"
    ).convert()

    background=pygame.transform.scale(
        background,
        (800,560)
    )

    screen.blit(background,(0,0))

    overlay=pygame.Surface(screen.get_size())
    overlay.set_alpha(60)
    overlay.fill((0,0,0))

    screen.blit(overlay,(0,0))

    names=[
        "Classic",
        "River",
        "Plains"
    ]

    for i in range(len(mapRects)):

        widgets.DrawButton(
            screen,
            mapRects[i],
            names[i]
        )

def HandleMapClick(event):

    mx,my=event.pos

    for i in range(len(mapRects)):

        if mapRects[i].collidepoint(mx,my):
            return i

    return None