import asyncio
import sys
from tkinter import font

import numpy as np
import random
import  pygame

pygame.init()
panel = pygame.Surface((580,580))
man_hinh = pygame.display.set_mode((800,800))
pygame.display.set_caption("Pikachu")
font = pygame.font.SysFont("Arial",20)
level =1
def Cost(i,j,value):
    if ma_tran[i][j] == value or  ma_tran[i][j] == 0 :
        return 1
import math
def Heristic(x_ht,y_ht,x_goal,y_goal):
    return abs(x_ht - x_goal) + abs(y_ht - y_goal)

def Heristic_1(x_ht,y_ht,x_goal,y_goal):
    return math.sqrt((x_ht - x_goal)**2 + (y_ht - y_goal)**2)
def Tao_board_game():
    ma_tran_ma_hoa = []
    cac_icon = np.arange(1,11)
    for i in cac_icon:
                mang_luu_icon_tam_thoi = [i] * 10
                ma_tran_ma_hoa.extend(mang_luu_icon_tam_thoi)


    ma_tran_ma_hoa = np.array(ma_tran_ma_hoa)

    random.shuffle(ma_tran_ma_hoa)
    ma_tran_ma_hoa = ma_tran_ma_hoa.reshape(10,10)

    rows, cols = ma_tran_ma_hoa.shape
    board_with_border = np.zeros((rows + 2, cols + 2), dtype=int)
    board_with_border[1:rows + 1, 1:cols + 1] = ma_tran_ma_hoa

    return board_with_border


ma_tran = Tao_board_game()
print(ma_tran)

img = pygame.image.load("ech_ki_dieu.png")
img_1 = pygame.image.load("avatar (1).png")
img_2 = pygame.image.load("caterpie (1).png")
img_3 = pygame.image.load("mankey (1).png")
img_4 = pygame.image.load("mew (1).png")
img_5 = pygame.image.load("pikachu (1).png")
img_6 = pygame.image.load("pokemon_.png")
img_7 = pygame.image.load("pokemon_1 (1).png")
img_8 = pygame.image.load("squirtle (1).png")
img_9 = pygame.image.load("venonat (1).png")
img_bg = pygame.image.load("bg.png")

def Gan_icon(ma_tran,panel):
    panel.fill("Pink")
    for i in range(12):
        for j in range(12):
            rect = pygame.Rect(j * 48, i * 48, 48, 48)
            mouse_pos = pygame.mouse.get_pos()
            if rect.collidepoint(mouse_pos[0]-100, mouse_pos[1]-170):
                pygame.draw.rect(panel, (178, 34, 34), rect, 3)
            else:
                pygame.draw.rect(panel, (32, 178, 170), rect, 1)
            if ma_tran[i][j] == 0 :
                pygame.draw.rect(panel,"Pink" , rect)
            if ma_tran[i][j] == 1:
                img_rect = img.get_rect(center=rect.center)
                panel.blit(img, img_rect)
            if ma_tran[i][j] == 2:
                img_rect = img_1.get_rect(center=rect.center)
                panel.blit(img_1, img_rect)
            if ma_tran[i][j] == 3:
                img_rect = img_2.get_rect(center=rect.center)
                panel.blit(img_2, img_rect)
            if ma_tran[i][j] == 4:
                img_rect = img_3.get_rect(center=rect.center)
                panel.blit(img_3, img_rect)
            if ma_tran[i][j] == 5:
                img_rect = img_4.get_rect(center=rect.center)
                panel.blit(img_4, img_rect)
            if ma_tran[i][j] == 6:
                img_rect = img_5.get_rect(center=rect.center)
                panel.blit(img_5, img_rect)
            if ma_tran[i][j] == 7:
                img_rect = img_6.get_rect(center=rect.center)
                panel.blit(img_6, img_rect)
            if ma_tran[i][j] == 8:
                img_rect = img_7.get_rect(center=rect.center)
                panel.blit(img_7, img_rect)
            if ma_tran[i][j] == 9:
                img_rect = img_8.get_rect(center=rect.center)
                panel.blit(img_8, img_rect)
            if ma_tran[i][j] == 10:
                img_rect = img_9.get_rect(center=rect.center)
                panel.blit(img_9, img_rect)


