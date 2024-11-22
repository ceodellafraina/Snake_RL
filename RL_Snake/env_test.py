from snake_env import SnakeEnv

# Crea un'istanza dell'ambiente
env = SnakeEnv()

# Reset dell'ambiente
observation = env.reset()

print("Osservazione iniziale:")
print(observation)

done = False
while not done:
    action = env.action_space.sample()  # Azione casuale
    observation, reward, done, info = env.step(action)

    print("Reward:", reward)
    env.render()

env.close()
