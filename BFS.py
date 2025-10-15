from collections import deque
import numpy as np
import random
import pygame



class BFS():
    def __init__(self,ma_tran):
        self.ma_tran = ma_tran
        self.dir = [(0, 1), (1, 0), (-1, 0), (0, -1)]
        self.simulation = []

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

    def Sinh_Trang_Thai_Ke_Tiep_BFS(self,Trang_Thai_HT, hang_doi, visited, TT_Dich, parent):
        _, (x, y), solanre, huong_truoc = Trang_Thai_HT
        value, (x_goal,y_goal), _,_ = TT_Dich
        for idx, (dx, dy) in enumerate(self.dir):
            x_new, y_new = x + dx, y + dy
            if 0 <= x_new < 12 and 0 <= y_new < 12:
                if (self.ma_tran[x_new][y_new] == 0 or (
                        self.ma_tran[x_new][y_new] == value and x_new == x_goal and y_new == y_goal)) and (huong_truoc == -1 or (self.dir[idx][0] + self.dir[huong_truoc][0], self.dir[idx][1] + self.dir[huong_truoc][1]) != (0, 0)):
                    new_turns = solanre + (0 if huong_truoc == idx or huong_truoc == -1 else 1)
                    if new_turns <= 2:
                        Trang_Thai_Moi = (self.ma_tran[x_new][y_new], (x_new, y_new), new_turns, idx)
                        if Trang_Thai_Moi not in visited:
                            hang_doi.append(Trang_Thai_Moi)
                            visited.add(Trang_Thai_Moi)
                            parent[Trang_Thai_Moi] = Trang_Thai_HT
                            self.simulation.append(((x, y), (x_new, y_new)))

    def BFS(self,Trang_Thai_Ban_Dau,TT_Dich):
        hang_doi = deque()
        hang_doi.append(Trang_Thai_Ban_Dau)
        visited = set()
        visited.add(Trang_Thai_Ban_Dau)
        parent = {}

        while hang_doi:
            Trang_Thai_HT  = hang_doi.popleft()
            if self.La_Dich(Trang_Thai_HT,TT_Dich):
                path = []
                cur = Trang_Thai_HT
                while cur in parent:
                    path.append(cur[1])
                    cur = parent[cur]
                path.append(Trang_Thai_Ban_Dau[1])
                path.reverse()
                return path
            self.Sinh_Trang_Thai_Ke_Tiep_BFS(Trang_Thai_HT,hang_doi,visited,TT_Dich,parent)


    def Ve_Simulation(self, panel, color=(0, 255, 0)):
            font = pygame.font.SysFont("Arial", 13, bold=True)
            line_number = 1
            for (start, end) in self.simulation:
                x1, y1 = start
                x2, y2 = end
                start_px = (y1 * 48 + 24, x1 * 48 + 24)
                end_px = (y2 * 48 + 24, x2 * 48 + 24)
                pygame.draw.line(panel, color, start_px, end_px, 4)


                mid_x = (start_px[0] + end_px[0]) // 2
                mid_y = (start_px[1] + end_px[1]) // 2


                text_surface = font.render(str(line_number), True, (0,0,0))  # màu trắng
                text_rect = text_surface.get_rect(center=(mid_x, mid_y))

                panel.blit(text_surface, text_rect)


                pygame.display.update()


                line_number += 1  # tăng số line


