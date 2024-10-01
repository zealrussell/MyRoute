import pandas as pd
import numpy as np

class Agent:
    def __init__(self, actions, long, learning_rate = 0.5, reward_decay=0.9, e_greedy=0.9):
        self.actions = actions
        self.lr = learning_rate
        self.gamma = reward_decay
        self.qtable = pd.DataFrame()
        for i in range(long):
            line_table = pd.Series(
                [0.0,0.0],
                name=i,
                index=actions
            )
            line_table_2_frame = line_table.to_frame()
            self.qtable = pd.concat([self.qtable, line_table_2_frame.T])
    def choose_action(self, observation):
        # 取出当前方向
        action_list = self.qtable.loc[observation,:]
        action = np.random.choice(action_list[action_list == np.max(action_list)].index)
        return action

    def learn(self, observation_now, action, score, observation_after, done):
        q_predict = self.qtable.loc[observation_now, action]
        if done:
            q_target = score
        else:
            q_target = score + self.gamma * self.qtable.loc[observation_after,:].max()

        self.qtable.loc[observation_now, action] += self.lr * (q_target-q_predict);
