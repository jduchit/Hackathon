import pygame
import pygame.freetype
from PIL import Image
import tkinter as tk
from tkinter import filedialog, messagebox
import random
import math

# Inicializar pygame y tkinter
pygame.init()
pygame.mixer.init()  # Inicializar el módulo de sonido
root = tk.Tk()
root.withdraw()  # Ocultar la ventana principal de tkinter

# Cargar el sonido flip
flip_sound = pygame.mixer.Sound('C:/Users/Johana/Downloads/flip.wav')

# Dimensiones de la ventana y la postal
SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 800
POSTCARD_WIDTH = 864
POSTCARD_HEIGHT = 648

# Definir colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHTBLUE = (173, 216, 230)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
HOVER_COLOR = (100, 149, 237)

# Definir estrellas fugaces
NUM_STARS = 100
stars = []

# Cargar imagen de fondo para la parte trasera de la postal
reverse_image_path = 'C:/Users/Johana/Downloads/Reverse.png'
try:
    background_image = pygame.image.load(reverse_image_path)
    background_image = pygame.transform.scale(background_image, (POSTCARD_WIDTH, POSTCARD_HEIGHT))
except pygame.error as e:
    print(f"Error al cargar la imagen de fondo del reverso: {e}")
    background_image = pygame.Surface((POSTCARD_WIDTH, POSTCARD_HEIGHT))
    background_image.fill(WHITE)

# Cargar fuentes personalizadas
font_path = 'C:/Users/Johana/Downloads/CloudyEraser.otf'
font_path2 = 'C:/Users/Johana/Downloads/JMH.ttf'
try:
    custom_font = pygame.freetype.Font(font_path, 36)
    custom_font2 = pygame.freetype.Font(font_path2, 21)
except IOError:
    print(f"Error al cargar la fuente personalizada desde {font_path}. Usando Arial por defecto.")
    custom_font = pygame.freetype.SysFont("Arial", 36)
    custom_font2 = pygame.freetype.SysFont("Arial", 36)

# Cargar fuente estándar
default_font = pygame.freetype.SysFont("Arial", 36)

# Variables para mensajes
left_message = "Your preset message on the left side"
right_message = "Custom message on the right side"
user_input = ""
text_box_active = False
placeholder_text = "Escribe aquí..."

# Variables para manejar la repetición de la tecla Backspace
backspace_held = False
backspace_time = 0
BACKSPACE_DELAY = 500  # Milisegundos antes de empezar a eliminar
BACKSPACE_REPEAT = 50   # Milisegundos entre cada eliminación

# Variables del cursor
cursor_visible = True
cursor_timer = 0
CURSOR_BLINK_INTERVAL = 500  # Milisegundos

# Crear la ventana principal
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Interactive Postcard')

# Definir área del cuadro de texto y botón de descarga
TEXT_BOX_RECT = pygame.Rect(0, 0, POSTCARD_WIDTH - 100, 60)
DOWNLOAD_BUTTON_RECT = pygame.Rect(0, 0, POSTCARD_WIDTH - 100, 40)
POSTCARD_RECT = pygame.Rect(0, 0, POSTCARD_WIDTH, POSTCARD_HEIGHT)

# Función para centrar los elementos de la postal
def center_elements():
    total_height = POSTCARD_HEIGHT + 60 + 40 + 40  # Postal + cuadro de texto + botón de descarga + margen
    y_offset = (SCREEN_HEIGHT - total_height) // 2
    POSTCARD_RECT.x = (SCREEN_WIDTH - POSTCARD_WIDTH) // 2
    POSTCARD_RECT.y = y_offset
    TEXT_BOX_RECT.x = POSTCARD_RECT.x + 50
    TEXT_BOX_RECT.y = POSTCARD_RECT.y + POSTCARD_HEIGHT + 10
    DOWNLOAD_BUTTON_RECT.x = POSTCARD_RECT.x + 50
    DOWNLOAD_BUTTON_RECT.y = TEXT_BOX_RECT.y + TEXT_BOX_RECT.height + 10

# Función para generar estrellas fugaces
def generate_stars():
    for _ in range(NUM_STARS):
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT)
        speed = random.uniform(1, 4)
        brightness = random.randint(150, 255)
        blink_speed = random.uniform(0.01, 0.05)
        stars.append([x, y, speed, brightness, blink_speed])

