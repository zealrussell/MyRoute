import time
import pandas as pd

from src.Agent import Agent
from src.Env import Env

LONG = 7
START_PLACE = 1
MAZE_PLACE = 7
TIMES = 1000
STOP_FLAG = False
e = 1e-2

people = Agent(['left','right'], LONG)
site = Env(LONG, START_PLACE, MAZE_PLACE)
for episode in range(TIMES):
    state = site.get_observation()
    site.draw()
    time.sleep(0.2)

    while True:
        done = site.get_terminal()  # 判断当前环境是否到达最后
        if done:  # 如果到达，则初始化
            interaction = '\n第%s次episode，共使用步数：%s。' % (episode + 1, site.count)
            print(interaction)
            # 存储本次记录，计算与上次最大差值
            fileName = "../data/episode" + str(episode) + ".csv"
            people.qtable.to_csv(fileName)  # 将本次的q_table存储到本地文件中
            # print(f"\n第{episode}轮数据：\n{people.q_table}\n")
            if episode != 0:  # 第一轮不进行判断
                old_file_name = "../data/episode" + str(episode - 1) + ".csv"  # 读取上一次的q_table
                old_q_table = pd.read_csv(old_file_name, index_col=0)
                # print(f"\n第{episode - 1}轮数据：\n{old_q_table}\n")
                difference = (people.qtable - old_q_table).abs()
                # print(f"两次差值：\n{difference}\n")
                max_difference = difference.max().iloc[0] \
                    if difference.max().iloc[0] >= difference.max().iloc[0] else difference.max().iloc[1]
                # print(f"与上一次最大差值：\n{difference.max()}\n{difference.max()[0]},{difference.max()[1]}\n")
                print(f"最大差值：{max_difference}"
                      f"\n------{episode + 1}------")
                if max_difference <= e:  # 达到收敛条件
                    STOP_FLAG = True
                    break
            site.retry(START_PLACE)  # 初始化
            time.sleep(0.5)
            break
        action = people.choose_action(state)  # 获得下一步方向
        state_after, score, pre_done = site.get_target(action)  # 获得下一步的环境的实际情况
        people.learn(state, action, score, state_after, pre_done)  # 根据所处的当前环境对各个动作的预测得分和下一步的环境的实际情况更新当前环境的q表
        site.update_place(action)  # 更新位置
        state = state_after  # 状态更新
        site.draw()  # 更新画布
        time.sleep(0.2)
    if STOP_FLAG:
        break
print(people.qtable)
