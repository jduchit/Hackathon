import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Jump Simulation with Gravity')

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Clock for controlling frame rate
clock = pygame.time.Clock()
#todo: Calcular gravedad

#todo: Agregar

# Define player attributes
player_pos = [width // 2, height - 100]  # Starting position (middle of the screen)
player_size = 50                        # Size of the player
player_vel_y = 0                        # Initial velocity
gravity = 0.8                           # Gravity value
jump_strength = -15                     # Jump strength (negative to move upward)

# Variable to track if the player is on the ground
on_ground = True

# Game loop
running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Handle jump event
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and on_ground:
                player_vel_y = jump_strength  # Apply jump velocity
                on_ground = False

    # Apply gravity
    player_vel_y += gravity
    player_pos[1] += player_vel_y

    # Check if player hits the ground
    if player_pos[1] >= height - player_size:
        player_pos[1] = height - player_size
        player_vel_y = 0
        on_ground = True

    # Draw the player
    pygame.draw.rect(screen, BLUE, (player_pos[0], player_pos[1], player_size, player_size))

    # Update the display
    pygame.display.flip()

    # Frame rate
    clock.tick(60)
