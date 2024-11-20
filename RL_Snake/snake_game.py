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

        # Controllo input da tastiera
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and direction != (0, CELL_SIZE):  # Evita di tornare indietro
            direction = (0, -CELL_SIZE)
        if keys[pygame.K_DOWN] and direction != (0, -CELL_SIZE):
            direction = (0, CELL_SIZE)
        if keys[pygame.K_LEFT] and direction != (CELL_SIZE, 0):
            direction = (-CELL_SIZE, 0)
        if keys[pygame.K_RIGHT] and direction != (-CELL_SIZE, 0):
            direction = (CELL_SIZE, 0)

        # Movimento del serpente
        new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
        snake.insert(0, new_head)

        # Controllo collisione con cibo
        if snake[0] == food:
            score += 1
            food = spawn_food(snake)
        else:
            snake.pop()  # Rimuove la coda se non ha mangiato

        # Controllo collisioni con bordi o se stesso
        if (snake[0][0] < 0 or snake[0][0] >= WIDTH or
                snake[0][1] < 0 or snake[0][1] >= HEIGHT or
                snake[0] in snake[1:]):
            print(f"Game Over! Punteggio: {score}")
            pygame.quit()
            sys.exit()

        # Disegna tutto sullo schermo
        screen.fill(BLACK)
        draw_snake(snake)
        draw_food(food)
        pygame.display.flip()

        # Controlla la velocità del gioco
        clock.tick(FPS)


# Funzione per disegnare il serpente
def draw_snake(snake):
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (segment[0], segment[1], CELL_SIZE, CELL_SIZE))


# Funzione per disegnare il cibo
def draw_food(food):
    pygame.draw.rect(screen, RED, (food[0], food[1], CELL_SIZE, CELL_SIZE))


# Funzione per generare cibo in una posizione casuale
def spawn_food(snake):
    while True:
        x = random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE
        y = random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE
        if (x, y) not in snake:  # Assicurati che il cibo non appaia sul serpente
            return (x, y)


# Avvia il gioco
if __name__ == "__main__":
    main()
