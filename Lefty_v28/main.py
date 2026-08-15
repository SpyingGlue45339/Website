import asyncio
import pygame

from title import run as title_screen
from quiz_flow import run as quiz_flow
from audio import initialise as initialise_audio

WIDTH, HEIGHT = 1200, 760


async def main():
    pygame.init()
    initialise_audio()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Lefty Simulator")

    if await title_screen(screen) == "quit":
        pygame.quit()
        return

    while True:
        result = await quiz_flow(screen)

        if result == "quit" or result is None:
            break

        if result == "again":
            await asyncio.sleep(0)
            continue

        break

    pygame.quit()


if __name__ == "__main__":
    asyncio.run(main())