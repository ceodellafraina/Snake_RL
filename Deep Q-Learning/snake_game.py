import pygame
import random
import numpy as np

class SnakeGameAI:
    def __init__(self, w=640, h=480, visualize=True):
        self.w = w
        self.h = h
        self.block_size = 20
        self.speed = 40
        self.visualize = visualize

        if self.visualize:
            pygame.init()
            self.display = pygame.display.set_mode((self.w, self.h))
            pygame.display.set_caption('Snake AI')
            self.clock = pygame.time.Clock()

        self.reset()

    def reset(self):
        self.direction = 0  # 0: right, 1: left, 2: up, 3: down
        self.head = [self.w / 2, self.h / 2]
        self.snake = [self.head[:], [self.head[0] - self.block_size, self.head[1]],
                      [self.head[0] - (2 * self.block_size), self.head[1]]]
        self.score = 0
        self.food = None
        self.place_food()
        self.frame_iteration = 0

    def place_food(self):
        x = random.randint(0, (self.w - self.block_size) // self.block_size) * self.block_size
        y = random.randint(0, (self.h - self.block_size) // self.block_size) * self.block_size
        self.food = [x, y]
        if self.food in self.snake:
            self.place_food()

    def play_step(self, action):
        self.frame_iteration += 1

        if self.visualize:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

        self.move(action)
        self.snake.insert(0, self.head[:])

        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration > 100 * len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score

        if self.head == self.food:
            self.score += 1
            reward = 10
            self.place_food()
        else:
            self.snake.pop()

        if self.visualize:
            self.update_ui()
            self.clock.tick(self.speed)

        return reward, game_over, self.score

    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        if pt[0] > self.w - self.block_size or pt[0] < 0 or pt[1] > self.h - self.block_size or pt[1] < 0:
            return True
        if pt in self.snake[1:]:
            return True
        return False

    def update_ui(self):
        self.display.fill((0, 0, 0))

        for pt in self.snake:
            pygame.draw.rect(self.display, (0, 255, 0), pygame.Rect(pt[0], pt[1], self.block_size, self.block_size))

        pygame.draw.rect(self.display, (255, 0, 0), pygame.Rect(self.food[0], self.food[1], self.block_size, self.block_size))

        pygame.display.flip()

    def move(self, action):
        clock_wise = [0, 2, 1, 3]  # right, up, left, down
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx]  # no change
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx]  # right turn
        else:  # [0, 0, 1]
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx]  # left turn

        self.direction = new_dir

        x, y = self.head
        if self.direction == 0:
            x += self.block_size
        elif self.direction == 1:
            x -= self.block_size
        elif self.direction == 2:
            y -= self.block_size
        elif self.direction == 3:
            y += self.block_size

        self.head = [x, y]
