import numpy as np
import time
from snake_env import SnakeEnv

# Load Q-Table
q_table = np.load("final.npy", allow_pickle=True).item()

# Discretize state (same as training)
def discretize_state(state):
    """Transforms the continuous state into a discrete one for the Q-table."""
    direction = int(state[0])  # Snake's direction
    dx = int((state[1] + 1) * 5)  # Transform from [-1, 1] to [0, 10]
    dy = int((state[2] + 1) * 5)  # Same for dy

    collision_risks = tuple(map(int, state[3:7]))  # Binary collision risks

    # Return the discretized state as a tuple
    return (direction, dx, dy) + collision_risks

# Function to select an action based on the Q-Table
def choose_action(state):
    state_key = tuple(state)  # Ensure it is a tuple
    if state_key in q_table:
        return np.argmax(q_table[state_key])  # Action with the highest value in the Q-Table
    else:
        return env.action_space.sample()  # If not found, explore randomly

# Initialize the environment
env = SnakeEnv()

# Number of episodes for evaluation
num_episodes = 10
total_rewards = []

for episode in range(num_episodes):
    state = discretize_state(env.reset())
    score = 0

    while True:
        # Best action based on the Q-table
        action = np.argmax([q_table.get(state + (a,), 0) for a in range(env.action_space.n)])
        next_state, reward, done, _ = env.step(action)
        next_state = discretize_state(next_state)
        state = next_state

        if reward > 0:
            score += 1

        # Add rendering to visualize the game
        env.render()
        time.sleep(0.01)  # Delay the update to observe the game

        if done:
            break

    total_rewards.append(score)
    print(f"Episode {episode + 1}, Score: {score}")

# Close the environment to avoid graphical issues
env.close()

# Final statistics
print(f"Average score over {num_episodes} episodes: {np.mean(total_rewards)}")
print(f"Maximum score over {num_episodes} episodes: {np.max(total_rewards)}")