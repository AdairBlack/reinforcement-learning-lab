import flappy_bird_gymnasium
import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.monitor import Monitor
import datetime

# Create and wrap the environment
env = gym.make("FlappyBird-v0", render_mode="human", use_lidar=True)
env = Monitor(env)
env = DummyVecEnv([lambda: env])

device = 'cpu'
print(f"Using device: {device}")

# Initialize the PPO algorithm
model = PPO("MlpPolicy", env, verbose=1, device=device)

# Train the agent
print("Training the agent...")
for _ in range(10):
    model.learn(total_timesteps=1e3, progress_bar=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    print(f"Saving model to flappy_bird_model_ppo_{timestamp}")
    model.save(f"flappy_bird_model_ppo_{timestamp}")
    print("Model saved.")

print("Training complete.")
