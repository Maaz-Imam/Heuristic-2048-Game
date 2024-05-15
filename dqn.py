import tensorflow as tf
import numpy as np
import random
import copy
from grid import Grid

class DQNAgent:
    def __init__(self, state_size, action_size, learning_rate=0.001, discount_factor=0.99, epsilon=1.0, epsilon_decay=0.995, min_epsilon=0.01):
        self.state_size = state_size
        self.action_size = action_size
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.min_epsilon = min_epsilon

        self.action_map = {0: 'w', 1: 'a', 2: 's', 3: 'd'}

        # Create the Q-network and target network
        self.model = self.build_model()
        self.target_model = self.build_model()
        self.update_target_model()

        # Initialize replay memory
        self.replay_memory = []
        self.batch_size = 64  # Increase batch size

    def build_model(self):
        model = tf.keras.Sequential([
            tf.keras.layers.Input(shape=(self.state_size,), name='input_layer'),
            tf.keras.layers.Dense(128, activation='relu'),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dense(self.action_size, activation='linear')
        ])
        model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=self.learning_rate), loss='mse')
        return model

    def update_target_model(self):
        self.target_model.set_weights(self.model.get_weights())

    def choose_action(self, state):
        state_flat = np.array(state).flatten()  # Flatten the state
        if np.random.rand() <= self.epsilon:
            # Random action (exploration)
            return np.random.choice(self.action_size)
        else:
            # Choose action based on Q-values from the network (exploitation)
            q_values = self.model.predict(np.expand_dims(state_flat, axis=0))[0]
            return np.argmax(q_values)

    def replay(self):
        if len(self.replay_memory) < self.batch_size:
            return

        # Sample minibatch from replay memory
        minibatch = random.sample(self.replay_memory, self.batch_size)

        states = []
        targets = []
        for state, action, reward, next_state, done in minibatch:
            state_flat = np.array(state).flatten()  # Flatten the state
            next_state_flat = np.array(next_state).flatten()  # Flatten the next state

            target = reward
            if not done:
                # Calculate target using Double Q-Learning
                next_q_values = self.model.predict(np.expand_dims(next_state_flat, axis=0))[0]
                next_action = np.argmax(next_q_values)
                target = reward + self.discount_factor * self.target_model.predict(np.expand_dims(next_state_flat, axis=0))[0][next_action]

            # Get current Q-values
            target_full = self.model.predict(np.expand_dims(state_flat, axis=0))[0]
            target_full[action] = target  # Use the action index directly

            states.append(state_flat)
            targets.append(target_full)

        # Train the Q-network
        self.model.fit(np.array(states), np.array(targets), epochs=1, verbose=0)

        # Update target model periodically
        if len(self.replay_memory) % 1000 == 0:
            self.update_target_model()

        # Decay epsilon
        if self.epsilon > self.min_epsilon:
            self.epsilon *= self.epsilon_decay

    def remember(self, state, action, reward, next_state, done):
        self.replay_memory.append((state, action, reward, next_state, done))

    def load(self, model_path):
        self.model.load_weights(model_path)
        self.update_target_model()

    def save(self, model_path):
        self.model.save_weights(model_path)

# Initialize the DQNAgent
state_size = 16  # Assuming the game state is represented as a flattened 4x4 grid
action_size = 4  # Actions: 'w', 's', 'a', 'd'
agent = DQNAgent(state_size, action_size)
env = Grid(4)

# Training loop (interacting with the game environment)
num_episodes = 1000
for episode in range(num_episodes):
    state = env.reset()
    total_reward = 0
    done = False

    while not done:
        action_idx = agent.choose_action(state)
        action = agent.action_map[action_idx]  
        print("-->", action)

        next_state, reward, done = env.step(action)  
        agent.remember(state, action_idx, reward, next_state, done)
        state = next_state
        total_reward += reward
        env.render()

        agent.replay()  # Train the agent by replaying experiences from the replay memory

    print(f"Episode: {episode + 1}, Total Reward: {total_reward}")

    if (episode + 1) % 10 == 0:
        agent.save(f'dqn_model_{episode + 1}.h5')