# Función para mover las estrellas
def move_stars():
    for star in stars:
        star[0] -= star[2] * 4
        star[1] += star[2] * 0.5
        star[3] = 255 * (0.5 + 0.5 * math.sin(pygame.time.get_ticks() * star[4]))
        if star[0] < 0 or star[1] > SCREEN_HEIGHT:
            star[0] = random.randint(SCREEN_WIDTH, SCREEN_WIDTH + 50)
            star[1] = random.randint(0, SCREEN_HEIGHT // 2)

# Función para dibujar las estrellas
def draw_stars():
    for star in stars:
        color = (int(star[3]), int(star[3]), int(star[3]))
        pygame.draw.circle(screen, color, (int(star[0]), int(star[1])), 2)

# Función para dividir texto en líneas
def wrap_text(text, font, max_width):
    lines = []
    words = text.split(' ')
    current_line = ""
    for word in words:
        if font.render(word, BLACK)[0].get_width() > max_width:
            split_word = word
            while font.render(split_word, BLACK)[0].get_width() > max_width:
                for i in range(1, len(split_word)):
                    if font.render(split_word[:i], BLACK)[0].get_width() > max_width:
                        lines.append(split_word[:i-1] + "-")
                        split_word = split_word[i-1:]
                        break
            current_line = split_word
        else:
            test_line = current_line + " " + word if current_line else word
            if font.render(test_line, BLACK)[0].get_width() <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
    if current_line:
        lines.append(current_line)
    return lines

# Función para mostrar la parte frontal de la postal
def display_front():
    pygame.draw.rect(screen, LIGHTBLUE, POSTCARD_RECT)
    default_font.render_to(screen, (POSTCARD_RECT.x + POSTCARD_RECT.width // 2 - 100, POSTCARD_RECT.y + POSTCARD_RECT.height // 2 - 18), "Front Side", BLACK)

# Función para renderizar el mensaje predeterminado en el lado izquierdo de la postal
def draw_default_left_message(surface, font, start_x, start_y, max_width):
    default_message = "Your preset message on the left side"
    lines = wrap_text(default_message, font, max_width)
    for i, line in enumerate(lines):
        font.render_to(surface, (start_x, start_y + i * 40), line, BLACK)

# Función para renderizar el mensaje personalizado en el lado derecho de la postal
def draw_custom_right_message(surface, font, start_x, start_y, max_width):
    lines = wrap_text(user_input, font, max_width)
    for i, line in enumerate(lines):
        font.render_to(surface, (start_x, start_y + i * 40), line, BLACK)

# Función para mostrar la parte trasera de la postal
def display_back():
    screen.blit(background_image, (POSTCARD_RECT.x, POSTCARD_RECT.y))

    left_area_width = POSTCARD_WIDTH // 2 - 40
    right_area_width = POSTCARD_WIDTH // 2 - 40

    left_start_y = POSTCARD_RECT.y + 50
    right_start_y = POSTCARD_RECT.y + POSTCARD_HEIGHT // 2 + 20

    # Llamar a la función específica para poner el mensaje predeterminado en el lado izquierdo
    draw_default_left_message(screen, custom_font2, POSTCARD_RECT.x + 50, left_start_y, left_area_width)

    # Renderizar el lado derecho (mensaje personalizado)
    draw_custom_right_message(screen, custom_font, POSTCARD_RECT.x + POSTCARD_WIDTH // 2 + 20, right_start_y, right_area_width)

# Función para mostrar el cuadro de texto
def display_text_box():
    pygame.draw.rect(screen, WHITE, TEXT_BOX_RECT, 0)
    pygame.draw.rect(screen, BLACK, TEXT_BOX_RECT, 2 if not text_box_active else 3)
    if user_input:
        default_font.render_to(screen, (TEXT_BOX_RECT.x + 10, TEXT_BOX_RECT.y + 15), user_input, BLACK)
    else:
        default_font.render_to(screen, (TEXT_BOX_RECT.x + 10, TEXT_BOX_RECT.y + 15), placeholder_text, GRAY)
    
    # Mostrar cursor parpadeante si el cuadro de texto está activo
    if text_box_active and cursor_visible:
        text_surface, _ = default_font.render(user_input, BLACK)
        text_width = text_surface.get_width()
        cursor_x = TEXT_BOX_RECT.x + 10 + text_width + 2
        cursor_y = TEXT_BOX_RECT.y + 15
        pygame.draw.line(screen, BLACK, (cursor_x, cursor_y), (cursor_x, cursor_y + text_surface.get_height()), 2)

# Función para mostrar el botón de descarga
def display_download_button(mouse_pos):
    button_color = HOVER_COLOR if DOWNLOAD_BUTTON_RECT.collidepoint(mouse_pos) else LIGHTBLUE
    pygame.draw.rect(screen, button_color, DOWNLOAD_BUTTON_RECT)
    pygame.draw.rect(screen, BLACK, DOWNLOAD_BUTTON_RECT, 2)
    default_font.render_to(screen, (DOWNLOAD_BUTTON_RECT.x + 100, DOWNLOAD_BUTTON_RECT.y + 5), "Descargar Postal", BLACK)

# Función para alternar entre frente y reverso de la postal
def flip_postal():
    global postal_front
    pygame.mixer.Sound.play(flip_sound)  # Reproducir el sonido al voltear
    postal_front = not postal_front

# Función para guardar la postal
def download_postal():
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if file_path:
        # Crear una nueva imagen con el doble de la altura para almacenar ambos lados
        img = Image.new('RGB', (POSTCARD_WIDTH, POSTCARD_HEIGHT * 2), color=WHITE)
        
        # Generar la imagen del lado frontal
        front_surf = pygame.Surface((POSTCARD_WIDTH, POSTCARD_HEIGHT))
        front_surf.fill(LIGHTBLUE)
        default_font.render_to(front_surf, (POSTCARD_WIDTH // 2 - 100, POSTCARD_HEIGHT // 2 - 30), "Front Side", BLACK)
        front_image = pygame.surfarray.array3d(front_surf)
        front_image = Image.fromarray(front_image.transpose([1, 0, 2]))  # Transponer para ajustar la orientación correcta
        img.paste(front_image, (0, 0))  # Pegar la imagen del frente en la parte superior

        # Generar la imagen del lado trasero
        back_surf = pygame.Surface((POSTCARD_WIDTH, POSTCARD_HEIGHT))
        back_surf.blit(background_image, (0, 0))
        
        # Lado izquierdo: Usar la misma fuente y renderizado que en la vista interactiva, con ajustes de altura
        left_lines = wrap_text(left_message, custom_font2, POSTCARD_WIDTH // 2 - 40)
        right_lines = wrap_text(user_input, custom_font, POSTCARD_WIDTH // 2 - 40)
        
        left_start_y = POSTCARD_RECT.y + 50  # Ajusta la altura para que coincida
        for i, line in enumerate(left_lines):
            custom_font2.render_to(back_surf, (50, left_start_y + i * 40), line, BLACK)
        
        # Lado derecho: Ajustar la altura del texto
        right_start_y = POSTCARD_RECT.y + POSTCARD_HEIGHT // 2 + 20
        for i, line in enumerate(right_lines):
            custom_font.render_to(back_surf, (POSTCARD_WIDTH // 2 + 20, right_start_y + i * 40), line, BLACK)

        # Convertir el lado trasero a imagen de PIL y transponer para la orientación correcta
        back_image = pygame.surfarray.array3d(back_surf)
        back_image = Image.fromarray(back_image.transpose([1, 0, 2]))  # Transponer para corregir la orientación
        img.paste(back_image, (0, POSTCARD_HEIGHT))  # Pegar la imagen trasera debajo de la imagen frontal
        
        # Guardar la imagen final
        img.save(file_path)
        messagebox.showinfo("Postal guardada", "La postal interactiva ha sido guardada con éxito.")

# Función principal para la postal interactiva
def postcard():
    generate_stars()
    clock = pygame.time.Clock()
    global postal_front, text_box_active, user_input
    postal_front = True
    running = True

    while running:
        dt = clock.tick(60)
        global cursor_timer, cursor_visible
        cursor_timer += dt
        if cursor_timer >= CURSOR_BLINK_INTERVAL:
            cursor_visible = not cursor_visible
            cursor_timer = 0

        mouse_pos = pygame.mouse.get_pos()
        move_stars()
        screen.fill(BLACK)
        draw_stars()

        center_elements()
        if postal_front:
            display_front()
        else:
            display_back()

        display_text_box()
        display_download_button(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if POSTCARD_RECT.collidepoint(mouse_pos):
                    flip_postal()
                    text_box_active = False
                elif TEXT_BOX_RECT.collidepoint(mouse_pos):
                    text_box_active = True
                elif DOWNLOAD_BUTTON_RECT.collidepoint(mouse_pos):
                    download_postal()
                else:
                    text_box_active = False

            elif event.type == pygame.KEYDOWN and text_box_active:
                if event.key == pygame.K_BACKSPACE:
                    backspace_held = True
                    backspace_time = 0
                    if user_input:
                        user_input = user_input[:-1]
                elif event.unicode.isprintable() and len(user_input.split()) < 10:
                    user_input += event.unicode
                else:
                    messagebox.showwarning("Límite de palabras", "El mensaje no puede tener más de 10 palabras.")

            elif event.type == pygame.KEYUP and event.key == pygame.K_BACKSPACE:
                backspace_held = False

        pygame.display.flip()

    pygame.quit()

# Llamar la función principal para iniciar la postal interactiva
postcard()