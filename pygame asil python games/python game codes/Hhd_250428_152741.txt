import pygame, random

pygame.init()
win = pygame.display.set_mode((400, 600))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 50)

bird = pygame.Rect(100, 250, 30, 30)
gravity = 0
pipes = []
score = 0

def draw():
    win.fill((135, 206, 235))
    for p in pipes:
        pygame.draw.rect(win, (0, 255, 0), p)
    pygame.draw.rect(win, (255, 255, 0), bird)
    win.blit(font.render(str(score), True, (0,0,0)), (10,10))
    pygame.display.update()

running = True
while running:
    clock.tick(30)
    gravity += 1
    bird.y += gravity

    if len(pipes) == 0 or pipes[-1].x < 250:
        h = random.randint(100, 400)
        pipes.append(pygame.Rect(400, 0, 50, h))
        pipes.append(pygame.Rect(400, h + 150, 50, 600 - h - 150))

    for p in pipes:
        p.x -= 5
    pipes = [p for p in pipes if p.x > -50]

    for p in pipes:
        if bird.colliderect(p):
            running = False
    if bird.y > 600 or bird.y < 0:
        running = False

    score += 1
    draw()

pygame.quit()