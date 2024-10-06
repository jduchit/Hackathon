import pygame

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)



# Sliders class
class Slider:
    def __init__(self, x, y, width, min_value, max_value, initial_value):
        self.rect = pygame.Rect(x, y, width, 10)  # Slider background
        self.handle = pygame.Rect(x + (initial_value - min_value) / (max_value - min_value) * width - 10, y - 5, 20, 20)  # Slider handle
        self.min_value = min_value
        self.max_value = max_value
        self.value = initial_value

    def draw(self, surface):
        # Draw slider background
        pygame.draw.rect(surface, BLUE, self.rect)
        # Draw slider handle
        pygame.draw.rect(surface, GREEN, self.handle)

    def update(self, mouse_pos, mouse_pressed):
        if mouse_pressed and self.rect.collidepoint(mouse_pos):
            # Move the handle with the mouse
            x_pos = mouse_pos[0]
            if x_pos < self.rect.left:
                x_pos = self.rect.left
            elif x_pos > self.rect.right:
                x_pos = self.rect.right
            self.handle.x = x_pos - 10  # Center the handle
            # Update value based on handle position
            self.value = self.min_value + (self.handle.x - self.rect.x) / self.rect.width * (self.max_value - self.min_value)

# Create sliders for radius and density
radius_slider = Slider(100, 100, 600, 10, 200, 100)  # Radius between 10 and 200
density_slider = Slider(100, 150, 600, 1, 10, 5)  # Density between 1 and 10

# Game variables
jump_height = 0
gravity = 0
on_ground = True
velocity_y = 0

# Rectangle properties
rectangle_width = 50
rectangle_height = 50
rectangle_x = screen_width // 2 - rectangle_width // 2
rectangle_y = screen_height // 2 - rectangle_height // 2

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and on_ground:  # Jump when space is pressed
                jump_height = radius_slider.value * 0.5  # Jump height influenced by radius
                velocity_y = -jump_height
                on_ground = False

    mouse_pressed = pygame.mouse.get_pressed()
    mouse_pos = pygame.mouse.get_pos()

    # Update sliders
    radius_slider.update(mouse_pos, mouse_pressed)
    density_slider.update(mouse_pos, mouse_pressed)

    # Physics calculations
    if not on_ground:
        # Apply gravity based on density
        gravity = density_slider.value * 0.1  # Gravity influenced by density
        velocity_y += gravity

        # Update rectangle position
        rectangle_y += velocity_y

        # Check if the rectangle hits the ground
        if rectangle_y >= screen_height - rectangle_height:
            rectangle_y = screen_height - rectangle_height  # Reset to ground level
            on_ground = True
            velocity_y = 0  # Reset velocity when on the ground
        else:
            on_ground = False

    # Fill the screen with white
    screen.fill(WHITE)

    # Draw sliders
    radius_slider.draw(screen)
    density_slider.draw(screen)

    # Display current values
    font = pygame.font.Font(None, 36)
    radius_text = font.render(f'Radius: {radius_slider.value:.2f}', True, (0, 0, 0))
    density_text = font.render(f'Density: {density_slider.value:.2f}', True, (0, 0, 0))
    screen.blit(radius_text, (100, 60))
    screen.blit(density_text, (100, 160))

    # Draw the rectangle
    pygame.draw.rect(screen, (0, 0, 255), (rectangle_x, rectangle_y, rectangle_width, rectangle_height))

    # Update the display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
