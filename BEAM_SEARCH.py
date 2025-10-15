import heapq
from collections import deque
import numpy as np
import random
import pygame



class BEAM_SEARCH():
    def __init__(self,ma_tran):
        self.ma_tran = ma_tran
        self.dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        self.simulation = []
    def Heristic(self,x_ht,y_ht,x_goal,y_goal):
        return abs(x_ht - x_goal) + abs(y_ht - y_goal)


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

    def Sinh_Trang_Thai_Ke_Tiep_Beam(self,value, x, y, huong, re, x_goal, y_goal, visited):

        trang_thai_moi = []

        for idx, (dx, dy) in enumerate(self.dirs):
            x_new, y_new = x + dx, y + dy
            if 0 <= x_new < len(self.ma_tran) and 0 <= y_new < len(self.ma_tran[0]):
                if (self.ma_tran[x_new][y_new] == 0 or (
                        self.ma_tran[x_new][y_new] == value and x_new == x_goal and y_new == y_goal)) and (
                        huong == -1 or (
                self.dirs[idx][0] + self.dirs[huong][0], self.dirs[idx][1] + self.dirs[huong][1]) != (0, 0)):
                    new_re = re + (0 if huong == idx or huong == -1 else 1)
                    if new_re <= 2:
                        if (x_new, y_new, idx, new_re) not in visited:
                            visited.add((x_new, y_new, idx, new_re))
                            self.simulation.append(((x, y), (x_new, y_new)))
                            h = self.Heristic(x_new, y_new, x_goal, y_goal)
                            f_new = h
                            trang_thai_moi.append((f_new, (x_new, y_new), idx, new_re))
        return trang_thai_moi

    def beam_search(self,TT_BD, TT_Dich, beam_width=3):
        value, (x_start, y_start), turn, huong_truoc = TT_BD
        _, (x_goal, y_goal), _, _ = TT_Dich

        ds = []
        heapq.heappush(ds, (0, [(x_start, y_start)], -1, 0))

        visited = set()
        visited.add((x_start, y_start, -1, 0))

        while ds:
            ds_hien_tai = []
            for _ in range(min(beam_width, len(ds))):
                f, path, huong, re = heapq.heappop(ds)
                ds_hien_tai.append((f, path, huong, re))

            ds_tt_moi = []
            for f, path, huong, re in ds_hien_tai:
                (x, y) = path[-1]

                if (x, y) == (x_goal, y_goal) and re <= 2:
                    return path, f

                cac_trang_thai_moi = self.Sinh_Trang_Thai_Ke_Tiep_Beam(
                    value, x, y, huong, re, x_goal, y_goal, visited
                )

                for f_new, (x_new, y_new), idx, new_re in cac_trang_thai_moi:
                    new_path = path + [(x_new, y_new)]
                    ds_tt_moi.append((f_new, new_path, idx, new_re))

            ds = heapq.nsmallest(beam_width, ds_tt_moi, key=lambda x: x[0])
            heapq.heapify(ds)

        return None, None

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


