import pygame

def DrawRules(screen):

    screen.fill((170,220,255))

    WHITE=(248,248,243)
    BLACK=(25,25,25)
    BLUE=(70,130,220)
    GREY=(215,215,215)
    PANEL=(246,246,246)

    BODY=(255,230,100)
    BEAK=(255,150,0)

    titleFont=pygame.font.SysFont(None,56)
    headingFont=pygame.font.SysFont("Georgia",24,bold=True)
    latinFont=pygame.font.SysFont("Georgia",18,italic=True)
    labelFont=pygame.font.SysFont(None,24)
    smallFont=pygame.font.SysFont(None,20)

    # =====================================================
    # Background
    # =====================================================

    pygame.draw.rect(
        screen,
        WHITE,
        (20,20,760,520),
        border_radius=22
    )

    # =====================================================
    # Title
    # =====================================================

    title=titleFont.render(
        "Duck Academy",
        True,
        BLUE
    )

    screen.blit(title,(235,18))

    # =====================================================
    # Main Anatomy Panel
    # =====================================================

    pygame.draw.rect(
        screen,
        PANEL,
        (40,90,545,390),
        border_radius=18
    )

    heading=headingFont.render(
        "Anatomy of a Duck",
        True,
        BLACK
    )

    screen.blit(
        heading,
        (80,118)
    )

    latin=latinFont.render(
        "Anas platyrhynchos",
        True,
        (120,120,120)
    )

    screen.blit(
        latin,
        (82,148)
    )

    # =====================================================
    # Duck
    # =====================================================

    square=82
    duck=[
        (2,1),
        (1,1),
        (1,0),
        (0,0)
    ]

    startX=330
    startY=170

    for i,(dx,dy) in enumerate(duck):

        colour=BEAK if i==0 else BODY

        pygame.draw.rect(
            screen,
            colour,
            (
                startX+dx*square,
                startY+dy*square,
                square-8,
                square-8
            ),
            border_radius=16
        )
    # =====================================================
    # Labels
    # =====================================================

    pygame.draw.line(
        screen,
        BLACK,
        (535,210),
        (610,210),
        2
    )

    screen.blit(
        labelFont.render(
            "Beak",
            True,
            BLACK
        ),
        (620,198)
    )

    pygame.draw.line(
        screen,
        BLACK,
        (455,330),
        (610,330),
        2
    )

    screen.blit(
        labelFont.render(
            "Body",
            True,
            BLACK
        ),
        (620,318)
    )

    # =====================================================
    # Professor Quackers
    # =====================================================

    pygame.draw.rect(
        screen,
        PANEL,
        (610,90,140,390),
        border_radius=18
    )

    pygame.draw.rect(
        screen,
        GREY,
        (625,110,110,120),
        border_radius=12
    )

    pygame.draw.rect(
        screen,
        BLACK,
        (625,110,110,120),
        2,
        border_radius=12
    )

    portrait=smallFont.render(
        "Portrait",
        True,
        (140,140,140)
    )

    screen.blit(
        portrait,
        (646,165)
    )

    name=labelFont.render(
        "Professor",
        True,
        BLACK
    )

    screen.blit(
        name,
        (620,255)
    )

    name=labelFont.render(
        "Quackers",
        True,
        BLACK
    )

    screen.blit(
        name,
        (625,282)
    )

    quote=smallFont.render(
        "\"Welcome!\"",
        True,
        (90,90,90)
    )

    screen.blit(
        quote,
        (632,330)
    )

    quote=smallFont.render(
        "\"Let's begin.\"",
        True,
        (90,90,90)
    )

    screen.blit(
        quote,
        (622,355)
    )

    # =====================================================
    # Progress
    # =====================================================

    for i in range(5):

        colour=(155,205,255)

        if i==0:
            colour=(45,120,220)

        pygame.draw.circle(
            screen,
            colour,
            (315+i*42,505),
            9
        )

    # =====================================================
    # Next Button
    # =====================================================

    nextRect=pygame.Rect(
        595,
        485,
        145,
        40
    )

    mx,my=pygame.mouse.get_pos()

    if nextRect.collidepoint(mx,my):
        colour=(230,230,230)
    else:
        colour=GREY

    pygame.draw.rect(
        screen,
        colour,
        nextRect,
        border_radius=10
    )

    nextText=labelFont.render(
        "Next  >",
        True,
        BLACK
    )

    screen.blit(
        nextText,
        (618,493)
    )
    
def HandleRulesClick(event):

    nextRect=pygame.Rect(555,445,180,55)

    if nextRect.collidepoint(event.pos):
        return "NEXT"

    return None