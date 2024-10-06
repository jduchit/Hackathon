import pygame
import math
import os
import cv2
import numpy as np
import camera
import cropface


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
        "Take Screenshoot": "Take Screenshoot"
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
        "Take Screenshoot": "Tomar Captura de Pantalla"
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
        "Take Screenshoot": "Prendre une Capture d'Écran"
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
        "Take Screenshoot": "Screenshot aufnehmen"
    }
}

# Initialize current language (default: English)
current_language = "English"

# Definitions
screen_width, screen_height = 1280, 720
#Antes 800 y 600
dif_x = (1280 - 800)/2
dif_y = (720 - 600)/2
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('ExoAdventure')
clock = pygame.time.Clock()

# Load background image
background_image = pygame.image.load('resources/background/new_background.jpeg')
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Load flag images (assuming they are stored in the same directory as the script)
english_flag = pygame.image.load('resources/flags/Flag_of_United_States-128x67.png')
spanish_flag = pygame.image.load('resources/flags/Flag_of_Spain-128x85.png')
french_flag = pygame.image.load('resources/flags/Flag_of_France-128x85.png')
german_flag = pygame.image.load('resources/flags/Flag_of_Germany-128x77.png')
hindi_flag = pygame.image.load('resources/flags/Flag_of_India-128x85.png')
japanese_flag = pygame.image.load('resources/flags/Flag_of_Japan-128x85.png')

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
    if (r < 0):
        r = 0
    if (b < 0):
        b = 0
    if (r > 255):
        r = 255
    if (b > 255):    
        b = 255
    
    # Create a surface with alpha channel
    overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    overlay.fill((r, 0, b, 100))  # Semi-transparent overlay
    
    return overlay


def set_face(face_image):
    face_image = pygame.transform.scale(face_image, (37*1.2, 37*1.2))
    return face_image

# Function to capture and save a new face image
def capture_new_face_image():
    camera.capture_new_face_image()
    cropface.cropface()
    return True

# Load or capture face image
def load_face_image():
    if not os.path.exists('resources/character/cropped_face_with_transparent_bg.png'):
        print("Face image not found. Capturing new image...")
        if not capture_new_face_image():
            print("Failed to capture new image. Using default.")
            return None
    return 'resources/character/cropped_face_with_transparent_bg.png'

# Load face image
face_image = pygame.image.load(load_face_image())
face_image = set_face(face_image)

# Load player image
player_image = pygame.image.load('resources/character/astronaut.png')
player_image = pygame.transform.scale(player_image, (170*1.5, 170*1.5))

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
        self.handle = pygame.Rect(x + (initial_value - min_value) / (max_value - min_value) * width - 10, y - 5, 20, 20)
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
            self.handle.x = x_pos - 10
            self.value = self.min_value + (self.handle.x - self.rect.x) / self.rect.width * (self.max_value - self.min_value)
        if not mouse_pressed[0]:
            self.dragging = False


#Multiplu radious by earth
# Create sliders
radius_slider = Slider(600 + dif_x, 60 + dif_y, 120, 1, 17, 10)
density_slider = Slider(600 + dif_x, 140 + dif_y, 120, 0.30, 28, 5)
temperature_slider = Slider(600 + dif_x, 220 + dif_y, 120, -67, 2456, 1000)

# Game states
HOME_SCREEN = 0
GAME_SCREEN = 1
LANGUAGE_SCREEN = 2
current_state = HOME_SCREEN

# Game variables
is_jumping = False
y_position = screen_height - 120
y_velocity = 0
G = 6.674 * 10**-11
densidad = 5500
radio = 6.4 * 10**6
gravedad = (4 * math.pi * G * densidad * radio) / 3
initial_jump_velocity = 11

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
    take_screenshoot_button = Button(translations[current_language]["Take Screenshoot"], 150 + dif_x, 600 + dif_y, 500, 50)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if current_state == HOME_SCREEN:
                if play_button.is_clicked(mouse_pos):
                    current_state = GAME_SCREEN
                elif language_button.is_clicked(mouse_pos):
                    print("Language button clicked")  # Implement language selection logic
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
                    y_position = screen_height - 120
                    y_velocity = 0
                elif take_screenshoot_button.is_clicked(mouse_pos):
                    print(radius_slider.value, density_slider.value, temperature_slider.value)
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
                y_velocity = -initial_jump_velocity
                is_jumping = True

    screen.blit(background_image, (0, 0))

    if current_state == HOME_SCREEN:
        play_button.draw(screen)
        language_button.draw(screen)
        quit_button.draw(screen)
        take_image_button.draw(screen)
    elif current_state == GAME_SCREEN:
        # Game logic
        radius = radius_slider.value * 1000 * 6.3
        density = density_slider.value * 5.5
        gravedad = (4 / 3) * math.pi * G * density * radius 

        if is_jumping:
            y_position += y_velocity
            y_velocity += gravedad * 0.016
            if y_position >= screen_height - 120:
                y_position = screen_height - 120
                is_jumping = False

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
        player_pos_y = y_position - 132
        screen.blit(face_image, (player_pos_x + 115 , player_pos_y + 19 ))
        screen.blit(player_image, (player_pos_x , player_pos_y ))

        # Display slider values
        font = pygame.font.Font(None, 16)
        radius_text = font.render(f'{translations[current_language]["Radius"]}: {radius_slider.value:.2f} x1000km', True, WHITE)
        density_text = font.render(f'{translations[current_language]["Density"]}: {density_slider.value:.2f} g/cm3', True, WHITE)
        temperature_text = font.render(f'{translations[current_language]["Temperature"]}: {temperature_slider.value:.2f} °C', True, WHITE)
        screen.blit(radius_text, (625 + dif_x, 80 + dif_y))
        screen.blit(density_text, (625 + dif_x, 160 + dif_y))
        screen.blit(temperature_text, (625 + dif_x, 240 + dif_y))

        # Draw return button
        return_button.draw(screen)
        take_screenshoot_button.draw(screen)
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
        screen.blit(english_flag, (105 + dif_x, 210 + dif_y))  # Position flag to the left of the button
        screen.blit(spanish_flag, (105 + dif_x, 310 + dif_y))
        screen.blit(french_flag, (505 + dif_x, 210 + dif_y))
        screen.blit(german_flag, (505 + dif_x, 310 + dif_y))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()