# widgets.py

import pygame

TEXT=(75,45,20)

buttonImage=pygame.image.load(
    "assets/images/buttontiny.png"
)

buttonImage=pygame.transform.scale(
    buttonImage,
    (300,70)
)



def GetButtonImage(rect):

    mx,my = pygame.mouse.get_pos()

    width = rect.width
    height = rect.height

    if rect.collidepoint(mx,my):

        width = int(width * 1.05)
        height = int(height * 1.05)

    image = pygame.transform.scale(
        buttonImage,
        (width, height)
    )

    drawRect = image.get_rect(
        center=rect.center
    )

    return image, drawRect

def DrawButtonImage(screen,image,rect):

    screen.blit(image,rect)
    
def DrawButtonText(screen,text,rect):

    buttonFont = pygame.font.Font(
    "assets/fonts/pixel.ttf",
    24
    )
    shadow=buttonFont.render(
        text,
        True,
        (40,20,10)
    )

    label=buttonFont.render(
        text,
        True,
        (215,185,120)
    )

    labelRect=label.get_rect(center=rect.center)
    screen.blit(
    shadow,
    (
        labelRect.x+2,
        labelRect.y+2
    )
)

    screen.blit(
        label,
        labelRect
    )
    screen.blit(label,labelRect)
    
def DrawButton(screen,rect,text):

    image,drawRect=GetButtonImage(rect)

    DrawButtonImage(
        screen,
        image,
        drawRect
    )

    DrawButtonText(
        screen,
        text,
        drawRect
    )
    
def ButtonPressed(rect):

    mx,my=pygame.mouse.get_pos()

    return rect.collidepoint(mx,my)


background = pygame.image.load(
    "assets/images/menu_background.png"
)

background = pygame.transform.scale(
    background,
    (800,560)
)
def DrawBackground(screen):

    screen.blit(background,(0,0))

    overlay = pygame.Surface(screen.get_size())
    overlay.set_alpha(60)
    overlay.fill((0,0,0))

    screen.blit(overlay,(0,0))
    
infoBox = pygame.image.load(
    "assets/images/box.png"
)
def DrawInfoBox(
    screen,
    rect,
    title,
    subtitle,
    lines
):

    titleFont = pygame.font.SysFont(None,50)
    subtitleFont = pygame.font.SysFont(None,28)
    textFont = pygame.font.SysFont(None,30)

    image = pygame.transform.scale(
        infoBox,
        (rect.width,rect.height)
    )

    screen.blit(image,rect)

    # --------------------------
    # Title
    # --------------------------

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

    screen.blit(
        shadow,
        (rect.x+32,rect.y+32)
    )

    screen.blit(
        text,
        (rect.x+30,rect.y+30)
    )

    # --------------------------
    # Subtitle
    # --------------------------

    if subtitle!="":

        shadow = subtitleFont.render(
            subtitle,
            True,
            (70,40,20)
        )

        text = subtitleFont.render(
            subtitle,
            True,
            (225,200,145)
        )

        screen.blit(
            shadow,
            (rect.x+32,rect.y+78)
        )

        screen.blit(
            text,
            (rect.x+30,rect.y+76)
        )

        y = rect.y+125

    else:

        y = rect.y+95

    # --------------------------
    # Body
    # --------------------------

    for line in lines:

        shadow = textFont.render(
            line,
            True,
            (70,40,20)
        )

        text = textFont.render(
            line,
            True,
            (245,235,185)
        )

        screen.blit(
            shadow,
            (rect.x+32,y+2)
        )

        screen.blit(
            text,
            (rect.x+30,y)
        )

        y += 36