import pygame

# Initialize
pygame.init()
WIDTH, HEIGHT = 800, 400
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2 Player Fighting Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Colors
WHITE = (255, 255, 255)
RED = (220, 50, 50)
BLUE = (50, 50, 255)
BLACK = (0, 0, 0)

# Players
player1 = pygame.Rect(100, 300, 50, 80)
player2 = pygame.Rect(650, 300, 50, 80)
p1_health = 100
p2_health = 100

# Game settings
speed = 5
punch_range = 50
punch_cooldown = 500  # ms
last_punch1 = 0
last_punch2 = 0

# Draw function
def draw():
    win.fill(WHITE)
    pygame.draw.rect(win, RED, player1)
    pygame.draw.rect(win, BLUE, player2)

    # Health bars
    pygame.draw.rect(win, RED, (20, 20, p1_health * 2, 20))
    pygame.draw.rect(win, BLUE, (WIDTH - 220, 20, p2_health * 2, 20))

    # Health text
    p1_text = font.render(f"P1 HP: {p1_health}", True, BLACK)
    p2_text = font.render(f"P2 HP: {p2_health}", True, BLACK)
    win.blit(p1_text, (20, 45))
    win.blit(p2_text, (WIDTH - 160, 45))

    pygame.display.update()

# Main game loop
running = True
while running:
    clock.tick(60)
    keys = pygame.key.get_pressed()
    now = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movement
    if keys[pygame.K_a] and player1.x > 0:
        player1.x -= speed
    if keys[pygame.K_d] and player1.x < WIDTH - player1.width:
        player1.x += speed

    if keys[pygame.K_LEFT] and player2.x > 0:
        player2.x -= speed
    if keys[pygame.K_RIGHT] and player2.x < WIDTH - player2.width:
        player2.x += speed

    # P1 Punch
    if keys[pygame.K_w] and now - last_punch1 > punch_cooldown:
        if abs(player1.x - player2.x) < punch_range:
            p2_health -= 10
        last_punch1 = now

    # P2 Punch
    if keys[pygame.K_UP] and now - last_punch2 > punch_cooldown:
        if abs(player2.x - player1.x) < punch_range:
            p1_health -= 10
        last_punch2 = now

    # Check win condition
    if p1_health <= 0 or p2_health <= 0:
        winner = "Player 1 Wins!" if p2_health <= 0 else "Player 2 Wins!"
        win.fill(WHITE)
        msg = font.render(winner, True, BLACK)
        win.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2))
        pygame.display.update()
        pygame.time.delay(3000)
        running = False

    draw()

pygame.quit()