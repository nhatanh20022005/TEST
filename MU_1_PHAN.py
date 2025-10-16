import heapq
from collections import deque
import numpy as np
import random
import pygame


class MU_1_PHAN():
    def __init__(self, ma_tran):
        self.ma_tran = ma_tran

    def KhoiTao_NiemTin_1_P(self, start, pham_vi=2):
        agent_map = [[-1] * 12 for _ in range(12)]  # -1: chưa biết
        niemtin = {}

        x, y = start
        for i in range(1, 11):
            for j in range(1, 11):
                if abs(i - x) <= pham_vi and abs(j - y) <= pham_vi:
                    agent_map[i][j] = self.ma_tran[i][j]
                    if self.ma_tran[i][j] == 0:
                        niemtin[(i, j)] = set()
                    else:
                        niemtin[(i, j)] = {self.ma_tran[i][j]}
                else:
                    niemtin[(i, j)] = set()
        return agent_map, niemtin

    def Quan_Sat_1_P(self, agent_map, x, y, pham_vi=2):
        danh_sach_thay_doi = []
        for dx in range(-pham_vi, pham_vi + 1):
            for dy in range(-pham_vi, pham_vi + 1):
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(self.ma_tran) and 0 <= ny < len(self.ma_tran[0]):
                    if agent_map[nx][ny] != self.ma_tran[nx][ny]:
                        agent_map[nx][ny] = self.ma_tran[nx][ny]
                        danh_sach_thay_doi.append((nx, ny))
        return danh_sach_thay_doi

    def Co_The_An_BFS(self, agent_map, p1, p2, niemtin):
        dir = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        x1, y1 = p1
        x2, y2 = p2
        queue = deque()
        visited = set()
        initial_state = (x1, y1, frozenset(niemtin.get((x1, y1), set())), -1, 0)
        queue.append(initial_state)
        visited.add((x1, y1, frozenset(niemtin.get((x1, y1), set())), -1, 0))

        while queue:
            x, y, belief_set, huong, re = queue.popleft()

            if (x, y) == (x2, y2) and re <= 2:
                return True

            for idx, (dx, dy) in enumerate(dir):
                x_new, y_new = x + dx, y + dy
                if 0 <= x_new < 12 and 0 <= y_new < 12:
                    if (agent_map[x_new][y_new] == 0 or (x_new, y_new) == (x2, y2)) and agent_map[x_new][y_new] != -1:
                        new_belief_set = frozenset(niemtin.get((x_new, y_new), set()))
                        new_re = re + (0 if huong == idx or huong == -1 else 1)
                        if new_re <= 2:
                            new_state = (x_new, y_new, new_belief_set, idx, new_re)

                            if new_state not in visited:
                                visited.add(new_state)
                                queue.append(new_state)

        return False






