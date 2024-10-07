import pygame
import math
import os
import cv2
import numpy as np
import camera
import cropface
from Data import model


# Initialize Pygame
pygame.init()

translations = {
    "English": {
        "English": "English",
        "Spanish": "Spanish",
        "French": "French",
        "German": "German",
        "Hindi": "Hindi",
        "Japanese": "Japanese",
        "Return": "Return",
        "Play": "Play",
        "Quit": "Quit",
        "Language": "Language",
        "Take New Image": "Take New Image",
        "Radius": "Radius",
        "Density": "Density",
        "Temperature": "Temperature",
        "Take Screenshoot": "Create Postcard",
        "Get Planet": "Get Planet"
    },
    "Spanish": {
        "English": "Inglés",
        "Spanish": "Español",
        "French": "Francés",
        "German": "Alemán",
        "Hindi": "Hindi",
        "Japanese": "Japonés",
        "Return": "Regresar",
        "Play": "Jugar",
        "Quit": "Salir",
        "Language": "Idioma",
        "Take New Image": "Tomar Nueva Imagen",
        "Radius": "Radio",
        "Density": "Densidad",
        "Temperature": "Temperatura",
        "Take Screenshoot": "Crear Postal",
        "Get Planet": "Obtener Planeta"
    },
    "French": {
        "English": "Anglais",
        "Spanish": "Espagnol",
        "French": "Français",
        "German": "Allemand",
        "Hindi": "Hindi",
        "Japanese": "Japonais",
        "Return": "Retour",
        "Play": "Jouer",
        "Quit": "Quitter",
        "Language": "Langue",
        "Take New Image": "Prendre une Nouvelle Image",
        "Radius": "Rayon",
        "Density": "Densité",
        "Temperature": "Température",
        "Take Screenshoot": "Créer une Carte Postale",
        "Get Planet": "Obtenir Planète"
    },
    "German": {
        "English": "Englisch",
        "Spanish": "Spanisch",
        "French": "Französisch",
        "German": "Deutsch",
        "Hindi": "Hindi",
        "Japanese": "Japanisch",
        "Return": "Zurück",
        "Play": "Spielen",
        "Quit": "Beenden",
        "Language": "Sprache",
        "Take New Image": "Neues Bild aufnehmen",
        "Radius": "Radius",
        "Density": "Dichte",
        "Temperature": "Temperatur",
        "Take Screenshoot": "Postkarte erstellen",
        "Get Planet": "Planet erhalten"
    }
}

# Initialize current language (default: English)
current_language = "English"

# Definitions
screen_width, screen_height = 1280, 720
dif_x = (1280 - 800) / 2
dif_y = (720 - 600) / 2
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('ExoAdventure')
clock = pygame.time.Clock()

# Get the directory of the current script
current_dir = os.path.dirname(__file__)

# Load background image
background_image = pygame.image.load(current_dir + '/resources/background/new_background.jpeg')
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Load flag images
english_flag = pygame.image.load(current_dir + '/resources/flags/Flag_of_United_States-128x67.png')
spanish_flag = pygame.image.load(current_dir + '/resources/flags/Flag_of_Spain-128x85.png')
french_flag = pygame.image.load(current_dir + '/resources/flags/Flag_of_France-128x85.png')
german_flag = pygame.image.load(current_dir + '/resources/flags/Flag_of_Germany-128x77.png')
hindi_flag = pygame.image.load(current_dir + '/resources/flags/Flag_of_India-128x85.png')
japanese_flag = pygame.image.load(current_dir + '/resources/flags/Flag_of_Japan-128x85.png')

# Adjust size of the flags if necessary
flag_size = (50, 30)  # Example size
english_flag = pygame.transform.scale(english_flag, flag_size)
spanish_flag = pygame.transform.scale(spanish_flag, flag_size)
french_flag = pygame.transform.scale(french_flag, flag_size)
german_flag = pygame.transform.scale(german_flag, flag_size)
hindi_flag = pygame.transform.scale(hindi_flag, flag_size)
japanese_flag = pygame.transform.scale(japanese_flag, flag_size)


