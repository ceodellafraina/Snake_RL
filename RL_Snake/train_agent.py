import numpy as np
import random
from snake_env import SnakeEnv

# Q-Learning parameters
alpha = 0.01       # Learning rate
gamma = 0.9       # Discount factor
epsilon = 1,0     # Initial exploration probability
epsilon_decay = 0.9995  # Reduction of epsilon in each episode
epsilon_min = 0.01     # Minimum value of epsilon
num_episodes = 2000000   # Total number of episodes

# Function to discretize the state
def discretize_state(state):
    """Transforms the continuous state into a discrete one for the Q-table."""
    direction = int(state[0])  # Snake's direction
    dx = int((state[1] + 1) * 5)  # Transform from [-1, 1] to [0, 10]
    dy = int((state[2] + 1) * 5)  # Same for dy

    collision_risks = tuple(map(int, state[3:7]))  # Binary collision risks

    # Return the discretized state as a tuple
    return (direction, dx, dy) + collision_risks

# Initialize the Snake environment
env = SnakeEnv()

# Initialize the Q-Table as a dictionary
try:
    q_table = np.load("last2.npy", allow_pickle=True).item()
    print("Q-Table loaded successfully.")
except FileNotFoundError:
    q_table = {}

# Function to choose an action using epsilon-greedy
def choose_action(state):
    """
    Choose an action based on the epsilon-greedy strategy.
    """
    state_key = tuple(state)  # Convert the state to a tuple for the Q-Table
    if random.uniform(0, 1) < epsilon:  # Exploration
        return env.action_space.sample()
    else:  # Exploitation
        if state_key not in q_table:
            q_table[state_key] = [0] * env.action_space.n
        return np.argmax(q_table[state_key])

# Main loop for training
for episode in range(num_episodes):
    state = discretize_state(env.reset())
    total_reward = 0

    while True:
        # Epsilon-greedy policy
        if np.random.rand() < epsilon:
            action = env.action_space.sample()  # Explore
        else:
            action = np.argmax([q_table.get(state + (a,), 0) for a in range(env.action_space.n)])

        # Execute the action
        next_state, reward, done, _ = env.step(action)
        next_state = discretize_state(next_state)

        # Update the Q-table
        best_next_action = np.max([q_table.get(next_state + (a,), 0) for a in range(env.action_space.n)])
        q_table[state + (action,)] = q_table.get(state + (action,), 0) + alpha * (
            reward + gamma * best_next_action - q_table.get(state + (action,), 0)
        )

        state = next_state
        total_reward += reward

        if done:
            break

    # Reduce epsilon
    epsilon = max(epsilon_min, epsilon * epsilon_decay)

    # Log every 100 episodes
    if episode % 100 == 0:
        print(f"Episode {episode}: Total reward: {total_reward} Epsilon: {epsilon}")

# Close the environment
env.close()

# Save the Q-Table to a file
np.save("last2.npy", q_table)

print("Training completed! Q-Table saved in 'final2_q_table.npy'.")

