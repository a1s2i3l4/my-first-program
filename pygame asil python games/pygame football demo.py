import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Multiplayer Football Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 32)

# Colors
WHITE = (255, 255, 255)
GREEN = (50, 205, 50)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

# Field and Goal settings
GOAL_WIDTH = 100
GOAL_HEIGHT = 200
PLAYER_RADIUS = 25
BALL_RADIUS = 15

# Player class
class Player:
    def __init__(self, x, y, color, controls):
        self.x = x
        self.y = y
        self.color = color
        self.controls = controls
        self.speed = 5
        self.score = 0

    def move(self, keys):
        if keys[self.controls['left']]:
            self.x -= self.speed
        if keys[self.controls['right']]:
            self.x += self.speed
        if keys[self.controls['up']]:
            self.y -= self.speed
        if keys[self.controls['down']]:
            self.y += self.speed

        # Stay inside field
        self.x = max(PLAYER_RADIUS, min(WIDTH - PLAYER_RADIUS, self.x))
        self.y = max(PLAYER_RADIUS, min(HEIGHT - PLAYER_RADIUS, self.y))

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), PLAYER_RADIUS)

# Ball class
class Ball:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.vel_x = random.choice([-4, 4])
        self.vel_y = random.choice([-3, 3])

    def move(self):
        self.x += self.vel_x
        self.y += self.vel_y

        # Bounce off top/bottom
        if self.y <= BALL_RADIUS or self.y >= HEIGHT - BALL_RADIUS:
            self.vel_y *= -1

    def draw(self, surface):
        pygame.draw.circle(surface, YELLOW, (int(self.x), int(self.y)), BALL_RADIUS)

    def collide_with_player(self, player):
        dx = self.x - player.x
        dy = self.y - player.y
        distance = (dx**2 + dy**2)**0.5
        if distance <= PLAYER_RADIUS + BALL_RADIUS:
            self.vel_x = dx / distance * 5
            self.vel_y = dy / distance * 5

# Initialize players and ball
controls1 = {'left': pygame.K_a, 'right': pygame.K_d, 'up': pygame.K_w, 'down': pygame.K_s}
controls2 = {'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'up': pygame.K_UP, 'down': pygame.K_DOWN}

player1 = Player(150, HEIGHT // 2, BLUE, controls1)
player2 = Player(WIDTH - 150, HEIGHT // 2, RED, controls2)
ball = Ball()

# Score display
def draw_scores():
    score_text = font.render(f"{player1.score} : {player2.score}", True, BLACK)
    screen.blit(score_text, (WIDTH // 2 - 40, 20))

# Draw goals
def draw_goals():
    pygame.draw.rect(screen, BLACK, (0, HEIGHT//2 - GOAL_HEIGHT//2, 10, GOAL_HEIGHT))
    pygame.draw.rect(screen, BLACK, (WIDTH - 10, HEIGHT//2 - GOAL_HEIGHT//2, 10, GOAL_HEIGHT))

# Check for goal
def check_goal():
    if ball.x - BALL_RADIUS <= 10 and HEIGHT//2 - GOAL_HEIGHT//2 < ball.y < HEIGHT//2 + GOAL_HEIGHT//2:
        player2.score += 1
        ball.reset()
    elif ball.x + BALL_RADIUS >= WIDTH - 10 and HEIGHT//2 - GOAL_HEIGHT//2 < ball.y < HEIGHT//2 + GOAL_HEIGHT//2:
        player1.score += 1
        ball.reset()

# Main game loop
running = True
while running:
    screen.fill(GREEN)
    draw_goals()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movement
    keys = pygame.key.get_pressed()
    player1.move(keys)
    player2.move(keys)
    ball.move()

    # Collision
    ball.collide_with_player(player1)
    ball.collide_with_player(player2)

    # Check for goal
    check_goal()

    # Draw everything
    player1.draw(screen)
    player2.draw(screen)
    ball.draw(screen)
    draw_scores()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
