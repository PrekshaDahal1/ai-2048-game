import random
import numpy as np

class QTrainer:
    def __init__(self, learning_rate=0.1, discount=0.9, epsilon=1.0, epsilon_decay=0.995):
        self.q_table = {}
        self.lr = learning_rate
        self.gamma = discount
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.actions = ['Up', 'Down', 'Left', 'Right']

    def get_state_key(self, board):
        return tuple(tuple(row) for row in board)

    def choose_action(self, state):
        if random.random() < self.epsilon or state not in self.q_table:
            return random.choice(self.actions)
        return self.actions[np.argmax(self.q_table[state])]

    def update_q(self, state, action, reward, next_state, done):
        if state not in self.q_table:
            self.q_table[state] = [0] * 4
        if next_state not in self.q_table:
            self.q_table[next_state] = [0] * 4

        idx = self.actions.index(action)
        max_future_q = max(self.q_table[next_state])
        current_q = self.q_table[state][idx]
        target_q = reward + self.gamma * max_future_q * (not done)
        self.q_table[state][idx] += self.lr * (target_q - current_q)

    def decay_epsilon(self):
        self.epsilon *= self.epsilon_decay