from collections import deque
import heapq

dir = [(0,1),(1,0),(-1,0),(0,-1)]

def La_Dich(Trang_Thai_HT,Trang_Thai_Dich):
    value, toa_do, solanre,_ = Trang_Thai_HT
    value1,toado_1,solanre_1,_ = Trang_Thai_Dich

    if value == value1 and toa_do==toado_1:
        if solanre < 3 :
            return True
        else:
            return False
    else:
        return False


def Sinh_Trang_Thai_Ke_Tiep_BFS(Trang_Thai_HT, hang_doi, visited, TT_Dich, parent):
    _, (x, y), solanre, huong_truoc = Trang_Thai_HT
    value, (x_goal,y_goal), _,_ = TT_Dich
    for idx, (dx, dy) in enumerate(dir):
        x_new, y_new = x + dx, y + dy
        if 0 <= x_new < 12 and 0 <= y_new < 12:
            if ma_tran[x_new][y_new] == 0 or (ma_tran[x_new][y_new] == value and x_new == x_goal and y_new == y_goal) :
                new_turns = solanre + (0 if huong_truoc == idx or huong_truoc == -1 else 1)
                if new_turns <= 2:
                    Trang_Thai_Moi = (ma_tran[x_new][y_new], (x_new, y_new), new_turns, idx)
                    if Trang_Thai_Moi not in visited:
                        hang_doi.append(Trang_Thai_Moi)
                        visited.add(Trang_Thai_Moi)
                        parent[Trang_Thai_Moi] = Trang_Thai_HT


def Sinh_Trang_Thai_Ke_Tiep_A_sao(Trang_Thai_HT, hang_doi, visited, TT_Dich, parent,cost_bd):
    global lan_vo
    _, (x, y), solanre, huong_truoc = Trang_Thai_HT
    value, Toa_Do_Goal, _, _ = TT_Dich
    for idx, (dx, dy) in enumerate(dir):
        x_new, y_new = x + dx, y + dy
        if 0 <= x_new < 12 and 0 <= y_new < 12:
            if ma_tran[x_new][y_new] == 0 or (ma_tran[x_new][y_new] == value and x_new == Toa_Do_Goal[0] and y_new == Toa_Do_Goal[1]):
                new_turns = solanre + (0 if huong_truoc == idx or huong_truoc == -1 else 1)
                if new_turns <= 2:
                    cost_all = Cost(x_new,y_new,value) + Heristic(x_new,y_new,Toa_Do_Goal[0],Toa_Do_Goal[1]) + cost_bd
                    Trang_Thai_Moi = (ma_tran[x_new][y_new], (x_new, y_new), new_turns, idx)
                    if Trang_Thai_Moi not in visited:
                        heapq.heappush(hang_doi,(cost_all,lan_vo,Trang_Thai_Moi))
                        lan_vo +=1
                        visited.add(Trang_Thai_Moi)
                        parent[Trang_Thai_Moi] = Trang_Thai_HT


def Sinh_Trang_Thai_Ke_Tiep_hill_clambing(Trang_Thai_HT, hang_doi, visited, TT_Dich, parent):
    global lan_vo
    _, (x, y), solanre, huong_truoc = Trang_Thai_HT
    value, (x_d,y_d), _, _ = TT_Dich
    hx_ht = Heristic_1(x,y,x_d,y_d)
    for idx,(dx,dy) in enumerate(dir):
        x_new,y_new= dx+x,y+dy
        if 0<=x_new<12 and 0<=y_new<12:
            if ma_tran[x_new][y_new] ==0 or (ma_tran[x_new][y_new] == value and x_new == x_d and y_new ==y_d):
                new_turns = solanre+(0 if huong_truoc == -1 or huong_truoc == idx else 1)
                if new_turns <= 2 :
                    hx =  Heristic_1(x_new,y_new,x_d,y_d)
                    if hx <= hx_ht:
                        Trang_Thai_Moi = (ma_tran[x_new][y_new],(x_new,y_new),new_turns,idx)
                        if Trang_Thai_Moi not in visited:
                            heapq.heappush(hang_doi,(hx,lan_vo,Trang_Thai_Moi))
                            lan_vo += 1
                            visited.add(Trang_Thai_Moi)
                            parent[Trang_Thai_Moi] =Trang_Thai_HT

