import pygame
import sys
import random

# Función para crear tuberías
def create_pipe():
    pipe_type = random.choice(['both', 'top', 'bottom'])
    if pipe_type == 'both':
        middle_position = random.randint(330, 500)
        top_pipe = pipe_surface.get_rect(midbottom=(800, middle_position - pipe_gap // 2))
        bottom_pipe = pipe_surface.get_rect(midtop=(800, middle_position + pipe_gap // 2))
        return bottom_pipe, top_pipe
    elif pipe_type == 'top':
        top_pipe_height = random.randint(200, 375)
        top_pipe = pipe_surface.get_rect(midbottom=(800, top_pipe_height))
        return (top_pipe,)
    else:
        bottom_pipe_height = random.randint(190, 275)
        bottom_pipe = pipe_surface.get_rect(midtop=(800, bottom_pipe_height))
        return (bottom_pipe,)

# Función para mover las tuberías
def move_pipes(pipes):
    global score, last_pipe_time, high_score

    current_time = pygame.time.get_ticks()

    for pipe in pipes:
        pipe.centerx -= 5

        if pipe.right < bird_rect.left and current_time - last_pipe_time > 200:
            last_pipe_time = current_time
            score += 0.5
            if score > high_score:  # Actualizar high score si la puntuación actual es mayor
                high_score = score
            if score % 5 == 0:
                pygame.mixer.Sound('assets/score.mp3').play()

        if pipe.right <= 0:
            last_pipe_time = current_time

    return [pipe for pipe in pipes if pipe.right > -50]

def menu():
    font = pygame.font.SysFont(None, 40)  # Tamaño de fuente más grande
    img_title = font.render("Corona Virus", True, (255, 255, 255))  # Título del juego
    img = font.render("1.- Crèdits", True, (255, 255, 255))
    img2 = font.render("2.- Jugar (SPACE)", True, (255, 255, 255))
    img3 = font.render("3.- Sortir (ESC)", True, (255, 255, 255))
    high_score_text = game_font.render(f'High Score: {int(high_score)}', True, (255, 255, 255))

    screen.blit(bg_surface, (0, 0))
    screen.blit(seccio_transparent, (200, 100))  # Centrar el menú horizontalmente
    screen.blit(img_title, (300, 150))  # Mostrar el título del juego
    screen.blit(img, (300, 220))
    screen.blit(img2, (300, 280))
    screen.blit(img3, (300, 340))
    screen.blit(high_score_text, (300, 390))
    pygame.display.update()

def credits():
    global creditsa
    while creditsa:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    creditsa = False

        font = pygame.font.SysFont(None, 30)  # Tamaño de fuente más grande
        img = font.render("1.- CODIGO: Daniel Agache, en", True, (255, 255, 255))
        img2 = font.render("2.- Diseñador: Moha Bouakka, Daniel", True, (255, 255, 255))
        img6 = font.render("Agache y en colaboración Kristopher", True, (255, 255, 255))
        img3 = font.render("3.- Música: Pixabay ", True, (255, 255, 255))
        img4 = font.render("4.- Efectos de sonido: Pixabay ", True, (255, 255, 255))
        img5 = font.render("Presiona ESPACIO para volver al menú", True, (255, 255, 255))
        img7 = font.render("González", True, (255, 255, 255))
        img8 = font.render("Colaboració Xavi Sancho i Arno Brescia", True, (255, 255, 255))

        screen.blit(bg_surface, (0, 0))
        screen.blit(seccio_transparent, (200, 100))  # Centrar el menú horizontalmente
        screen.blit(img, (200, 150))
        screen.blit(img2, (200, 210))
        screen.blit(img6, (200, 235))
        screen.blit(img3, (200, 290))
        screen.blit(img4, (200, 330))
        screen.blit(img5, (200, 400))
        screen.blit(img7, (200, 260))
        screen.blit(img8, (200, 170))
        pygame.display.update()

# Función para dibujar las tuberías
def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 600:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

# Función para rotar el pájaro
def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3, 1)
    return new_bird

# Función para mostrar la puntuación en pantalla
def score_display():
    score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
    score_rect = score_surface.get_rect(center=(400, 50))
    screen.blit(score_surface, score_rect)

    high_score_surface = game_font.render(f'High Score: {int(high_score)}', True, (255, 255, 255))
    high_score_rect = high_score_surface.get_rect(center=(400, 100))
    screen.blit(high_score_surface, high_score_rect)

# Función para comprobar colisiones
def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
    if bird_rect.top <= 0 or bird_rect.bottom >= 550:
        return False
    return True

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
game_font = pygame.font.Font(None, 40)
creditsa = False

bg_surface = pygame.image.load('assets/fons.png').convert()
floor_surface = pygame.image.load('assets/suelo.png').convert()
bird_downflap = pygame.image.load('assets/virus.png').convert_alpha()
pipe_surface = pygame.image.load('assets/vacuna.png').convert_alpha()

seccio_transparent = pygame.Surface((400, 400), pygame.SRCALPHA)
pygame.draw.rect(seccio_transparent, (20, 200, 170, 70), (0, 0, 400, 400))

gravity = 0.68
bird_movement = 0
game_active = False
score = 0
high_score = 0  # Variable para almacenar la mejor puntuación de la sesión
last_pipe_time = pygame.time.get_ticks()
pipe_gap = 220
pipe_heights = [200, 325, 400]
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 2000)
bird_frames = [bird_downflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(100, 300))

floor_x_pos = 0
# Variable para controlar si el juego está pausado
paused = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SPAWNPIPE and game_active and not paused:
            pipe_list.extend(create_pipe())

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_active and not paused:
                    pygame.mixer.Sound('assets/salt.mp3').play()
                    bird_movement = -12
                elif not game_active:
                    game_active = True
                    pipe_list.clear()
                    bird_rect.center = (100, 300)
                    bird_movement = 0
                    score = 0
                    # Cargar música de fondo
                    try:
                        pygame.mixer.music.load('assets/MUSICA.mp3')
                    except pygame.error as e:
                        print("Error al cargar la música de fondo:", e)
                        sys.exit(-1)
                    pygame.mixer.music.play(-1)
                elif paused:
                    paused = False
                    pygame.mixer.music.unpause()
            elif event.key == pygame.K_RETURN:  # Tecla ENTER para pausar
                if game_active and not paused:
                    paused = True
                    pygame.mixer.music.pause()
            elif event.key == pygame.K_ESCAPE:  # Tecla ESC para volver al menú
                if game_active:
                    game_active = False
                    paused = False
                    pipe_list.clear()
                    bird_rect.center = (100, 300)
                    bird_movement = 0
                    pygame.mixer.music.stop()
                else:  # Salir del juego si se presiona ESC en el menú
                    pygame.quit()
                    sys.exit()
            if event.key == pygame.K_1:
                creditsa = True

    screen.blit(bg_surface, (0, 0))

    if game_active and not paused:
        bird_movement += gravity
        bird_rect.centery += bird_movement

        rotated_bird = rotate_bird(bird_surface)
        screen.blit(rotated_bird, bird_rect)

        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        game_active = check_collision(pipe_list)

        if not game_active:
            pygame.mixer.music.stop()

        score_display()
    elif not game_active:
        menu()
        if creditsa:
            credits()

    elif paused:
        screen.blit(game_font.render('Juego pausado. Presiona ENTER para continuar', True, (255, 255, 255)), (100, 250))

    # Dibujar el suelo
    screen.blit(floor_surface, (floor_x_pos, 550))
    screen.blit(floor_surface, (floor_x_pos + 800, 550))

    # Mover el suelo
    floor_x_pos -= 1
    if floor_x_pos <= -800:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(60)
