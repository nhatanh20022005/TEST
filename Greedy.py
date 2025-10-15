import heapq
import math

import pygame


class Greedy():

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

    def Sinh_Trang_Thai_Ke_Tiep_Greedy(self,Trang_Thai_HT, hang_doi, visited, TT_Dich, parent):
        global lan_vo
        _, (x, y), solanre, huong_truoc = Trang_Thai_HT
        value, (x_goal, y_goal), _, _ = TT_Dich
        for idx, (dx, dy) in enumerate(self.dir):
            x_new, y_new = dx + x, y + dy
            if 0 <= x_new < 12 and 0 <= y_new < 12:
                if (self.ma_tran[x_new][y_new] == 0 or (
                        self.ma_tran[x_new][y_new] == value and x_new == x_goal and y_new == y_goal)) and (
                        huong_truoc == -1 or (self.dir[idx][0] + self.dir[huong_truoc][0], self.dir[idx][1] + self.dir[huong_truoc][1]) != (0, 0)):
                    new_turns = solanre + (0 if huong_truoc == -1 or huong_truoc == idx else 1)
                    if new_turns <= 2:
                        hx = self.Heristic(x_new, y_new, x_goal, y_goal)
                        Trang_Thai_Moi = (self.ma_tran[x_new][y_new], (x_new, y_new), new_turns, idx)
                        if Trang_Thai_Moi not in visited:
                            heapq.heappush(hang_doi, (hx, lan_vo, Trang_Thai_Moi))
                            lan_vo += 1
                            visited[Trang_Thai_Moi] = hx
                            parent[Trang_Thai_Moi] = Trang_Thai_HT
                            self.simulation.append(((x,y),(x_new,y_new)))
                        elif Trang_Thai_Moi in visited and hx < visited[Trang_Thai_Moi] :
                            heapq.heappush(hang_doi, (hx, lan_vo, Trang_Thai_Moi))
                            lan_vo += 1
                            visited[Trang_Thai_Moi] = hx
                            parent[Trang_Thai_Moi] = Trang_Thai_HT
                            self.simulation.append(((x,y),(x_new,y_new)))


    def Greedy(self,Trang_Thai_Ban_Dau,TT_Dich):
        global  lan_vo
        hang_doi  = []
        heapq.heappush(hang_doi,(self.Heristic(Trang_Thai_Ban_Dau[1][0],Trang_Thai_Ban_Dau[1][1],TT_Dich[1][0],TT_Dich[1][1]),self.lan_vo,Trang_Thai_Ban_Dau))
        self.lan_vo +=1
        visited = set()
        visited = {Trang_Thai_Ban_Dau:self.Heristic(Trang_Thai_Ban_Dau[1][0],Trang_Thai_Ban_Dau[1][1],TT_Dich[1][0],TT_Dich[1][1])}
        parent = {}
        while hang_doi:
            cost_bd,lan_vo,Trang_Thai_Hien_Tai = heapq.heappop(hang_doi)
            if self.La_Dich(Trang_Thai_Hien_Tai, TT_Dich):
                path = []
                cost_values = []
                cur = Trang_Thai_Hien_Tai
                while cur in parent:
                    path.append(cur[1])
                    g = self.Heristic(cur[1][0],cur[1][1],TT_Dich[1][0],TT_Dich[1][1])
                    cost_values.append(g)
                    cur = parent[cur]
                path.append(Trang_Thai_Ban_Dau[1])
                cost_values.append(self.Heristic(Trang_Thai_Ban_Dau[1][0],Trang_Thai_Ban_Dau[1][1],TT_Dich[1][0],TT_Dich[1][1]))
                path.reverse()
                cost_values.reverse()
                return path, cost_values
            self.Sinh_Trang_Thai_Ke_Tiep_Greedy(Trang_Thai_Hien_Tai,hang_doi,visited,TT_Dich,parent)
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