def BFS(Trang_Thai_Ban_Dau,TT_Dich):
    hang_doi = deque()
    hang_doi.append(Trang_Thai_Ban_Dau)
    visited = set()
    visited.add(Trang_Thai_Ban_Dau)
    parent = {}
    while hang_doi:
        Trang_Thai_HT  = hang_doi.popleft()
        if La_Dich(Trang_Thai_HT,TT_Dich):
            path = []
            cur = Trang_Thai_HT
            while cur in parent:
                path.append(cur[1])
                cur = parent[cur]
            path.append(Trang_Thai_Ban_Dau[1])
            path.reverse()
            return path
        Sinh_Trang_Thai_Ke_Tiep_BFS(Trang_Thai_HT,hang_doi,visited,TT_Dich,parent)


lan_vo = 0
def Asao(Trang_Thai_Ban_Dau,TT_Dich):
    global  lan_vo
    hang_doi  = []
    heapq.heappush(hang_doi,(Heristic(Trang_Thai_Ban_Dau[1][0],Trang_Thai_Ban_Dau[1][1],TT_Dich[1][0],TT_Dich[1][1]),lan_vo,Trang_Thai_Ban_Dau))
    lan_vo +=1
    visited = set()
    visited.add(Trang_Thai_Ban_Dau)
    parent = {}
    while hang_doi:
        cost_bd,lan_vo,Trang_Thai_Hien_Tai = heapq.heappop(hang_doi)
        if La_Dich(Trang_Thai_Hien_Tai,TT_Dich):
            cur = Trang_Thai_Hien_Tai
            path = []
            gia_tri_cost = []
            while cur in parent:
                path.append(cur[1])
                gia_tri_cost.append(Heristic(cur[1][0], cur[1][1], TT_Dich[1][0], TT_Dich[1][1]))
                cur = parent[cur]
            path.append(Trang_Thai_Ban_Dau[1])
            gia_tri_cost.append(Heristic(Trang_Thai_Ban_Dau[1][0],Trang_Thai_Ban_Dau[1][1],TT_Dich[1][0],TT_Dich[1][1]))
            gia_tri_cost.reverse()
            path.reverse()
            return (path,gia_tri_cost)
        cost_bd -= Heristic(Trang_Thai_Hien_Tai[1][0],Trang_Thai_Hien_Tai[1][1],TT_Dich[1][0],TT_Dich[1][1])
        Sinh_Trang_Thai_Ke_Tiep_A_sao(Trang_Thai_Hien_Tai,hang_doi,visited,TT_Dich,parent,cost_bd)
    return [],[]

def hill_clambing(Trang_Thai_Ban_Dau,TT_Dich):
    global  lan_vo
    hang_doi  = []
    heapq.heappush(hang_doi,(Heristic_1(Trang_Thai_Ban_Dau[1][0],Trang_Thai_Ban_Dau[1][1],TT_Dich[1][0],TT_Dich[1][1]),lan_vo,Trang_Thai_Ban_Dau))
    lan_vo +=1
    visited = set()
    visited.add(Trang_Thai_Ban_Dau)
    parent = {}

    while hang_doi:
        cost_bd,lan_vo,Trang_Thai_Hien_Tai = heapq.heappop(hang_doi)
        if La_Dich(Trang_Thai_Hien_Tai,TT_Dich):
            cur = Trang_Thai_Hien_Tai
            path = []
            gia_tri_cost = []
            while cur in parent:
                path.append(cur[1])
                gia_tri_cost.append(Heristic(cur[1][0], cur[1][1], TT_Dich[1][0], TT_Dich[1][1]))
                cur = parent[cur]
            path.append(Trang_Thai_Ban_Dau[1])
            gia_tri_cost.append(Heristic_1(Trang_Thai_Ban_Dau[1][0],Trang_Thai_Ban_Dau[1][1],TT_Dich[1][0],TT_Dich[1][1]))
            gia_tri_cost.reverse()
            path.reverse()
            return (path,gia_tri_cost)
        hang_doi = []
        Sinh_Trang_Thai_Ke_Tiep_hill_clambing(Trang_Thai_Hien_Tai,hang_doi,visited,TT_Dich,parent)
    return [],[]
