import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 288
SCREEN_HEIGHT = 512

# Colors
WHITE = (255, 255, 255)

# Load images
BACKGROUND = pygame.image.load("assets/background-day.png")
BASE = pygame.image.load("assets/base.png")
BIRD = pygame.image.load("assets/yellowbird-midflap.png")
PIPE = pygame.image.load("assets/pipe-green.png")

# Game variables
gravity = 0.25
bird_movement = 0
game_active = True
score = 0

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Bird rectangle
bird_rect = BIRD.get_rect(center=(50, SCREEN_HEIGHT // 2))

# Base rectangle
base_rect = BASE.get_rect(topleft=(0, SCREEN_HEIGHT - 100))

# Pipe list
pipe_list = []

# Pipe settings
pipe_height = [200, 300, 400]
pipe_gap = 150

# Font
game_font = pygame.font.Font("freesansbold.ttf", 32)

def draw_base():
    screen.blit(BASE, base_rect)
    screen.blit(BASE, (base_rect.x + SCREEN_WIDTH, base_rect.y))

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = PIPE.get_rect(midtop=(SCREEN_WIDTH + 50, random_pipe_pos))
    top_pipe = PIPE.get_rect(midbottom=(SCREEN_WIDTH + 50, random_pipe_pos - pipe_gap))
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return [pipe for pipe in pipes if pipe.right > 0]

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= SCREEN_HEIGHT:
            screen.blit(PIPE, pipe)
        else:
            flip_pipe = pygame.transform.flip(PIPE, False, True)
            screen.blit(flip_pipe, pipe)

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
    if bird_rect.top <= -50 or bird_rect.bottom >= SCREEN_HEIGHT - 100:
        return False
    return True

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3, 1)
    return new_bird

def score_display():
    score_surface = game_font.render(f"Score: {int(score)}", True, WHITE)
    score_rect = score_surface.get_rect(center=(SCREEN_WIDTH // 2, 50))
    screen.blit(score_surface, score_rect)

# Main game loop
pipe_spawn = pygame.USEREVENT
pygame.time.set_timer(pipe_spawn, 1200)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 6
            if event.key == pygame.K_SPACE and not game_active:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (50, SCREEN_HEIGHT // 2)
                bird_movement = 0
                score = 0
        if event.type == pipe_spawn:
            pipe_list.extend(create_pipe())

    screen.blit(BACKGROUND, (0, 0))

    if game_active:
        bird_movement += gravity
        rotated_bird = rotate_bird(BIRD)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)

        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        score += 0.01
        score_display()
    else:
        score_display()

    draw_base()
    base_rect.x -= 1
    if base_rect.right <= SCREEN_WIDTH:
        base_rect.left = 0

    pygame.display.update()
    clock.tick(120)
