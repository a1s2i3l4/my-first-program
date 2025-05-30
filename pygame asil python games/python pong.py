import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH = 600
HEIGHT = 600
BALL_RADIUS = 20
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 60
FPS = 60

# Set up some variables
ball_x = WIDTH / 2
ball_y = HEIGHT / 2
ball_speed_x = 5
ball_speed_y = 5
paddle1_y = HEIGHT / 2
paddle2_y = HEIGHT / 2
score1 = 0
score2 = 0

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Move the paddles
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        paddle1_y -= 5
    if keys[pygame.K_s]:
        paddle1_y += 5
    if keys[pygame.K_UP]:
        paddle2_y -= 5
    if keys[pygame.K_DOWN]:
        paddle2_y += 5

    # Move the ball
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Collision with the edges
    if ball_y < 0 or ball_y > HEIGHT:
        ball_speed_y *= -1

    # Collision with the paddles
    if (ball_x < PADDLE_WIDTH and
            ball_y > paddle1_y - PADDLE_HEIGHT / 2 and
            ball_y < paddle1_y + PADDLE_HEIGHT / 2):
        ball_speed_x *= -1
    elif (ball_x > WIDTH - PADDLE_WIDTH - BALL_RADIUS and
            ball_y > paddle2_y - PADDLE_HEIGHT / 2 and
            ball_y < paddle2_y + PADDLE_HEIGHT / 2):
        ball_speed_x *= -1

    # Collision with the goal
    if ball_x < 0:
        score2 += 1
        ball_x = WIDTH / 2
        ball_y = HEIGHT / 2
    elif ball_x > WIDTH:
        score1 += 1
        ball_x = WIDTH / 2
        ball_y = HEIGHT / 2

    # Draw everything
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255, 255, 255),
                        (0, paddle1_y - PADDLE_HEIGHT / 2, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.rect(screen, (255, 255, 255),
                        (WIDTH - PADDLE_WIDTH, paddle2_y - PADDLE_HEIGHT / 2, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.circle(screen, (255, 255, 255), (int(ball_x), int(ball_y)), BALL_RADIUS)
    pygame.draw.aaline(screen, (255, 255, 255), (WIDTH / 2, 0), (WIDTH / 2, HEIGHT))
    font = pygame.font.Font(None, 72)
    text = font.render(str(score1) + " - " + str(score2), 1, (255, 255, 255))
    screen.blit(text, (WIDTH / 2 - text.get_width() / 2, 10))

    # Update the display
    pygame.display.flip()
    pygame.time.Clock().tick(FPS)