def Ve_Duong_Di_Asao(path, gia_tri_cost, panel):
    for i in range(len(path) - 1):
        x1, y1 = path[i]
        x2, y2 = path[i+1]

        start = (y1 * 48 + 24, x1 * 48 + 24)
        end   = (y2 * 48 + 24, x2 * 48 + 24)
        pygame.draw.line(panel, (255, 0, 0), start, end, 3)
        mid_x = (start[0] + end[0]) // 2
        mid_y = (start[1] + end[1]) // 2
        text = font.render(str(gia_tri_cost[i]), True, (0, 0, 255))
        panel.blit(text, (mid_x , mid_y ))


def ham_reset():
    global ma_tran
    core = ma_tran[1:11, 1:11].flatten()
    random.shuffle(core)
    ma_tran[1:11, 1:11] = np.array(core).reshape(10, 10)


def ve_nut(text, x, y, width, height, color, hover_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()


    if x < mouse[0] < x + width and y < mouse[1] < y + height:
        pygame.draw.rect(man_hinh, hover_color, (x, y, width, height))
        if click[0] == 1 and action is not None:
            action()  # Gọi hành động khi nhấn
    else:
        pygame.draw.rect(man_hinh, color, (x, y, width, height))

    # Thêm chữ vào nút
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    man_hinh.blit(text_surface, text_rect)




def Ve_Duong_Di(path, panel):
    for i in range(len(path) - 1):
        x1, y1 = path[i]
        x2, y2 = path[i+1]
        start = (y1 * 48 + 24, x1 * 48 + 24)
        end   = (y2 * 48 + 24, x2 * 48 + 24)
        pygame.draw.line(panel, (255, 0, 0), start, end, 3)



def Tu_Dong():
    for i in range(1, 11):
        for j in range(1, 11):
            if ma_tran[i][j] != 0:  # chỉ xét ô có hình
                solanre = 0
                TT_BD = (ma_tran[i][j],(i,j),solanre,-1)
                for x in range(1,11 ):
                    for y in range(1,11):
                        if (x!=i or y!=j) and ma_tran[i][j] == ma_tran[x][y]:
                            TT_GOAL = (ma_tran[x][y],(x,y),None,None)
                            (path,cost) = Asao(TT_BD,TT_GOAL)
                            if path and cost:
                                print("Tìm được cặp:", path)
                                (x1, y1) = path[0]
                                (x2, y2) = path[-1]
                                ma_tran[x1][y1] = 0
                                ma_tran[x2][y2] = 0
                                Ve_Duong_Di_Asao(path,cost,panel)
                                man_hinh.blit(img_bg,(0,0))
                                man_hinh.blit(panel,(100,170))
                                Gan_icon(ma_tran, panel)
                                pygame.display.update()
                                pygame.time.delay(600)

                                return True
    return False


dir = [(1,0),(0,1),(-1,0),(0,-1)]

def init_Tap_Gia_Tri(x,y):
    Tap_Gia_Tri = []
    for k in dir:
        x_new, y_new = k[0]+x, k[1]+y
        Tap_Gia_Tri.append((x_new,y_new))
    return Tap_Gia_Tri

def init_Tap_Rang_Buoc(turn ,x,y,value,huong_trc,huong_ht,visited,X_goal):
    if x < 12 and x >= 0 and y < 12 and y >= 0:
        if (ma_tran[x][y] == 0 or (ma_tran[x][y] == value and X_goal[0]==x and X_goal[1]==y)) and ((x,y) not in visited):
            turn += (0 if huong_trc == huong_ht else 1)
            if turn <=2:
                return True
    return False

def Backtracking(X_cur,X_goal,path,turn,visited,huong_ht):
  if X_cur == X_goal:
      return path.copy()
  Tap_Gia_Tri = init_Tap_Gia_Tri(X_cur[0],X_cur[1])
  for (dx,dy) in Tap_Gia_Tri:
      if huong_ht ==-1 :
          new_dir = ((dx - X_cur[0]), (dy - X_cur[1]))
          huong_ht = new_dir
          huong_trc = new_dir
      else:
          huong_trc = huong_ht
          huong_ht =  ((dx-X_cur[0]), (dy-X_cur[1]))
      if  init_Tap_Rang_Buoc(turn,dx,dy,ma_tran[X_goal[0]][X_goal[1]],huong_trc,huong_ht,visited,X_goal):
          new_turn = turn
          if (huong_trc != huong_ht):
              new_turn += 1
          visited.add((dx, dy))
          path.append((dx, dy))
          result = Backtracking((dx,dy),X_goal,path,new_turn,visited,huong_ht)
          if result is not None:
              return result
          path.pop()
          visited.remove((dx,dy))
  return None



def Tu_Dong_1():
        for i in range(1, 11):
            for j in range(1, 11):
                if ma_tran[i][j] != 0:
                    X1 =  (i, j)
                    for x in range(1, 11):
                         for y in range(1, 11):
                            if (x != i or y != j) and ma_tran[i][j] == ma_tran[x][y]:
                                    Xn = (x,y)
                                    visited = set([(i,j)])
                                    path = Backtracking(X1,Xn,[(i,j)],0,visited,-1)
                                    if path is not None:
                                        print("Tìm được cặp:", path)
                                        (x1, y1) = path[0]
                                        (x2, y2) = path[-1]
                                        ma_tran[x1][y1] = 0
                                        ma_tran[x2][y2] = 0
                                        Ve_Duong_Di(path, panel)
                                        man_hinh.blit(img_bg, (0, 0))
                                        man_hinh.blit(panel, (100, 170))
                                        Gan_icon(ma_tran, panel)
                                        pygame.display.update()
                                        pygame.time.delay(200)
                                        huong_sap = Lay_Huong_Sap(level)
                                        if huong_sap is not None:
                                            Sap_Hinh(huong_sap)
                                            man_hinh.blit(img_bg, (0, 0))
                                            man_hinh.blit(panel, (100, 170))
                                            Gan_icon(ma_tran, panel)
                                            pygame.display.update()
                                            pygame.time.delay(10)
                                        return True
        return False


def Kiem_Tra_Het():
    global level
    for i in range(1, 11):
        for j in range(1, 11):
            if ma_tran[i][j] != 0:
                return False
    level+=1
    return True

def Sap_Hinh(huong="down"):
    global ma_tran
    core = ma_tran[1:11, 1:11].copy()   # copy để thao tác an toàn

    if huong == "down":
        for j in range(10):
            col = [core[i][j] for i in range(10)]
            new_col = [x for x in col if x != 0]
            new_col = [0] * (10 - len(new_col)) + new_col
            for i in range(10):
                core[i][j] = new_col[i]

    elif huong == "up":
        for j in range(10):
            col = [core[i][j] for i in range(10)]
            new_col = [x for x in col if x != 0]
            new_col = new_col + [0] * (10 - len(new_col))
            for i in range(10):
                core[i][j] = new_col[i]

    elif huong == "left":
        for i in range(10):
            row = [core[i][j] for j in range(10)]
            new_row = [x for x in row if x != 0]
            new_row = new_row + [0] * (10 - len(new_row))
            for j in range(10):
                core[i][j] = new_row[j]


    elif huong == "right":
        for i in range(10):
            row = [core[i][j] for j in range(10)]
            new_row = [x for x in row if x != 0]
            new_row = [0] * (10 - len(new_row)) + new_row
            for j in range(10):
                core[i][j] = new_row[j]


    elif huong == "center":
        for i in range(10):
            row = [x for x in core[i] if x != 0]
            zeros = 10 - len(row)
            left = zeros // 2
            right = zeros - left
            core[i] = [0]*left + row + [0]*right

    # ghi ngược lại vào ma_tran có viền
    ma_tran[1:11, 1:11] = core

def Lay_Huong_Sap(level):
    if level == 1:
        return None
    elif level == 2:
        return "down"
    elif level == 3:
        return "up"
    elif level == 4:
        return "left"
    elif level == 5:
        return "right"
    else:
        return "center"



while True:
        man_hinh.blit(img_bg, (0, 0))
        man_hinh.blit(panel, (100, 170))
        Gan_icon(ma_tran, panel)

        if not Tu_Dong_1():
            if Kiem_Tra_Het():
                ma_tran = Tao_board_game()
            else:
                ham_reset()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        pygame.time.delay(200)

