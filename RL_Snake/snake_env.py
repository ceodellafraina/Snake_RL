import gym
import numpy as np
from gym import spaces
import random
import pygame
import sys

class SnakeEnv(gym.Env):
    """Custom Environment for Snake RL, compatible with Gym."""
    metadata = {'render.modes': ['human']}

    def __init__(self):
        super(SnakeEnv, self).__init__()
        # Dimensions of the game field
        self.width = 600
        self.height = 400
        self.cell_size = 20

        # Possible actions: [0: UP, 1: DOWN, 2: LEFT, 3: RIGHT]
        self.action_space = spaces.Discrete(4)

        # Observation: a state represented as a matrix
        # Includes the snake's position, food position, and collisions
        self.observation_space = spaces.Box(
            low=0,
            high=1,
            shape=(self.height // self.cell_size, self.width // self.cell_size),
            dtype=np.int32
        )

        # Initialize the state
        self.reset()

    def render(self, mode='human'):
        """Displays the game on screen with the score."""
        if not hasattr(self, "screen"):
            # Initialize Pygame only if not already initialized
            pygame.init()
            self.screen = pygame.display.set_mode((self.width, self.height))
            pygame.display.set_caption("RL Snake")
            self.font = pygame.font.SysFont("Arial", 24)  # Font for the score

        self.screen.fill((0, 0, 0))  # Black background

        # Draw the snake
        for segment in self.snake:
            pygame.draw.rect(
                self.screen, (0, 255, 0), (segment[0], segment[1], self.cell_size, self.cell_size)
            )

        # Draw the food
        pygame.draw.rect(
            self.screen, (255, 0, 0), (self.food[0], self.food[1], self.cell_size, self.cell_size)
        )

        # Display the score
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))  # Draw the score in the top left corner

        pygame.display.flip()

        # Handle close events (to avoid the window freezing)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def reset(self):
        """Resets the environment for a new episode."""
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.direction = (self.cell_size, 0)  # Initial movement to the right
        self.food = self._spawn_food()
        self.done = False
        self.score = 0

        return self._get_observation()

    def step(self, action):
        """Performs an action and updates the state."""
        if action == 0:  # UP
            if self.direction != (0, self.cell_size):
                self.direction = (0, -self.cell_size)
        elif action == 1:  # DOWN
            if self.direction != (0, -self.cell_size):
                self.direction = (0, self.cell_size)
        elif action == 2:  # LEFT
            if self.direction != (self.cell_size, 0):
                self.direction = (-self.cell_size, 0)
        elif action == 3:  # RIGHT
            if self.direction != (-self.cell_size, 0):
                self.direction = (self.cell_size, 0)

        # Calculate the distance from the food before moving
        old_distance = abs(self.snake[0][0] - self.food[0]) + abs(self.snake[0][1] - self.food[1])

        # Move the snake
        new_head = (self.snake[0][0] + self.direction[0], self.snake[0][1] + self.direction[1])
        self.snake.insert(0, new_head)

        # Check if the snake eats the food
        reward = 0
        if self.snake[0] == self.food:
            self.score += 1
            reward = 1  # Positive reward for eating food
            self.food = self._spawn_food()
        else:
            self.snake.pop()  # Remove the tail if no food is eaten

        # Calculate the distance from the food after moving
        new_distance = abs(self.snake[0][0] - self.food[0]) + abs(self.snake[0][1] - self.food[1])

        # Intermediate reward based on distance to the food
        if new_distance < old_distance:
            reward += 0.1  # Reward for getting closer
        else:
            reward -= 0.1  # Penalty for moving away

        # Check for collisions
        if (self.snake[0][0] < 0 or self.snake[0][0] >= self.width or
                self.snake[0][1] < 0 or self.snake[0][1] >= self.height or
                self.snake[0] in self.snake[1:]):
            self.done = True
            reward = -1  # Penalty for collision

        return self._get_observation(), reward, self.done, {}

    def close(self):
        """Closes the environment."""
        pygame.quit()

    def _spawn_food(self):
        """Generates food at a random position."""
        while True:
            x = random.randint(0, (self.width // self.cell_size) - 1) * self.cell_size
            y = random.randint(0, (self.height // self.cell_size) - 1) * self.cell_size
            if (x, y) not in self.snake:
                return (x, y)

    def _get_observation(self):
        """Creates a more informative representation of the state."""
        head_x, head_y = self.snake[0]
        food_x, food_y = self.food

        # Current direction of the snake
        direction_map = {
            (0, -self.cell_size): 0,  # UP
            (0, self.cell_size): 1,   # DOWN
            (-self.cell_size, 0): 2,  # LEFT
            (self.cell_size, 0): 3    # RIGHT
        }
        direction = direction_map[self.direction]

        # Distance to the food (normalized)
        dx = (food_x - head_x) / self.width
        dy = (food_y - head_y) / self.height

        # Imminent collisions
        danger_up = (head_y - self.cell_size < 0) or ((head_x, head_y - self.cell_size) in self.snake)
        danger_down = (head_y + self.cell_size >= self.height) or ((head_x, head_y + self.cell_size) in self.snake)
        danger_left = (head_x - self.cell_size < 0) or ((head_x - self.cell_size, head_y) in self.snake)
        danger_right = (head_x + self.cell_size >= self.width) or ((head_x + self.cell_size, head_y) in self.snake)

        collision_risks = [int(danger_up), int(danger_down), int(danger_left), int(danger_right)]

        # Final state as a vector
        return np.array([direction, dx, dy] + collision_risks, dtype=np.float32)
