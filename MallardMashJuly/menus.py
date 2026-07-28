import pygame

WHITE=(255,255,255)
BLACK=(0,0,0)
GREY=(200,200,200)
LIGHTGREY=(230,230,230)


aiRects=[]

for i in range(7):

    aiRects.append(
        pygame.Rect(
            170,
            110+i*60,
            460,
            50
        )
    )


def DrawAIMenu(screen):
    titleFont=pygame.font.SysFont(None,72)
    buttonFont=pygame.font.SysFont(None,48)
    screen.fill((180,220,255))

    title=titleFont.render("Choose Opponent",True,BLACK)
    screen.blit(title,(170,70))

    names=[
    "Gary",
    "Velma",
    "Terrance",
    "Octavia",
    "Cuthbert",
    "Barry",
    "Bartholomew"
    ]

    mx,my=pygame.mouse.get_pos()

    for i in range(7):

        rect=aiRects[i]

        if rect.collidepoint(mx,my):
            colour=LIGHTGREY
        else:
            colour=GREY

        pygame.draw.rect(
            screen,
            colour,
            rect,
            border_radius=12
        )

        text=buttonFont.render(names[i],True,BLACK)

        screen.blit(
            text,
            (
                rect.x+25,
                rect.y+10
            )
        )

def HandleAIClick(event):

    mx,my=event.pos

    print("Click:",mx,my)

    for i in range(len(aiRects)):

        rect=aiRects[i]

        print(rect)

        if rect.collidepoint(mx,my):


            return i



    return None