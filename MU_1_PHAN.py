import heapq
from collections import deque
import numpy as np
import random
import pygame



class MU_1_PHAN():
    def __init__(self,ma_tran):
        self.ma_tran = ma_tran


    def KhoiTao_NiemTin_1_P( self,start, pham_vi=2):
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

    def Quan_Sat_1_P(self,agent_map, x, y, pham_vi=2):
        danh_sach_thay_doi = []
        for dx in range(-pham_vi, pham_vi + 1):
            for dy in range(-pham_vi, pham_vi + 1):
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(self.ma_tran) and 0 <= ny < len(self.ma_tran[0]):
                    if agent_map[nx][ny] != self.ma_tran[nx][ny]:
                        agent_map[nx][ny] = self.ma_tran[nx][ny]
                        danh_sach_thay_doi.append((nx, ny))
        return danh_sach_thay_doi


    



