import numpy as np
import pandas as pd
from sklearn.preprocessing import KBinsDiscretizer

class QLearningTrader:
    def __init__(self, bins=10, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.bins = bins
        self.alpha = alpha  # learning rate
        self.gamma = gamma  # discount factor
        self.epsilon = epsilon  # exploration
        self.q_table = {}  # state-action values

    def _discretize(self, short_ma, long_ma):
        # Convert continuous MAs into discrete bins for state representation
        diff = short_ma - long_ma
        return int(np.digitize(diff, bins=np.linspace(-10, 10, self.bins)))

    def _get_state(self, row):
        return self._discretize(row['sma_short'], row['sma_long'])

    def _choose_action(self, state):
        if np.random.rand() < self.epsilon or state not in self.q_table:
            return np.random.choice(['BUY', 'SELL', 'HOLD'])
        return max(self.q_table[state], key=self.q_table[state].get)

    def train(self, df: pd.DataFrame, episodes=10):
        df = df.copy()
        df['signal'] = 0  # Init

        for _ in range(episodes):
            position = 0
            buy_price = 0

            for i in range(len(df)):
                row = df.iloc[i]
                state = self._get_state(row)
                action = self._choose_action(state)

                reward = 0
                if action == 'BUY' and position == 0:
                    position = 1
                    buy_price = row['close']
                elif action == 'SELL' and position == 1:
                    reward = row['close'] - buy_price
                    position = 0
                elif action == 'HOLD':
                    reward = 0.01  # small reward for patience

                next_state = self._get_state(row)
                if state not in self.q_table:
                    self.q_table[state] = {'BUY': 0, 'SELL': 0, 'HOLD': 0}

                max_future_q = max(self.q_table.get(next_state, {'BUY': 0, 'SELL': 0, 'HOLD': 0}).values())
                self.q_table[state][action] += self.alpha * (reward + self.gamma * max_future_q - self.q_table[state][action])

        # After training, assign best action as signal
        signals = []
        for i in range(len(df)):
            row = df.iloc[i]
            state = self._get_state(row)
            if state in self.q_table:
                best_action = max(self.q_table[state], key=self.q_table[state].get)
                signal = 1 if best_action == 'BUY' else -1 if best_action == 'SELL' else 0
            else:
                signal = 0
            signals.append(signal)

        df['signal'] = signals
        return df
