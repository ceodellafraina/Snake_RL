import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Basic config
WIDTH, HEIGHT = 600, 400  # window dimensions
CELL_SIZE = 20  # cells dimensions
FPS = 10  # fps

# colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# score Font
FONT = pygame.font.Font(None, 36)

# initializing window game
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake RL")

# clock
clock = pygame.time.Clock()


# main function
def main():
    # snake initial status
    snake = [(100, 100), (80, 100), (60, 100)]  # starting coordinates
    direction = (CELL_SIZE, 0)  # starts moving to the right
    food = spawn_food(snake)

    score = 0  # score

    while True:
        # event management
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # keyboard input control
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and direction != (0, CELL_SIZE):  # avoid to go back
            direction = (0, -CELL_SIZE)
        if keys[pygame.K_DOWN] and direction != (0, -CELL_SIZE):
            direction = (0, CELL_SIZE)
        if keys[pygame.K_LEFT] and direction != (CELL_SIZE, 0):
            direction = (-CELL_SIZE, 0)
        if keys[pygame.K_RIGHT] and direction != (-CELL_SIZE, 0):
            direction = (CELL_SIZE, 0)

        # snake movements
        new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
        snake.insert(0, new_head)

        # food collision control
        if snake[0] == food:
            score += 1
            food = spawn_food(snake)
        else:
            snake.pop()  # remove tail if he didn't eat

        # collision with borders or himself
        if (snake[0][0] < 0 or snake[0][0] >= WIDTH or
                snake[0][1] < 0 or snake[0][1] >= HEIGHT or
                snake[0] in snake[1:]):
            print(f"Game Over! Punteggio: {score}")
            pygame.quit()
            sys.exit()

        # draw all on the screen
        screen.fill(BLACK)
        draw_snake(snake)
        draw_food(food)
        draw_score(score)
        pygame.display.flip()

        # game speed control
        clock.tick(FPS)


# draw snake
def draw_snake(snake):
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (segment[0], segment[1], CELL_SIZE, CELL_SIZE))


# draw food
def draw_food(food):
    pygame.draw.rect(screen, RED, (food[0], food[1], CELL_SIZE, CELL_SIZE))


# random food spawn
def spawn_food(snake):
    while True:
        x = random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE
        y = random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE
        if (x, y) not in snake:  # make sure food doesn't spawn on snake
            return (x, y)

# draw score
def draw_score(score):
    score_text = FONT.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10)) 

# start game
if __name__ == "__main__":
    main()
