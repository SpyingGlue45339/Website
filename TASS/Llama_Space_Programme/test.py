
number_of_rows = 10
number_of_columns = 10
def generate_biomes():
    map = []
    for x in range(number_of_columns):
        new_column = []
        for y in range(number_of_rows):
            new_column.append("Rocky Plains")
        map.append(new_column)
        
    middle_x_start = (number_of_columns - 2) // 2
    middle_y_start = (number_of_rows - 2) // 2
    # corrr snazzy operator
    volcano_start_y = (number_of_rows - 4) // 2

    map[middle_x_start][middle_y_start] = "Crater"
    map[middle_x_start+1][middle_y_start] = "Crater"
    map[middle_x_start][middle_y_start+1] = "Crater"
    map[middle_x_start+1][middle_y_start+1] = "Crater"
    
    map[middle_x_start][number_of_rows-1] = "Water"
    map[middle_x_start+1][number_of_rows-1] = "Water"
    
    map[number_of_columns -1][middle_y_start] = "Volcano"
    map[number_of_columns -1][middle_y_start+1] = "Volcano"
    map[number_of_columns -2][middle_y_start] = "Volcano"
    map[number_of_columns -2][middle_y_start+1] = "Volcano"
    
    map[middle_x_start][0] = "Desert"
    map[middle_x_start+1][0] = "Desert"
    map[middle_x_start-1][0] = "Desert"
    map[middle_x_start-1][1] = "Desert"
    map[middle_x_start-2][0] = "Desert"
    
    return map
    
    
















# Optional debugging visualiser. It reuses a screen created by main.py.
import pygame

CELL_SIZE = 60

# Biome colours
BIOME_COLOURS = {
    "Rocky Plains": (130, 130, 130),
    "Volcano": (220, 70, 30),
    "Desert": (30, 140, 60),
    "Water": (40, 100, 220)
}

def visualise_map(map_data, screen):
    """Preview a biome grid on an existing Pygame display surface."""
    running = True
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 20)
    width, height = screen.get_size()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((30, 30, 30))

        # Draw map
        for x in range(len(map_data)):
            for y in range(len(map_data[x])):

                biome = map_data[x][y]
                colour = BIOME_COLOURS.get(biome, (255, 0, 255))

                # Convert Cartesian Y to screen Y
                screen_x = x * CELL_SIZE
                screen_y = height - (y + 1) * CELL_SIZE

                pygame.draw.rect(
                    screen,
                    colour,
                    (screen_x, screen_y, CELL_SIZE, CELL_SIZE)
                )

                pygame.draw.rect(
                    screen,
                    (0, 0, 0),
                    (screen_x, screen_y, CELL_SIZE, CELL_SIZE),
                    1
                )

                # Display coordinates
                label = font.render(f"{x},{y}", True, (255, 255, 255))
                screen.blit(label, (screen_x + 5, screen_y + 5))

        # Display hovered coordinate
        mouse_x, mouse_y = pygame.mouse.get_pos()

        hover_x = mouse_x // CELL_SIZE
        hover_y = len(map_data[0]) - 1 - (mouse_y // CELL_SIZE)

        if 0 <= hover_x < len(map_data) and 0 <= hover_y < len(map_data[0]):
            text = font.render(
                f"Coordinate: ({hover_x}, {hover_y})",
                True,
                (255, 255, 255)
            )
            pygame.display.set_caption(
                f"Biome Map - {map_data[hover_x][hover_y]} - ({hover_x}, {hover_y})"
            )

        pygame.display.flip()
        clock.tick(60)

    return True
