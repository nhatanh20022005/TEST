import heapq
import math

import pygame


class A_SAO():

    def __init__(self,ma_tran):
        self.ma_tran = ma_tran
        self.lan_vo = 0
        self.dir = [(0, 1), (1, 0), (-1, 0), (0, -1)]
        self.simulation = []
    def Cost(self,i,j,value):
        if self.ma_tran[i][j] == value or  self.ma_tran[i][j] == 0 :
            return 1
    def Heristic(self,x_ht,y_ht,x_goal,y_goal):
        return abs(x_ht - x_goal) + abs(y_ht - y_goal)

    def Heristic_1(self,x_ht,y_ht,x_goal,y_goal):
        return math.sqrt((x_ht - x_goal)**2 + (y_ht - y_goal)**2)


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



    def Sinh_Trang_Thai_Ke_Tiep_A_sao(self,Trang_Thai_HT, hang_doi, visited, TT_Dich, parent,cost_bd):
        global lan_vo
        _, (x, y), solanre, huong_truoc = Trang_Thai_HT
        value, Toa_Do_Goal, _, _ = TT_Dich
        for idx, (dx, dy) in enumerate(self.dir):
            x_new, y_new = x + dx, y + dy
            if 0 <= x_new < 12 and 0 <= y_new < 12:
                if self.ma_tran[x_new][y_new] == 0 or (self.ma_tran[x_new][y_new] == value and x_new == Toa_Do_Goal[0] and y_new == Toa_Do_Goal[1]) and (x_new+x,y_new+y) != (0,0):
                    new_turns = solanre + (0 if huong_truoc == idx or huong_truoc == -1 else 1)
                    if new_turns <= 2:
                        cost_all = self.Cost(x_new,y_new,value) + self.Heristic(x_new,y_new,Toa_Do_Goal[0],Toa_Do_Goal[1]) + cost_bd
                        if self.Heristic(x_new,y_new,Toa_Do_Goal[0],Toa_Do_Goal[1]) ==0:
                            cost_all=0
                        Trang_Thai_Moi = (self.ma_tran[x_new][y_new], (x_new, y_new), new_turns, idx)
                        if Trang_Thai_Moi not in visited:
                            heapq.heappush(hang_doi,(cost_all,lan_vo,Trang_Thai_Moi))
                            self.lan_vo +=1
                            visited[Trang_Thai_Moi] = cost_all
                            parent[Trang_Thai_Moi] = (Trang_Thai_HT,cost_bd+self.Heristic(x,y,Toa_Do_Goal[0],Toa_Do_Goal[1]))
                            self.simulation.append(((x,y),(x_new,y_new)))
                        elif Trang_Thai_Moi in visited and visited[Trang_Thai_Moi] > cost_all :
                            heapq.heappush(hang_doi,(cost_all,lan_vo,Trang_Thai_Moi))
                            self.lan_vo +=1
                            visited[Trang_Thai_Moi] = cost_all
                            parent[Trang_Thai_Moi] = (Trang_Thai_HT,cost_bd+self.Heristic(x,y,Toa_Do_Goal[0],Toa_Do_Goal[1]))
                            self.simulation.append(((x,y),(x_new,y_new)))


    def Asao(self,Trang_Thai_Ban_Dau,TT_Dich):
        global  lan_vo
        hang_doi  = []
        heapq.heappush(hang_doi,(self.Heristic(Trang_Thai_Ban_Dau[1][0],Trang_Thai_Ban_Dau[1][1],TT_Dich[1][0],TT_Dich[1][1]),self.lan_vo,Trang_Thai_Ban_Dau))
        self.lan_vo +=1
        visited = {Trang_Thai_Ban_Dau:self.Heristic(Trang_Thai_Ban_Dau[1][0],Trang_Thai_Ban_Dau[1][1],TT_Dich[1][0],TT_Dich[1][1])}
        parent = {}
        while hang_doi:
            cost_bd,lan_vo,Trang_Thai_Hien_Tai = heapq.heappop(hang_doi)
            if self.La_Dich(Trang_Thai_Hien_Tai, TT_Dich):
                path = []
                cost_values = []
                cur = Trang_Thai_Hien_Tai
                g = cost_bd
                while cur in parent:
                    path.append(cur[1])
                    cost_values.append(g)
                    cur, g = parent[cur]
                path.append(Trang_Thai_Ban_Dau[1])
                cost_values.append(self.Heristic(Trang_Thai_Ban_Dau[1][0],Trang_Thai_Ban_Dau[1][1],TT_Dich[1][0],TT_Dich[1][1]))
                path.reverse()
                cost_values.reverse()
                return path, cost_values

            cost_bd -= self.Heristic(Trang_Thai_Hien_Tai[1][0],Trang_Thai_Hien_Tai[1][1],TT_Dich[1][0],TT_Dich[1][1])
            self.Sinh_Trang_Thai_Ke_Tiep_A_sao(Trang_Thai_Hien_Tai,hang_doi,visited,TT_Dich,parent,cost_bd)
        return [],[]
    def Ve_Simulation(self, panel, color=(0, 255, 0)):
            font = pygame.font.SysFont("Arial", 13, bold=True)
            for (start, end) in self.simulation:
                x1, y1 = start
                x2, y2 = end
                start_px = (y1 * 48 + 24, x1 * 48 + 24)
                end_px = (y2 * 48 + 24, x2 * 48 + 24)
                pygame.draw.line(panel, color, start_px, end_px, 4)
                pygame.display.update()



