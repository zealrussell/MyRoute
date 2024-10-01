# -*- coding: utf-8 -*-
"""
@Project ：Q_learn
@File ：Env.py
@Author ：Hao
@Date ：2022-09-10 010 8:38
"""
import numpy as np

class Env:
    def __init__(self, column, start_colum, maze_column):
        self.column = column  # 表示地图的长度
        self.maze_column = maze_column - 1  # 宝藏所在的位置
        self.x = start_colum  # 初始化x
        self.map = np.arange(column)  # 给予每个地点一个标号
        self.count = 0  # 用于记录一共走了多少步

    # 生成图像
    def draw(self):
        a = []
        for j in range(self.column):  # 更新图画
            if j == 0:
                a.append('x')
            elif j == self.x:
                a.append('o')
            elif j == self.maze_column:
                a.append('m')
            else:
                a.append('_')
        interaction = ''.join(a)
        print('\r{}'.format(interaction), end='')

    # 获取所在位置
    def get_observation(self):
        return self.map[self.x]  # 返回现在所在位置

    # 是否已到达终点
    def get_terminal(self):
        if self.x == self.maze_column:  # 如果得到了宝藏，则返回已经完成
            done = True
        elif self.x == 0:  # 如果掉入左边边缘，失败，-1
            done = True
        else:
            done = False
        return done

    # 更新当前位置
    def update_place(self, action):
        self.count += 1  # 更新的时候表示已经走了一步
        if action == 'right':
            if self.x < self.column - 1:
                self.x += 1
        elif action == 'left':  # left
            if self.x > 0:
                self.x -= 1

    # 获得下一步的环境的实际情况
    def get_target(self, action):
        if action == 'right':  # 获得下一步的环境的实际情况
            if self.x + 1 == self.maze_column:
                score = 1
                pre_done = True
            else:
                score = 0
                pre_done = False
            return self.map[self.x + 1], score, pre_done
        elif action == 'left':  # left
            if self.x - 1 == self.maze_column:
                score = 1
                pre_done = True
            elif self.x - 1 == 0:
                score = -1
                pre_done = True
            else:
                score = 0
                pre_done = False
            return self.map[self.x - 1], score, pre_done

    # 初始化，位置0，计数器归零
    def retry(self, start_colum):  # 初始化
        self.x = start_colum
        self.count = 0