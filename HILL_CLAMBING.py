import numpy as np
import random
import heapq


import math

import pygame


class HILL_CLAMBING():
    def __init__(self,ma_tran):
        self.ma_tran = ma_tran
        self.lan_vo = 0
        self.dir = [(0, 1), (1, 0), (-1, 0), (0, -1)]
        self.simulation = []


    def Heristic(self,x_ht,y_ht,x_goal,y_goal):
        return abs(x_ht - x_goal) + abs(y_ht - y_goal)

    dir = [(0,1),(1,0),(-1,0),(0,-1)]

    def La_Dich(self,Trang_Thai_HT,Trang_Thai_Dich):
        value, toa_do, solanre,_ = Trang_Thai_HT
        value1,toado_1,solanre_1,_ = Trang_Thai_Dich

        if value == value1 and toa_do==toado_1:
            if solanre < 3 :
                return True
            else:
                return False
        else:
            return False




    def Sinh_Trang_Thai_Ke_Tiep_hill_clambing(self,Trang_Thai_HT, hang_doi, visited, TT_Dich, parent):
        global lan_vo
        _, (x, y), solanre, huong_truoc = Trang_Thai_HT
        value, (x_goal,y_goal), _, _ = TT_Dich
        hx_ht = self.Heristic(x,y,x_goal,y_goal)
        for idx,(dx,dy) in enumerate(self.dir):
            x_new,y_new= dx+x,y+dy
            if 0<=x_new<12 and 0<=y_new<12:
                if (self.ma_tran[x_new][y_new] == 0 or (
                        self.ma_tran[x_new][y_new] == value and x_new == x_goal and y_new == y_goal)) and (
                        huong_truoc == -1 or (
                self.dir[idx][0] + self.dir[huong_truoc][0], self.dir[idx][1] + self.dir[huong_truoc][1]) != (0, 0)):
                    new_turns = solanre+(0 if huong_truoc == -1 or huong_truoc == idx else 1)
                    if new_turns <= 2 :
                        hx =  self.Heristic(x_new,y_new,x_goal,y_goal)
                        if hx <= hx_ht:
                            Trang_Thai_Moi = (self.ma_tran[x_new][y_new],(x_new,y_new),new_turns,idx)
                            if Trang_Thai_Moi not in visited:
                                heapq.heappush(hang_doi,(hx,lan_vo,Trang_Thai_Moi))
                                lan_vo += 1
                                visited.add(Trang_Thai_Moi)
                                parent[Trang_Thai_Moi] =Trang_Thai_HT


    lan_vo = 0
    def hill_clambing(self,Trang_Thai_Ban_Dau,TT_Dich):
        global  lan_vo
        hang_doi  = []
        heapq.heappush(hang_doi,(self.Heristic(Trang_Thai_Ban_Dau[1][0],Trang_Thai_Ban_Dau[1][1],TT_Dich[1][0],TT_Dich[1][1]),self.lan_vo,Trang_Thai_Ban_Dau))
        self.lan_vo +=1
        visited = set()
        visited.add(Trang_Thai_Ban_Dau)
        parent = {}
        while hang_doi:
            cost_bd,lan_vo,Trang_Thai_Hien_Tai = heapq.heappop(hang_doi)
            if self.La_Dich(Trang_Thai_Hien_Tai,TT_Dich):
                cur = Trang_Thai_Hien_Tai
                path = []
                gia_tri_cost = []
                while cur in parent:
                    path.append(cur[1])
                    gia_tri_cost.append(self.Heristic(cur[1][0], cur[1][1], TT_Dich[1][0], TT_Dich[1][1]))
                    cur = parent[cur]
                path.append(Trang_Thai_Ban_Dau[1])
                gia_tri_cost.append(self.Heristic(Trang_Thai_Ban_Dau[1][0],Trang_Thai_Ban_Dau[1][1],TT_Dich[1][0],TT_Dich[1][1]))
                gia_tri_cost.reverse()
                path.reverse()
                return (path,gia_tri_cost)
            hang_doi = []
            self.Sinh_Trang_Thai_Ke_Tiep_hill_clambing(Trang_Thai_Hien_Tai,hang_doi,visited,TT_Dich,parent)
        return [],[]
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









