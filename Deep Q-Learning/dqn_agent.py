import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import random
import os

class LinearQNet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(LinearQNet, self).__init__()
        self.linear1 = nn.Linear(input_size, hidden_size)
        self.linear2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = F.relu(self.linear1(x))
        x = self.linear2(x)
        return x

    def save(self, file_name='model2.pth'):
        model_folder_path = './'
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)
        torch.save(self.state_dict(), model_folder_path + file_name)

class DQNAgent:
    def __init__(self, input_size, hidden_size, output_size, lr):
        self.model = LinearQNet(input_size, hidden_size, output_size)
        self.optimizer = optim.Adam(self.model.parameters(), lr=lr)
        self.gamma = 0.9

    def get_state(self, game):
        head = game.snake[0]
        point_l = [head[0] - game.block_size, head[1]]
        point_r = [head[0] + game.block_size, head[1]]
        point_u = [head[0], head[1] - game.block_size]
        point_d = [head[0], head[1] + game.block_size]

        dir_l = game.direction == 1
        dir_r = game.direction == 0
        dir_u = game.direction == 2
        dir_d = game.direction == 3

        state = [
            # Danger straight
            (dir_r and game.is_collision(point_r)) or
            (dir_l and game.is_collision(point_l)) or
            (dir_u and game.is_collision(point_u)) or
            (dir_d and game.is_collision(point_d)),

            # Danger right
            (dir_u and game.is_collision(point_r)) or
            (dir_d and game.is_collision(point_l)) or
            (dir_l and game.is_collision(point_u)) or
            (dir_r and game.is_collision(point_d)),

            # Danger left
            (dir_d and game.is_collision(point_r)) or
            (dir_u and game.is_collision(point_l)) or
            (dir_r and game.is_collision(point_u)) or
            (dir_l and game.is_collision(point_d)),

            # Move direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,

            # Food location
            game.food[0] < game.head[0],  # food left
            game.food[0] > game.head[0],  # food right
            game.food[1] < game.head[1],  # food up
            game.food[1] > game.head[1]   # food down
        ]

        return torch.tensor(state, dtype=torch.float)

    def select_action(self, state, epsilon):
        if random.uniform(0, 1) < epsilon:
            move = random.randint(0, 2)
            final_move = [0, 0, 0]
            final_move[move] = 1
        else:
            state0 = state.unsqueeze(0)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move = [0, 0, 0]
            final_move[move] = 1
        return final_move


    def train_step(self, state, action, reward, next_state, done):
        # Impila gli stati
        state = torch.stack(state)
        next_state = torch.stack(next_state)
        action = torch.tensor(action, dtype=torch.float)
        reward = torch.tensor(reward, dtype=torch.float)
        done = torch.tensor(done, dtype=torch.bool)

        # Predizioni del modello per lo stato corrente
        pred = self.model(state)  # Shape: [batch_size, output_size]

        # Ottieni i valori Q per le azioni intraprese
        action_indices = torch.argmax(action, dim=1).unsqueeze(1)
        pred = pred.gather(1, action_indices)  # Shape: [batch_size, 1]

        # Predizioni per lo stato successivo
        next_pred = self.model(next_state)
        max_next_pred = torch.max(next_pred, dim=1)[0]

        # Calcola il target Q value
        target = reward + self.gamma * max_next_pred * (~done)
        target = target.unsqueeze(1)  # Shape: [batch_size, 1]

        # Ottimizzazione del modello
        self.optimizer.zero_grad()
        loss = F.mse_loss(pred, target)
        loss.backward()
        self.optimizer.step()


