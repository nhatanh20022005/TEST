import sys
from tkinter import font

import numpy as np
import random

import pygame


class FW_BK():
    def __init__(self, ma_tran):
        self.ma_tran = ma_tran
        self.dir = [(0, 1), (1, 0), (-1, 0), (0, -1)]
        self.simulation = []

    def _is_opposite(self, a, b):
        # a, b là tuple (dx, dy); bỏ qua nếu chưa có hướng (a == -1 hoặc b == -1)
        if a == -1 or b == -1:
            return False
        return a[0] == -b[0] and a[1] == -b[1]

    def forward_checking(self,x,y,value):
        Tap_Gia_Tri = []
        for k in self.dir:
            x_new, y_new = k[0] + x, k[1] + y
            if x_new < 12 and x_new >= 0 and y_new < 12 and y_new >= 0:
                if self.ma_tran[x_new][y_new] == 0 or (self.ma_tran[x_new][y_new] == value):
                    Tap_Gia_Tri.append((x_new, y_new))
        return Tap_Gia_Tri

    def init_Tap_Rang_Buoc(self, turn, x, y, value, huong_trc, huong_ht):
        if x < 12 and x >= 0 and y < 12 and y >= 0:
            if (self.ma_tran[x][y] == 0 or self.ma_tran[x][y] == value):
                if self._is_opposite(huong_trc, huong_ht):
                    return False
                turn += (0 if huong_trc == huong_ht else 1)
                if turn <= 2:
                    return True
        return False

    def FW_Backtracking(self,X_cur,X_goal,path,turn,visited,huong_ht,lan_lap = 0):
      if X_cur == X_goal:
          return path.copy()
      if lan_lap >  15:
          return None
      Tap_Gia_Tri = self.forward_checking(X_cur[0],X_cur[1],self.ma_tran[X_goal[0]][X_goal[1]])
      for (dx,dy) in Tap_Gia_Tri:
          if huong_ht == -1:
              huong_trc = -1
              huong_moi = (dx - X_cur[0], dy - X_cur[1])
          else:
              huong_trc = huong_ht
              huong_moi = (dx - X_cur[0], dy - X_cur[1])
          if  self.init_Tap_Rang_Buoc(turn,dx,dy,self.ma_tran[X_goal[0]][X_goal[1]],huong_trc,huong_moi) and (dx,dy) not in visited:
              new_turn = turn
              if (huong_trc != huong_moi):
                  new_turn += 1

              visited.add((dx, dy))
              path.append((dx, dy))
              lan_lap += 1
              self.simulation.append((X_cur, (dx, dy)))
              result = self.FW_Backtracking((dx,dy),X_goal,path,new_turn,visited,huong_moi,lan_lap)
              if result is not None:
                  return result
              lan_lap -=1
              path.pop()
              visited.remove((dx,dy))
      return None

    def Ve_Simulation(self, panel, color=(0, 255, 0)):

        for (start, end) in self.simulation:
            x1, y1 = start
            x2, y2 = end
            start_px = (y1 * 48 + 24, x1 * 48 + 24)
            end_px = (y2 * 48 + 24, x2 * 48 + 24)
            pygame.draw.line(panel, color, start_px, end_px, 4)

            mid_x = (start_px[0] + end_px[0]) // 2
            mid_y = (start_px[1] + end_px[1]) // 2



            pygame.display.update()











