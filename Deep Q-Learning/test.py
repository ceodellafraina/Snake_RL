import pygame
import torch
from snake_game import SnakeGameAI
from dqn_agent import DQNAgent

def test():
    agent = DQNAgent(11, 256, 3, 0)
    agent.model.load_state_dict(torch.load('model2.pth'))
    agent.model.eval()

    game = SnakeGameAI()

    while True:
        state = agent.get_state(game)
        final_move = agent.select_action(state, epsilon=0)
        reward, done, score = game.play_step(final_move)

        if done:
            game.reset()

if __name__ == '__main__':
    test()
