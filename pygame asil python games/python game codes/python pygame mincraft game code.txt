import pygame
import math

# Window dimensions
WIDTH, HEIGHT = 800, 600

# Block size
BLOCK_SIZE = 50

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

class Block:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def draw(self, screen, player_x, player_y, player_z):
        # Calculate the distance from the player
        distance = math.sqrt((self.x - player_x) ** 2 + (self.y - player_y) ** 2 + (self.z - player_z) ** 2)

        # Draw the block
        block_size = BLOCK_SIZE / distance
        pygame.draw.rect(screen, RED, (self.x * BLOCK_SIZE - player_x * BLOCK_SIZE + WIDTH / 2, self.y * BLOCK_SIZE - player_y * BLOCK_SIZE + HEIGHT / 2, block_size, block_size))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    blocks = [
        Block(0, 0, 0),
        Block(1, 0, 0),
        Block(0, 1, 0),
        Block(0, 0, 1),
    ]

    player_x, player_y, player_z = 0, 0, 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player_z -= 0.1
        if keys[pygame.K_s]:
            player_z += 0.1
        if keys[pygame.K_a]:
            player_x -= 0.1
        if keys[pygame.K_d]:
            player_x += 0.1

        screen.fill(WHITE)

        for block in blocks:
            block.draw(screen, player_x, player_y, player_z)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()