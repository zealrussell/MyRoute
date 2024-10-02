import numpy as np
from queue import Queue
import random
import matplotlib.pyplot as plt

network_topology = [[1, 6], [0, 2, 7], [1, 8], [4, 9], [3, 5, 10], [4, 11], [0, 7, 12], [1, 6, 8, 13], [2, 7, 14],
                    [3, 10, 15], [4, 9, 11, 16], [5, 10, 17], [6, 13, 18], [7, 12, 14, 19], [8, 13, 20], [9, 16, 21],
                    [10, 15, 17, 22], [11, 16, 23], [12, 19, 24], [13, 18, 20, 25], [14, 19, 21, 26], [15, 20, 22, 27],
                    [16, 21, 23, 28], [17, 22, 29], [18, 30], [19, 26], [20, 25], [21, 28], [22, 27], [23, 35],
                    [24, 31], [30, 32], [31, 33], [32, 34], [33, 35], [29, 34]]
packet_list = []  # 存储所有的数据包信息
node_list = []  # 存储每个节点的数据包，用队列
Q_table = []
liveNodeList = []  # 还没有到大目的地数据包的index
avgNodes = 0  # 用于计算平均时延
avgTimes = 0  # 用于计算平均时延
avgList = []  # 用于存储平均时延
avgCount = 0
time_count = 0
greed_rate = 1
learn_rate = 0.6
lamda = 1
max_time = 16000
poisson_list = np.random.poisson(lam=lamda, size=max_time)

for i in range(36):
    Q_table.append(np.ones((36, 36)))

for i in range(36):
    node_list.append(Queue(maxsize=0))


def getNewPackets(currenttime):  # 每个模拟时间中产生对应的数据包
    packets_list = []
    packets_count = poisson_list[currenttime]
    for x in range(packets_count):
        nodes = random.sample(range(0, 36), 2)
        new_node = [nodes[0], nodes[1], nodes[0], 0, 0, 0]
        packets_list.append(new_node)
    return packets_list


def getQueueTime():  # 获得本次排队时间
    return 0


while time_count < max_time:
    packets = getNewPackets(time_count)  # 生成数据包
    if len(packets) > 0:
        for packet in packets:
            liveNodeList.append(len(packet_list))
            node_list[packet[0]].put(len(packet_list))
            packet_list.append(packet)

    for node_index in range(len(node_list)):  # 数据包传输，更新Q表
        if not node_list[node_index].empty():
            packet_index = node_list[node_index].get()
            if not node_list[node_index].empty():
                for livenode in liveNodeList:
                    if livenode != packet_index and packet_list[livenode][2] == node_index:
                        packet_list[livenode][3] += 1
                        packet_list[livenode][4] += 1
            packet = packet_list[packet_index]
            pnode = packet[2]
            ptime = packet[3]
            dst = packet[1]
            ptable = Q_table[pnode]
            if random.random() > greed_rate:  # 随机选择一个动作
                random_index = np.random.randint(0, len(network_topology[pnode]))
                next_node = network_topology[pnode][random_index]
            else:  # 选取奖赏值最大的动作
                minq = 99999
                for i in network_topology[pnode]:
                    if ptable[dst, i] <= minq:
                        minq = ptable[dst, i]
                        next_node = i
            if next_node == dst:  # 选择下一个节点到目的节点最小的最小延迟
                next_ninq = 0
            else:
                next_table = Q_table[next_node]
                next_ninq = 99999
                for i in network_topology[next_node]:
                    if next_table[dst, i] <= next_ninq:
                        next_ninq = next_table[dst, i]
            newQ = (1 - learn_rate) * ptable[dst, next_node] + learn_rate * (packet[3] + 1 + next_ninq)
            Q_table[pnode][dst, next_node] = newQ
            if next_node == dst:  # 修改相关包的信息，将数据包入队列
                packet_list[packet_index][2] = dst
                packet_list[packet_index][3] = 0
                packet_list[packet_index][4] += 1
                packet_list[packet_index][5] = 1
                avgNodes += 1
                avgTimes += packet_list[packet_index][4]
                liveNodeList.remove(packet_index)
            else:
                packet_list[packet_index][2] = next_node
                packet_list[packet_index][3] = 0
                packet_list[packet_index][4] += 1
                node_list[next_node].put(packet_index)
    time_count += 1
    avgCount += 1
    if avgCount == 200:
        avgCount = 0
        avgList.append(avgTimes / avgNodes)

print(Q_table)
plt.plot(range(len(avgList)), avgList)
plt.show()