# Function to create temperature overlay
def create_temperature_overlay(temperature, min_temp, max_temp):
    # Normalize temperature to 0-1 range
    t = (temperature - min_temp - 50) / (max_temp - min_temp)
    # Create color gradient from blue (cold) to red (hot)
    r = int(255 * t)
    b = int(255 * (1 - t))
    r = max(0, min(r, 255))
    b = max(0, min(b, 255))
    # Create a surface with alpha channel
    overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    overlay.fill((r, 0, b, 100))  # Semi-transparent overlay
    return overlay

def set_face(face_image):
    face_image = pygame.transform.scale(face_image, (37 * 1.2, 37 * 1.2))
    return face_image

# Function to capture and save a new face image
def capture_new_face_image():
    camera.capture_new_face_image()
    cropface.cropface()
    return True

def load_face_image():
    # Updated directory path
    save_dir = os.path.expanduser('~/.exoadventure')
    image_path = os.path.join(save_dir, 'cropped_face_with_transparent_bg.png')

    if not os.path.exists(image_path):
        print("Face image not found. Capturing new image...")
        if not capture_new_face_image():
            print("Failed to capture new image. Using default.")
            return None
    return image_path


# Add these functions outside the main game loop
def format_jump_height(height_meters):
    if height_meters < 1000:
        return f"{height_meters:.1f} m"
    else:
        return f"{height_meters/1000:.1f} km"

def update_jump_message(height_meters):
    return f"Jump height: {format_jump_height(height_meters)}"



# Load face image
face_image = pygame.image.load(load_face_image())
face_image = set_face(face_image)

# Load player image
player_image = pygame.image.load(current_dir + '/resources/character/astronaut.png')
player_image = pygame.transform.scale(player_image, (170 * 1.5, 170 * 1.5))

