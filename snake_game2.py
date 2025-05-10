import pygame
import random
import math

# Add the following constants for the wall and menu colors
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CELL_SIZE = 20
FPS = 10
SNAKE_INITIAL_LENGTH = 3
SNAKE_SPEED = 1
FOOD_COLOR = (255, 0, 0)
SNAKE_HEAD_COLOR = (0, 255, 0)
SNAKE_BODY_COLOR = (0, 200, 0)
BACKGROUND_COLOR = (0, 0, 0)
WALL_COLOR = (100, 100, 100)
MENU_COLOR = (150, 150, 150)
BUTTON_COLOR = (200, 200, 200)
FONT_COLOR = (0, 0, 0)
FONT_SIZE = 40

# Function to draw the snake
def draw_snake(screen, snake):
    for i, segment in enumerate(snake):
        if i == len(snake) - 1:
            # Draw the head as a diamond
            draw_diamond(screen, segment, SNAKE_HEAD_COLOR)
        else:
            # Draw body segments as circles
            pygame.draw.circle(screen, SNAKE_BODY_COLOR, (segment[0] + CELL_SIZE // 2, segment[1] + CELL_SIZE // 2), CELL_SIZE // 2)

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

# Function to draw the wall
def draw_wall(screen):
    pygame.draw.rect(screen, WALL_COLOR, pygame.Rect(0, 0, SCREEN_WIDTH, CELL_SIZE))  # Top wall
    pygame.draw.rect(screen, WALL_COLOR, pygame.Rect(0, 0, CELL_SIZE, SCREEN_HEIGHT))  # Left wall
    pygame.draw.rect(screen, WALL_COLOR, pygame.Rect(SCREEN_WIDTH - CELL_SIZE, 0, CELL_SIZE, SCREEN_HEIGHT))  # Right wall
    pygame.draw.rect(screen, WALL_COLOR, pygame.Rect(0, SCREEN_HEIGHT - CELL_SIZE, SCREEN_WIDTH, CELL_SIZE))  # Bottom wall

# Function to draw the menu with buttons and game status
def draw_menu(screen, game_status):
    pygame.draw.rect(screen, MENU_COLOR, pygame.Rect(0, 0, SCREEN_WIDTH, CELL_SIZE))
    font = pygame.font.Font(None, FONT_SIZE)
    font_surface = font.render(game_status, True, FONT_COLOR)
    screen.blit(font_surface, ((SCREEN_WIDTH - font_surface.get_width()) // 2, (CELL_SIZE - font_surface.get_height()) // 2))

# Function to handle the menu and game status
def handle_menu(screen):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.fill(BACKGROUND_COLOR)
        draw_wall(screen)
        draw_menu(screen, "Snake Game")

        font = pygame.font.Font(None, FONT_SIZE)
        start_surface = font.render("Start", True, FONT_COLOR)
        start_button = pygame.Rect((SCREEN_WIDTH - start_surface.get_width()) // 2, 200, start_surface.get_width(), start_surface.get_height())

        resume_surface = font.render("Resume", True, FONT_COLOR)
        resume_button = pygame.Rect((SCREEN_WIDTH - resume_surface.get_width()) // 2, 250, resume_surface.get_width(), resume_surface.get_height())

        exit_surface = font.render("Exit", True, FONT_COLOR)
        exit_button = pygame.Rect((SCREEN_WIDTH - exit_surface.get_width()) // 2, 300, exit_surface.get_width(), exit_surface.get_height())

        pygame.draw.rect(screen, BUTTON_COLOR, start_button)
        screen.blit(start_surface, ((SCREEN_WIDTH - start_surface.get_width()) // 2, 200))

        pygame.draw.rect(screen, BUTTON_COLOR, resume_button)
        screen.blit(resume_surface, ((SCREEN_WIDTH - resume_surface.get_width()) // 2, 250))

        pygame.draw.rect(screen, BUTTON_COLOR, exit_button)
        screen.blit(exit_surface, ((SCREEN_WIDTH - exit_surface.get_width()) // 2, 300))

        mouse_x, mouse_y = pygame.mouse.get_pos()
        if start_button.collidepoint(mouse_x, mouse_y):
            if pygame.mouse.get_pressed()[0]:
                return "start"
        elif resume_button.collidepoint(mouse_x, mouse_y):
            if pygame.mouse.get_pressed()[0]:
                return "resume"
        elif exit_button.collidepoint(mouse_x, mouse_y):
            if pygame.mouse.get_pressed()[0]:
                pygame.quit()
                quit()

        pygame.display.flip()

# Modify the snake_game function to use the menu and game status
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

    game_status = "Press Start"

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # Handle keyboard input
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    dx, dy = 0, -CELL_SIZE
                elif event.key == pygame.K_DOWN:
                    dx, dy = 0, CELL_SIZE
                elif event.key == pygame.K_LEFT:
                    dx, dy = -CELL_SIZE, 0
                elif event.key == pygame.K_RIGHT:
                    dx, dy = CELL_SIZE, 0

        if game_status == "Press Start":
            action = handle_menu(screen)
            if action == "start":
                game_status = "Playing"
            elif action == "resume":
                game_status = "Playing"
                continue

        if game_status == "Playing":
            # Game logic goes here

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
            if head[0] < CELL_SIZE or head[0] >= SCREEN_WIDTH - CELL_SIZE or head[1] < CELL_SIZE or head[1] >= SCREEN_HEIGHT - CELL_SIZE:
                game_status = "Game Over"

            # Check for collision with the snake's body
            if len(set(snake)) != len(snake):
                game_status = "Game Failed"

            # Clear the screen
            screen.fill(BACKGROUND_COLOR)
            draw_wall(screen)

            # Draw the food
            pygame.draw.rect(screen, FOOD_COLOR, pygame.Rect(food[0], food[1], CELL_SIZE, CELL_SIZE))

            # Draw the snake
            draw_snake(screen, snake)

            # Render the score
            font = pygame.font.Font(None, 36)
            score_text = font.render(f"Score: {score}", True, (255, 255, 255))
            screen.blit(score_text, (10, 10))

        elif game_status == "Game Over":
            draw_menu(screen, "Game Over - Press Start")
            if handle_menu(screen) == "start":
                snake = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
                food = generate_food()
                dx, dy = CELL_SIZE, 0
                score = 0
                game_status = "Playing"

        elif game_status == "Game Failed":
            draw_menu(screen, "Game Failed - Press Start")
            if handle_menu(screen) == "start":
                snake = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
                food = generate_food()
                dx, dy = CELL_SIZE, 0
                score = 0
                game_status = "Playing"

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    snake_game()
