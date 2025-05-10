import pygame
import random
import math

# Constants for the game
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CELL_SIZE = 20
FPS = 10
SNAKE_INITIAL_LENGTH = 3
SNAKE_SPEED = 1
FOOD_COLOR = (255, 0, 0)
SNAKE_HEAD_COLOR = (255, 255, 0)
SNAKE_BODY_COLOR = (0, 200, 0)
BACKGROUND_COLOR = (0, 0, 0)

# Function to draw the snake
def draw_snake(screen, snake):
    for i, segment in enumerate(snake):
        if i == len(snake) - 1:
            # Draw the head as a diamond
            draw_diamond(screen, segment, SNAKE_HEAD_COLOR)
        else:
            # Draw body segments as circles
            pygame.draw.circle(screen, SNAKE_BODY_COLOR, (segment[0] + CELL_SIZE // 2, segment[1] + CELL_SIZE // 2), CELL_SIZE // 2)

# Function to draw a diamond head
def draw_diamond(screen, position, color):
    x, y = position
    half_side = CELL_SIZE // 2
    points = [(x + half_side, y), (x + CELL_SIZE, y + half_side),
              (x + half_side, y + CELL_SIZE), (x, y + half_side)]
    pygame.draw.polygon(screen, color, points)


# Function to generate new food position
def generate_food():
    return (random.randint(0, SCREEN_WIDTH - CELL_SIZE) // CELL_SIZE * CELL_SIZE,
            random.randint(0, SCREEN_HEIGHT - CELL_SIZE) // CELL_SIZE * CELL_SIZE)

# Main game function
def snake_game():
    pygame.init()

    # Initialize the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake Game")

    clock = pygame.time.Clock()

    # Initialize the snake and food
    snake = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
    food = generate_food()

    # Initial direction
    dx, dy = CELL_SIZE, 0

    score = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # Control the snake with arrow keys
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and dx == 0:
                    dx, dy = -CELL_SIZE, 0
                elif event.key == pygame.K_RIGHT and dx == 0:
                    dx, dy = CELL_SIZE, 0
                elif event.key == pygame.K_UP and dy == 0:
                    dx, dy = 0, -CELL_SIZE
                elif event.key == pygame.K_DOWN and dy == 0:
                    dx, dy = 0, CELL_SIZE

        # Move the snake
        head = (snake[-1][0] + dx, snake[-1][1] + dy)
        snake.append(head)

        # Check for collision with food
        if head == food:
            food = generate_food()
            score += 1
        else:
            # If no food is eaten, remove the tail segment
            snake.pop(0)

        # Check for collision with the screen border
        if head[0] < 0 or head[0] >= SCREEN_WIDTH or head[1] < 0 or head[1] >= SCREEN_HEIGHT:
            pygame.quit()
            quit()

        # Check for collision with the snake's body
        if len(set(snake)) != len(snake):
            pygame.quit()
            quit()

        # Clear the screen
        screen.fill(BACKGROUND_COLOR)

        # Draw the food
        pygame.draw.rect(screen, FOOD_COLOR, pygame.Rect(food[0], food[1], CELL_SIZE, CELL_SIZE))

        # Draw the snake
        draw_snake(screen, snake)

        # Render the score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    snake_game()