# Button class
class Button:
    def __init__(self, text, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.Font(None, 36)

    def draw(self, surface):
        pygame.draw.rect(surface, WHITE, self.rect)
        text_surface = self.font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

# Slider class
class Slider:
    def __init__(self, x, y, width, min_value, max_value, initial_value):
        self.rect = pygame.Rect(x, y, width, 10)
        initial_value = max(min_value, min(initial_value, max_value))
        handle_x = x + (initial_value - min_value) / (max_value - min_value) * width - 10
        self.handle = pygame.Rect(handle_x, y - 5, 20, 20)
        self.min_value = min_value
        self.max_value = max_value
        self.value = initial_value
        self.dragging = False

    def draw(self, surface):
        pygame.draw.rect(surface, BLUE, self.rect)
        pygame.draw.rect(surface, GREEN, self.handle)

    def update(self, mouse_pos, mouse_pressed):
        if mouse_pressed[0]:
            if self.rect.collidepoint(mouse_pos):
                self.dragging = True
        if self.dragging:
            x_pos = max(self.rect.left, min(mouse_pos[0], self.rect.right))
            self.handle.x = x_pos - self.handle.width // 2
            self.value = self.min_value + (self.handle.x - self.rect.x + self.handle.width // 2) / self.rect.width * (self.max_value - self.min_value)
            self.value = max(self.min_value, min(self.value, self.max_value))
        if not mouse_pressed[0]:
            self.dragging = False

# Create sliders with proper limits
radius_slider = Slider(600 + dif_x, 60 + dif_y, 120, 1, 17, 10)
density_slider = Slider(600 + dif_x, 140 + dif_y, 120, 0.30, 28, 5)
temperature_slider = Slider(600 + dif_x, 220 + dif_y, 120, -67, 2456, 1000)

# Game states
HOME_SCREEN = 0
GAME_SCREEN = 1
LANGUAGE_SCREEN = 2
current_state = HOME_SCREEN

# Scaling factors
pixels_per_meter = 100  # Adjust this value as needed for proper scaling

# Load player image to get character height
character_height_pixels = player_image.get_height()

# Game variables
is_jumping = False
y_position_meters = 0  # Starting at ground level
y_velocity = 0  # m/s
G = 6.67430e-11  # Gravitational constant in m^3 kg^-1 s^-2
initial_jump_velocity = 5  # m/s, adjust as needed

jump_message = ""  # Initialize jump message

# Main game loop
running = True
while running:
    mouse_pressed = pygame.mouse.get_pressed()
    mouse_pos = pygame.mouse.get_pos()

    # Create buttons
    play_button = Button(translations[current_language]["Play"], 300 + dif_x, 200 + dif_y, 200, 50)
    language_button = Button(translations[current_language]["Language"], 300 + dif_x, 300 + dif_y, 200, 50)
    quit_button = Button(translations[current_language]["Quit"], 300 + dif_x, 400 + dif_y, 200, 50)
    return_button = Button(translations[current_language]["Return"], 10 + dif_x, 10 + dif_y, 100, 40)
    take_image_button = Button(translations[current_language]["Take New Image"], 150 + dif_x, 500 + dif_y, 500, 50)
    take_screenshoot_button = Button(translations[current_language]["Take Screenshoot"], 450 + dif_x, 600 + dif_y, 500, 50)
    get_planet_button = Button(translations[current_language]["Get Planet"], -150 + dif_x, 600 + dif_y, 500, 50)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if current_state == HOME_SCREEN:
                if play_button.is_clicked(mouse_pos):
                    current_state = GAME_SCREEN
                elif language_button.is_clicked(mouse_pos):
                    current_state = LANGUAGE_SCREEN
                elif quit_button.is_clicked(mouse_pos):
                    running = False
                elif take_image_button.is_clicked(mouse_pos):
                    if capture_new_face_image():
                        face_image = pygame.image.load(load_face_image())
                        face_image = set_face(face_image)
                        print("New image captured and loaded successfully!")
                    else:
                        print("Failed to capture new image.")
            elif current_state == GAME_SCREEN:
                if return_button.is_clicked(mouse_pos):
                    current_state = HOME_SCREEN
                    is_jumping = False
                    y_position_meters = 0
                    y_velocity = 0
                    jump_message = ""
                elif get_planet_button.is_clicked(mouse_pos):
                    print(radius_slider.value, density_slider.value, temperature_slider.value)
                    planet_name = model.getPlanet(radius_slider.value, density_slider.value, temperature_slider.value, current_language.lower())
                    planet_name = planet_name.replace(" ", "")
                    background_image = pygame.image.load(current_dir + f'/resources/planetAI/{planet_name}.jpg')
                    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
            elif current_state == LANGUAGE_SCREEN:
                if return_button.is_clicked(mouse_pos):
                    current_state = HOME_SCREEN
                elif english_button.is_clicked(mouse_pos):
                    current_language = "English"
                elif spanish_button.is_clicked(mouse_pos):
                    current_language = "Spanish"
                elif french_button.is_clicked(mouse_pos):
                    current_language = "French"
                elif german_button.is_clicked(mouse_pos):
                    current_language = "German"
        if event.type == pygame.KEYDOWN and current_state == GAME_SCREEN:
            if event.key == pygame.K_SPACE and not is_jumping:
                y_velocity = initial_jump_velocity  # Positive value, upwards
                is_jumping = True

    screen.blit(background_image, (0, 0))

    if current_state == HOME_SCREEN:
        play_button.draw(screen)
        language_button.draw(screen)
        quit_button.draw(screen)
        take_image_button.draw(screen)
    elif current_state == GAME_SCREEN:
        # Time delta
        dt = clock.tick(60) / 1000.0  # Limit to 60 FPS, dt in seconds

        # Update planet properties
        radius = radius_slider.value * 6.371e6  # Earth's radius in meters
        density = density_slider.value * 1000    # Convert from g/cm3 to kg/m3

        # Calculate gravity
        gravedad = -(4 / 3) * math.pi * G * density * radius  # Negative because gravity pulls downward


        # Game logic
        if is_jumping:
            y_velocity += gravedad * dt
            y_position_meters += y_velocity * dt
            
            # Update jump message while in air
            jump_message = update_jump_message(y_position_meters)

            if y_position_meters <= 0:
                y_position_meters = 0
                is_jumping = False
                y_velocity = 0
                jump_message = "Ready to jump!"
        else:
            jump_message = "Press SPACE to jump!"

        # Create temperature overlay
        temperature_overlay = create_temperature_overlay(temperature_slider.value, temperature_slider.min_value, temperature_slider.max_value)
        screen.blit(temperature_overlay, (0, 0))

        # Update and draw sliders
        radius_slider.update(mouse_pos, mouse_pressed)
        density_slider.update(mouse_pos, mouse_pressed)
        temperature_slider.update(mouse_pos, mouse_pressed)

        radius_slider.draw(screen)
        density_slider.draw(screen)
        temperature_slider.draw(screen)

        # Draw player
        player_pos_x = 300 + dif_x
        y_position_pixels = screen_height - (y_position_meters * pixels_per_meter) - character_height_pixels
        screen.blit(face_image, (player_pos_x + 115, y_position_pixels + 19))
        screen.blit(player_image, (player_pos_x, y_position_pixels))

        # Display slider values
        font = pygame.font.Font(None, 16)
        radius_text = font.render(f'{translations[current_language]["Radius"]}: {radius_slider.value:.2f} x Earth\'s radius', True, WHITE)
        density_text = font.render(f'{translations[current_language]["Density"]}: {density_slider.value:.2f} g/cm³', True, WHITE)
        temperature_text = font.render(f'{translations[current_language]["Temperature"]}: {temperature_slider.value:.2f} °C', True, WHITE)
        screen.blit(radius_text, (625 + dif_x, 80 + dif_y))
        screen.blit(density_text, (625 + dif_x, 160 + dif_y))
        screen.blit(temperature_text, (625 + dif_x, 240 + dif_y))

        # Display jump message - position it at bottom left
        if (len(jump_message) > 0):
            font = pygame.font.Font(None, 36)  # Increased font size for better visibility
            message_surface = font.render(jump_message, True, WHITE)
            message_rect = message_surface.get_rect(bottomleft=(20 + dif_x, screen_height - 20))
            screen.blit(message_surface, message_rect)

        # Draw return button
        return_button.draw(screen)
        take_screenshoot_button.draw(screen)
        get_planet_button.draw(screen)
    elif current_state == LANGUAGE_SCREEN:
        english_button = Button(translations[current_language]["English"], 100 + dif_x, 200 + dif_y, 250, 50)
        spanish_button = Button(translations[current_language]["Spanish"], 100 + dif_x, 300 + dif_y, 250, 50)
        french_button = Button(translations[current_language]["French"], 500 + dif_x, 200 + dif_y, 250, 50)
        german_button = Button(translations[current_language]["German"], 500 + dif_x, 300 + dif_y, 250, 50)
        english_button.draw(screen)
        spanish_button.draw(screen)
        french_button.draw(screen)
        german_button.draw(screen)
        return_button.draw(screen)

        # Draw flags next to the buttons
        screen.blit(english_flag, (105 + dif_x, 210 + dif_y))
        screen.blit(spanish_flag, (105 + dif_x, 310 + dif_y))
        screen.blit(french_flag, (505 + dif_x, 210 + dif_y))
        screen.blit(german_flag, (505 + dif_x, 310 + dif_y))

    pygame.display.flip()
    # Remove clock.tick(60) here since it's already called above

pygame.quit()