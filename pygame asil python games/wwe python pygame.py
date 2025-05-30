import pygame
import random

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("WWE Wrestling Game")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Game variables
player1_x, player1_y = 100, HEIGHT - 150
player2_x, player2_y = 600, HEIGHT - 150
player_width, player_height = 50, 50
player1_health, player2_health = 100, 100

# Clock
clock = pygame.time.Clock()

# Fonts
font = pygame.font.SysFont(None, 36)

# Functions to draw health bar
def draw_health_bar(x, y, health, color):
    pygame.draw.rect(screen, color, (x, y, 200, 20))
    pygame.draw.rect(screen, (0, 0, 0), (x, y, 200, 20), 2)
    pygame.draw.rect(screen, (255, 0, 0), (x, y, health * 2, 20))

# Main Game Loop
running = True
while running:
    screen.fill(WHITE)
   
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
   
    # Key press events for player1 (WASD) and player2 (Arrow keys)
    keys = pygame.key.get_pressed()

    # Player 1 controls
    if keys[pygame.K_a]:
        player1_x -= 5
    if keys[pygame.K_d]:
        player1_x += 5
    if keys[pygame.K_w]:
        player1_y -= 5
    if keys[pygame.K_s]:
        player1_y += 5

    # Player 2 controls
    if keys[pygame.K_LEFT]:
        player2_x -= 5
    if keys[pygame.K_RIGHT]:
        player2_x += 5
    if keys[pygame.K_UP]:
        player2_y -= 5
    if keys[pygame.K_DOWN]:
        player2_y += 5

    # Simulate a random punch or attack (simple version)
    if random.random() < 0.02:  # Chance to hit each frame
        if abs(player1_x - player2_x) < 60 and abs(player1_y - player2_y) < 60:
            player2_health -= 10  # Player 1 attacks Player 2
        if abs(player2_x - player1_x) < 60 and abs(player2_y - player1_y) < 60:
            player1_health -= 10  # Player 2 attacks Player 1

    # Draw players (simple rectangles for now)
    pygame.draw.rect(screen, BLUE, (player1_x, player1_y, player_width, player_height))
    pygame.draw.rect(screen, RED, (player2_x, player2_y, player_width, player_height))

    # Draw health bars
    draw_health_bar(50, 20, player1_health, BLUE)
    draw_health_bar(WIDTH - 250, 20, player2_health, RED)

    # Check for winner
    if player1_health <= 0:
        winner_text = font.render("Player 2 Wins!", True, RED)
        screen.blit(winner_text, (WIDTH//2 - 100, HEIGHT//2))
    elif player2_health <= 0:
        winner_text = font.render("Player 1 Wins!", True, BLUE)
        screen.blit(winner_text, (WIDTH//2 - 100, HEIGHT//2))

    pygame.display.flip()

    clock.tick(60)

pygame.quit()