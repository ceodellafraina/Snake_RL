import torch
import random
import numpy as np
from snake_game import SnakeGameAI
from dqn_agent import DQNAgent
from replay_memory import ReplayMemory

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.01 #rifare training con 0.01

def train():
    total_score = 0
    record = 0
    agent = DQNAgent(11, 256, 3, LR)
    memory = ReplayMemory(MAX_MEMORY)
    n_games = 0

    visualize = (n_games % 1000 == 0)
    game = SnakeGameAI(visualize=visualize)

    while True:
        state_old = agent.get_state(game)

        epsilon = max(0, 80 - n_games)
        final_move = agent.select_action(state_old, epsilon)

        reward, done, score = game.play_step(final_move)
        state_new = agent.get_state(game)

        memory.push((state_old, final_move, reward, state_new, done))

        if len(memory) > BATCH_SIZE:
            mini_sample = memory.sample(BATCH_SIZE)
            states, actions, rewards, next_states, dones = zip(*mini_sample)
            agent.train_step(states, actions, rewards, next_states, dones)


        if done:
            n_games += 1
            total_score += score
            if score > record:
                record = score
                agent.model.save()
            print('Game', n_games, 'Score', score, 'Record:', record)

            # Determina se visualizzare il prossimo episodio
            new_visualize = (n_games % 1000 == 0)
            if new_visualize != visualize:
                visualize = new_visualize
                game = SnakeGameAI(visualize=visualize)
            else:
                game.reset()

if __name__ == '__main__':
    train()
