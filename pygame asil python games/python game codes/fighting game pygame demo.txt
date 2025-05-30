import pygame
import sys

# -- Constants and Setup --
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLOCK_SIZE = 40        # Size of each block (in pixels)
GRAVITY = 0.5          # Gravity acceleration
JUMP_SPEED = -10       # Speed when jumping

# Colors (RGB)
SKY_BLUE = (135, 206, 235)
GRASS_GREEN = (30, 180, 30)
DIRT_BROWN = (150, 75, 0)
PLAYER_COLOR = (255, 0, 0)

# -- World Generation --
# The world is stored as a dictionary where each key is an (x, y) tuple (grid coordinates)
# and the value is a string representing the type of block at that position.
world = {}

def generate_world():
    global world
    # Define the grid rows and columns based on the screen dimensions and block size.
    rows = SCREEN_HEIGHT // BLOCK_SIZE
    cols = SCREEN_WIDTH // BLOCK_SIZE

    # We set a "ground level" a few blocks from the bottom of the screen.
    ground_level = rows - 3

    # Create a horizontally extended world: you can adjust the range for a larger terrain.
    for x in range(-50, 50):
        for y in range(ground_level, rows):
            # The top row of the ground gets a grass block; below that, place dirt.
            if y == ground_level:
                world[(x, y)] = "grass"
            else:
                world[(x, y)] = "dirt"

generate_world()

def draw_world(screen, camera_x, camera_y):
    """Draws each block in the world relative to the camera offset."""
    for (x, y), block in world.items():
        # Convert grid coordinates to pixel positions taking into account the camera
        block_x = x * BLOCK_SIZE + camera_x
        block_y = y * BLOCK_SIZE + camera_y
        
        # Skip drawing blocks that are completely off screen.
        if block_x < -BLOCK_SIZE or block_x > SCREEN_WIDTH or block_y < -BLOCK_SIZE or block_y > SCREEN_HEIGHT:
            continue
        
        # Choose a color based on the block type.
        if block == "grass":
            color = GRASS_GREEN
        elif block == "dirt":
            color = DIRT_BROWN
        
        # Draw the block as a filled rectangle with a thin outline.
        pygame.draw.rect(screen, color, (block_x, block_y, BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(screen, (0, 0, 0), (block_x, block_y, BLOCK_SIZE, BLOCK_SIZE), 1)

# -- Player Class --
class Player:
    def __init__(self, x, y):
        # The player is represented by a rectangle.
        # Here the width is one block and height is two blocks.
        self.rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE * 2)
        self.vel_y = 0      # Y-axis velocity (for jumping/falling)
        self.on_ground = False

    def update(self):
        """Apply gravity and handle vertical movement and collisions."""
        # Apply gravity
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y

        # Reset on_ground flag; will be set to True if colliding with a block.
        self.on_ground = False
        for (bx, by), block in world.items():
            block_rect = pygame.Rect(bx * BLOCK_SIZE, by * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            if self.rect.colliderect(block_rect):
                # If falling, set the player's bottom to block's top and stop vertical velocity.
                if self.vel_y > 0:
                    self.rect.bottom = block_rect.top
                    self.on_ground = True
                    self.vel_y = 0
                # If jumping and hitting a block above, set the player's top to block's bottom.
                elif self.vel_y < 0:
                    self.rect.top = block_rect.bottom
                    self.vel_y = 0

    def move(self, dx):
        """Move the player left or right and check horizontal collisions."""
        self.rect.x += dx
        for (bx, by), block in world.items():
            block_rect = pygame.Rect(bx * BLOCK_SIZE, by * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            if self.rect.colliderect(block_rect):
                if dx > 0:  # Moving right; align to left edge of block
                    self.rect.right = block_rect.left
                elif dx < 0:  # Moving left; align to right edge of block
                    self.rect.left = block_rect.right

    def jump(self):
        """Make the player jump if they are on the ground."""
        if self.on_ground:
            self.vel_y = JUMP_SPEED

    def draw(self, screen, camera_x, camera_y):
        """Draw the player on the screen with the camera offset."""
        pygame.draw.rect(screen, PLAYER_COLOR, 
                         (self.rect.x + camera_x, self.rect.y + camera_y, self.rect.width, self.rect.height))

# -- Main Game Loop --
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Minecraft Adventure - Pygame Edition")
    clock = pygame.time.Clock()

    # Create a player starting at position (100, 100)
    player = Player(100, 100)
    
    # Camera offsets allow us to simulate the “camera” following the player.
    camera_x = 0
    camera_y = 0

    running = True
    while running:
        clock.tick(60)  # Limit the game to 60 frames per second
        
        # -- Event Handling --
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Jump when the player presses the space bar.
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump()
            
            # Mouse events for block interaction.
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Get the mouse position on screen.
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Convert the mouse coordinates to world grid coordinates.
                grid_x = (mouse_x - camera_x) // BLOCK_SIZE
                grid_y = (mouse_y - camera_y) // BLOCK_SIZE
                # Left-click removes a block if one exists.
                if event.button == 1:
                    if (grid_x, grid_y) in world:
                        del world[(grid_x, grid_y)]
                # Right-click places a dirt block.
                elif event.button == 3:
                    world[(grid_x, grid_y)] = "dirt"

        # -- Player Movement --
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            player.move(-5)
        if keys[pygame.K_d]:
            player.move(5)
        
        # Update player position (gravity, collisions).
        player.update()

        # -- Camera System --
        # Center the camera on the player's center position.
        camera_x = SCREEN_WIDTH // 2 - player.rect.centerx
        camera_y = SCREEN_HEIGHT // 2 - player.rect.centery

        # -- Drawing --
        screen.fill(SKY_BLUE)               # Clear screen with sky color.
        draw_world(screen, camera_x, camera_y)
        player.draw(screen, camera_x, camera_y)

        pygame.display.flip()               # Update the display

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
