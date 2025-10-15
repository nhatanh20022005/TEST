import heapq
from collections import deque
import numpy as np
import random
import pygame



class MU_TOAN_PHAN():
    def __init__(self,ma_tran):
        self.ma_tran = ma_tran


    def KhoiTao_NiemTin_Non(self, max_loai=10):
        niemtin = {}
        tat_ca_loai = set(range(1, max_loai + 1))
        for i in range(1, 11):
            for j in range(1, 11):
                if self.ma_tran[i][j] == 0:
                    niemtin[(i, j)] = set()
                else:
                    niemtin[(i, j)] = set(tat_ca_loai)
        return niemtin

    def Quan_Sat(self,agent_map,  x, y, pham_vi=2):
        thay_doi = []
        for dx in range(-pham_vi, pham_vi + 1):
            for dy in range(-pham_vi, pham_vi + 1):
                x_new, y_new = x + dx, y + dy
                if 0 <= x_new < len(self.ma_tran) and 0 <= y_new < len(self.ma_tran[0]):
                    if agent_map[x_new][y_new] != self.ma_tran[x_new][y_new]:
                        agent_map[x_new][y_new] = self.ma_tran[x_new][y_new]
                        thay_doi.append((x_new, y_new))
        return thay_doi

    def Cap_Nhat_Niem_Tin_Sau_Quan_Sat(self,niemtin, agent_map, danh_sach_quan_sat):
        for (x_new, y_new) in danh_sach_quan_sat:
            val = agent_map[x_new][y_new]
            if val == 0:
                niemtin[(x_new, y_new)] = set()
            else:
                niemtin[(x_new, y_new)] = {val}

    def Doan_Cap_Tu_Niem_Tin(self,niemtin):
        cac_gia_tri = {}
        for pos, tap in niemtin.items():
            for v in tap:
                if v == 0:
                    continue
                cac_gia_tri.setdefault(v, []).append(pos)

        cac_v_kha_thi = [v for v, lst in cac_gia_tri.items() if len(lst) >= 2]
        if not cac_v_kha_thi:
            return None, None, None
        v = random.choice(cac_v_kha_thi)
        pos_list = cac_gia_tri[v]
        p1, p2 = random.sample(pos_list, 2)
        return v, p1, p2

    def Co_The_An_BFS(self,agent_map, p1, p2, niemtin):
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

    def Cap_Kha_Nang_An(self,niemtin):
        counts = {}
        for pos, tap in niemtin.items():
            for v in tap:
                if v != 0:
                    counts[v] = counts.get(v, 0) + 1
        for v, c in counts.items():
            if c >= 2:
                return True
        return False



