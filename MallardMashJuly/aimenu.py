

import pygame
import engine
import widgets

currentAI = 0

BLACK=(20,20,20)
WHITE=(248,248,243)
PANEL=(246,246,246)
BLUE=(70,130,220)
GOLD=(255,210,60)

previousRect = pygame.Rect(90, 470, 140, 60)

playRect = pygame.Rect(330, 470, 140, 60)

nextRect = pygame.Rect(570, 470, 140, 60)
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
    global AIs
    AIs=[

    {
        "name":"Greedy \nGary",
        "difficulty":"Easy",
        "description":[
            "Gary always looks",
            "for the move that",
            "gives him the most",
            "options next turn."
        ]
    },

    {
        "name":"Vindictive \nVelma",
        "difficulty":"Easy",
        "description":[
            "Velma would rather",
            "stop you playing",
            "than improve her",
            "own position."
        ]
    },

    {
        "name":"Territorial \nTerrance",
        "difficulty":"Medium",
        "description":[
            "Terrance loves",
            "wide open spaces.",
            "He races to claim",
            "new territory."
        ]
    },

    {
        "name":"Optimised \nOctavia",
        "difficulty":"Hard",
        "description":[
            "Octavia weighs",
            "every move against",
            "both players before",
            "making her choice."
        ]
    },

    {
        "name":"Collaborative \nCuthbert",
        "difficulty":"Hard",
        "description":[
            "Cuthbert believes",
            "sharing beaks is",
            "the key to success.",
            "Usually."
        ]
    },

    {
        "name":"Bottleneck \nBarry",
        "difficulty":"Hard",
        "description":[
            "Barry blocks",
            "important routes",
            "and squeezes the",
            "board shut."
        ]
    },

    {
        "name":"Bartholomew",
        "difficulty":"Expert",
        "description":[
            "Nobody really",
            "understands what",
            "Bartholomew is",
            "thinking..."
        ]
    }

    ]
    global currentAI

    widgets.DrawBackground(screen)

    ai = AIs[engine.selectedAI]
    pixel = "assets/fonts/pixel.ttf"

    titleFont = pygame.font.Font(
        pixel,
        28
    )

    textFont = pygame.font.Font(
        pixel,
        14
    )

    smallFont = pygame.font.Font(
        pixel,
        12
    )

    # ==========================================
    # Wooden Board
    # ==========================================

    board = pygame.transform.scale(
        widgets.infoBox,
        (744,360)
    )

    boardRect = board.get_rect(
        center=(400,190)
    )

    screen.blit(
        board,
        boardRect
    )

    # ==========================================
    # Content Area
    # ==========================================
    
    contentX = boardRect.x + 90
    contentY = boardRect.y + 60

    portraitRect = pygame.Rect(
        contentX,
        contentY,
        170,
        220
    )

    textX = boardRect.x + 285

    # ==========================================
    # Portrait Placeholder
    # ==========================================

    pygame.draw.rect(
        screen,
        (210,210,210),
        portraitRect,
        border_radius=12
    )

    placeholder = smallFont.render(
        "Portrait",
        True,
        (120,120,120)
    )

    screen.blit(
        placeholder,
        placeholder.get_rect(
            center=portraitRect.center
        )
    )

    # ==========================================
    # AI Name
    # ==========================================

    shadow = titleFont.render(
        ai["name"],
        True,
        (70,40,20)
    )

    text = titleFont.render(
        ai["name"],
        True,
        (245,225,170)
    )

    nameY = contentY + 5

    screen.blit(
        shadow,
        (textX+2,nameY+2)
    )

    screen.blit(
        text,
        (textX,nameY)
    )

    # ==========================================
    # Difficulty
    # ==========================================

    difficulty = smallFont.render(
        "Difficulty: " + ai["difficulty"],
        True,
        (240,220,170)
    )

    screen.blit(
        difficulty,
        (textX,nameY+70)
    )

    # ==========================================
    # Description
    # ==========================================

    y = nameY + 95
    for line in ai["description"]:

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
            (textX+2,y+2)
        )

        screen.blit(
            text,
            (textX,y)
        )

        y += 34

    # ==========================================
    # Progress Dots
    # ==========================================

    startX = 280

    for i in range(len(AIs)):

        colour = (130,190,255)

        if i == currentAI:
            colour = (40,120,220)

        pygame.draw.circle(
            screen,
            colour,
            (
                startX+i*40,
                420
            ),
            8
        )

    # ==========================================
    # Buttons
    # ==========================================

    widgets.DrawButton(
        screen,
        previousRect,
        "<"
    )

    widgets.DrawButton(
        screen,
        playRect,
        "Play"
    )

    widgets.DrawButton(
        screen,
        nextRect,
        ">"
    )

def HandleAIClick(event):

    if previousRect.collidepoint(event.pos):
        return "PREVIOUS"

    if nextRect.collidepoint(event.pos):
        return "NEXT"

    if playRect.collidepoint(event.pos):
        return "PLAY"

    return None