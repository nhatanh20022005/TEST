import sys, random, pygame
import numpy as np
# Đặt trong đầu file game.py (hoặc file chính)
import csv, os, psutil, time

HISTORY_FILE = "history.csv"
if not os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Thuật toán", "Level", "Thời gian (s)", "Bộ nhớ (MB)"])
def Ghi_Lich_Su(ten_thuat_toan, level, start_time):
    elapsed = round(time.time() - start_time, 3)
    memory = round(psutil.Process().memory_info().rss / 1024 / 1024, 3)  # MB
    with open(HISTORY_FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([ten_thuat_toan, level, elapsed, memory])

# ====== MENU ======
pygame.init()
MENU_W, MENU_H = 977, 600
menu_screen = pygame.display.set_mode((MENU_W, MENU_H))
pygame.display.set_caption("Pikachu Menu")

bg_image = pygame.image.load("bg_menu2.jpg").convert()
bg_x, bg_y = 0, 0
bg_dx, bg_dy = 0.2, 0.1
font = pygame.font.SysFont("Tahoma", 28, bold=True)

algorithms = [
    "BFS", "DFS", "A*", "Greedy", "HillClimb", "BeamSearch",
    "Backtrack", "ForwardChk", "Mu1Phan", "MuTP"
]

play_button   = pygame.Rect(MENU_W//2 - 150, MENU_H - 100, 120, 50)
choose_button = pygame.Rect(MENU_W//2 +   30, MENU_H - 100, 150, 50)
history_button = pygame.Rect(MENU_W//2 - 84, MENU_H - 40, 160, 40)


algorithm_rects = [None] * len(algorithms)
confirm_button = pygame.Rect(MENU_W//2 - 200, MENU_H - 80, 150, 50)
cancel_button  = pygame.Rect(MENU_W//2 +  50, MENU_H - 80, 150, 50)

selected = None
temp_selected = None
choosing_screen = False

def draw_background(surface):
    global bg_x, bg_y, bg_dx, bg_dy
    bg_x += bg_dx
    bg_y += bg_dy
    if bg_x > 5 or bg_x < -6: bg_dx *= -1
    if bg_y > 7 or bg_y < -6: bg_dy *= -1
    surface.blit(bg_image, (int(bg_x), int(bg_y)))

def draw_main_menu():
    draw_background(menu_screen)
    mx, my = pygame.mouse.get_pos()

    play_color = (255,235,100) if play_button.collidepoint(mx,my) else (255,215,0)
    pygame.draw.rect(menu_screen, play_color, play_button, border_radius=12)
    menu_screen.blit(font.render("PLAY", True, (0,0,0)),
                     (play_button.centerx-40, play_button.centery-18))

    opt_color = (150,230,255) if choose_button.collidepoint(mx,my) else (100,200,255)
    pygame.draw.rect(menu_screen, opt_color, choose_button, border_radius=12)
    menu_screen.blit(font.render("OPTIONS", True, (0,0,0)),
                     (choose_button.centerx-70, choose_button.centery-18))
    hist_color = (250,180,180) if history_button.collidepoint(mx,my) else (240,150,150)
    pygame.draw.rect(menu_screen, hist_color, history_button, border_radius=12)
    menu_screen.blit(font.render("HISTORY", True, (0,0,0)),
                 (history_button.centerx-60, history_button.centery-15))

    if selected is not None:
        label = font.render(f"SELECTED: {algorithms[selected]}", True, (0,0,0))
        pygame.draw.rect(menu_screen, (230,230,230),
                         (MENU_W//2-200, MENU_H-160, 400, 50), border_radius=8)
        menu_screen.blit(label, (MENU_W//2 - label.get_width()//2, MENU_H-155))

def draw_choose_screen():
    menu_screen.fill((246,241,233))
    mx, my = pygame.mouse.get_pos()

    title = font.render("OPTIONS", True, (0,0,0))
    menu_screen.blit(title, (MENU_W//2 - title.get_width()//2, 30))

    cols = 3
    gap_x, gap_y = 220, 100
    start_x, start_y = 150, 100
    item_w, item_h = 200, 70

    for i, alg in enumerate(algorithms):
        row, col = divmod(i, cols)
        rect = pygame.Rect(start_x + col*gap_x, start_y + row*gap_y, item_w, item_h)
        algorithm_rects[i] = rect

        if rect.collidepoint(mx,my):
            color = (130,220,255)
        elif temp_selected == i:
            color = (100,200,255)
        else:
            color = (255,217,61)

        pygame.draw.rect(menu_screen, color, rect, border_radius=10)
        txt = font.render(alg, True, (0,0,0))
        menu_screen.blit(txt, (rect.centerx - txt.get_width()//2,
                               rect.centery - txt.get_height()//2))

    conf_color = (0,230,120) if confirm_button.collidepoint(mx,my) else (0,200,100)
    pygame.draw.rect(menu_screen, conf_color, confirm_button, border_radius=12)
    menu_screen.blit(font.render("ACCEPT", True, (255,255,255)),
                     (confirm_button.centerx-60, confirm_button.centery-18))

    canc_color = (230,70,70) if cancel_button.collidepoint(mx,my) else (200,50,50)
    pygame.draw.rect(menu_screen, canc_color, cancel_button, border_radius=12)
    menu_screen.blit(font.render("CANCEL", True, (255,255,255)),
                     (cancel_button.centerx-60, cancel_button.centery-18))


# ====== GAME: gói code Pikachu của bạn vào một hàm ======
def run_pikachu(selected_alg: str):
    # --- chuẩn bị cửa sổ game (dùng cửa sổ mới 800x800) ---
    GAME_W, GAME_H = 800, 800
    man_hinh = pygame.display.set_mode((GAME_W, GAME_H))
    pygame.display.set_caption(f"Pikachu - {selected_alg}")
    font20 = pygame.font.SysFont("Arial", 20)
    panel = pygame.Surface((580, 580))
    start_time = time.time()


    level = 1
## tạo ma trận _ Tự Động, Vẽ đường đi, reset
    def Tao_board_game():
        ma_tran_ma_hoa = []
        cac_icon = np.arange(1,11)
        for i in cac_icon:
            ma_tran_ma_hoa.extend([i]*10)
        ma_tran_ma_hoa = np.array(ma_tran_ma_hoa)
        random.shuffle(ma_tran_ma_hoa)
        ma_tran_ma_hoa = ma_tran_ma_hoa.reshape(10,10)
        rows, cols = ma_tran_ma_hoa.shape
        board_with_border = np.zeros((rows+2, cols+2), dtype=int)
        board_with_border[1:rows+1, 1:cols+1] = ma_tran_ma_hoa
        return board_with_border

    ma_tran = Tao_board_game()

    # ---- load hình (giữ nguyên của bạn) ----
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

    def Gan_icon(ma_tran, panel):
        panel.fill((236, 242, 247))  # nền panel

        mouse_pos = pygame.mouse.get_pos()
        mx, my = mouse_pos[0] - 100, mouse_pos[1] - 170  # panel đặt ở (100,170)

        for i in range(12):
            for j in range(12):
                rect = pygame.Rect(j * 48, i * 48, 48, 48)
                inside = rect.collidepoint(mx, my)

                # nền ô: trống (ghi nhạt) / có icon (checker xanh nhạt)
                if ma_tran[i][j] == 0:
                    pygame.draw.rect(panel, (223, 231, 239), rect)  # ô trống
                else:
                    pygame.draw.rect(
                        panel,
                        ((214, 235, 245) if (i + j) % 2 == 0 else (198, 225, 240)),
                        rect
                    )

                # viền: hover xanh dương dịu, thường xám xanh
                pygame.draw.rect(panel, ((70, 140, 200) if inside else (160, 185, 205)), rect, 2)

                # vẽ icon nếu có
                val = ma_tran[i][j]
                if val == 1:
                    panel.blit(img, img.get_rect(center=rect.center))
                elif val == 2:
                    panel.blit(img_1, img_1.get_rect(center=rect.center))
                elif val == 3:
                    panel.blit(img_2, img_2.get_rect(center=rect.center))
                elif val == 4:
                    panel.blit(img_3, img_3.get_rect(center=rect.center))
                elif val == 5:
                    panel.blit(img_4, img_4.get_rect(center=rect.center))
                elif val == 6:
                    panel.blit(img_5, img_5.get_rect(center=rect.center))
                elif val == 7:
                    panel.blit(img_6, img_6.get_rect(center=rect.center))
                elif val == 8:
                    panel.blit(img_7, img_7.get_rect(center=rect.center))
                elif val == 9:
                    panel.blit(img_8, img_8.get_rect(center=rect.center))
                elif val == 10:
                    panel.blit(img_9, img_9.get_rect(center=rect.center))
        for k in range(13):
            x = k * 48
            pygame.draw.line(panel, (180, 200, 215), (x, 0), (x, 576), 1)
            pygame.draw.line(panel, (180, 200, 215), (0, x), (576, x), 1)

    def Ve_Duong_Di(path, panel):
        for i in range(len(path)-1):
            x1,y1 = path[i]
            x2,y2 = path[i+1]
            start = (y1*48+24, x1*48+24)
            end   = (y2*48+24, x2*48+24)
            pygame.draw.line(panel, (220, 60, 60), start, end, 3)

    def Ve_Duong_Di_1(path, gia_tri_cost, panel):
        m = min(len(gia_tri_cost), len(path) - 1)
        for i in range(m):
            x1, y1 = path[i]
            x2, y2 = path[i + 1]
            start = (y1 * 48 + 24, x1 * 48 + 24)
            end = (y2 * 48 + 24, x2 * 48 + 24)

            pygame.draw.line(panel, (220, 60, 60), start, end, 3)

            mid_x = (start[0] + end[0]) // 2
            mid_y = (start[1] + end[1]) // 2
            text = font.render(str(gia_tri_cost[i]), True, (30, 60, 120))
            panel.blit(text, (mid_x - text.get_width() // 2,
                              mid_y - text.get_height() // 2))


    def ham_reset():
        nonlocal ma_tran
        core = ma_tran[1:11,1:11].flatten()
        random.shuffle(core)
        ma_tran[1:11,1:11] = np.array(core).reshape(10,10)


    from BFS import BFS
    from A_SAO import A_SAO
    from BK import BK
    from HILL_CLAMBING import HILL_CLAMBING
    from Foward_Checking import FW_BK
    from DFS import DFS
    from BEAM_SEARCH import BEAM_SEARCH
    from Greedy import Greedy
    from MU_TOAN_PHAN import MU_TOAN_PHAN
    from MU_1_PHAN import MU_1_PHAN

    def chon_Thuat_Toan(ten: str):
        t = ten.lower()
        if t == "bfs": return BFS(ma_tran)
        if t in ("a*", "asao", "a_sao", "a sao"): return A_SAO(ma_tran)
        if t in ("bk", "back tracking", "back_tracking", "backtrack", "backtracking"): return BK(ma_tran)
        if t in ("hillclimb","hill_clambing","hill clambing"): return HILL_CLAMBING(ma_tran)
        if t in ("fwbk","forwardchk","foward checking back tracking","fowardchecking_backtracking"): return FW_BK(ma_tran)
        if t in ("dfs"): return DFS(ma_tran)
        if t in ("beamsearch"): return BEAM_SEARCH(ma_tran)
        if t in ("greedy"): return Greedy(ma_tran)
        if t in ("mutp"): return MU_TOAN_PHAN(ma_tran)
        if t in ("mu1p"): return MU_1_PHAN(ma_tran)


        return None

    doi_tuong = chon_Thuat_Toan(selected_alg)
    if doi_tuong is None:
        print("Không tìm thấy thuật toán:", selected_alg)
        return

    def Kiem_Tra_Het():
        nonlocal level,running_game
        for i in range(1,11):
            for j in range(1,11):
                if ma_tran[i][j] != 0:
                    return False
        # --- Ghi lịch sử trước khi tăng level ---
        end_time = time.time()
        elapsed_time = end_time - start_time

        process = psutil.Process(os.getpid())
        memory_used = process.memory_info().rss / (1024 * 1024)

        with open(HISTORY_FILE, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                selected_alg,
                level,  # level hiện tại (vừa chơi xong)
                round(elapsed_time, 3),
                round(memory_used, 3),
            ])
        print(f"Đã lưu lịch sử: {selected_alg} - Level {level}")

        # --- Sau đó mới tăng level ---
        level += 1

        # --- Kiểm tra nếu hết level thì dừng game ---
        if level > 6:
            Show_Congrats(man_hinh, img_bg, seconds=2.0)
            pygame.time.delay(1000)
            running_game = False
        return True



    def Sap_Hinh(huong="down"):
        nonlocal ma_tran
        core = ma_tran[1:11,1:11].copy()
        if huong == "down":
            for j in range(10):
                col = [core[i][j] for i in range(10)]
                new_col = [x for x in col if x != 0]
                new_col = [0]*(10-len(new_col)) + new_col
                for i in range(10): core[i][j] = new_col[i]
        elif huong == "up":
            for j in range(10):
                col = [core[i][j] for i in range(10)]
                new_col = [x for x in col if x != 0] + [0]*(10-len([x for x in col if x != 0]))
                for i in range(10): core[i][j] = new_col[i]
        elif huong == "left":
            for i in range(10):
                row = [core[i][j] for j in range(10)]
                new_row = [x for x in row if x != 0] + [0]*(10-len([x for x in row if x != 0]))
                for j in range(10): core[i][j] = new_row[j]
        elif huong == "right":
            for i in range(10):
                row = [core[i][j] for j in range(10)]
                nz = [x for x in row if x != 0]
                new_row = [0]*(10-len(nz)) + nz
                for j in range(10): core[i][j] = new_row[j]
        elif huong == "center":
            for i in range(10):
                row = [x for x in core[i] if x != 0]
                zeros = 10 - len(row)
                left = zeros // 2
                right = zeros - left
                core[i] = [0]*left + row + [0]*right
        ma_tran[1:11,1:11] = core

    def Lay_Huong_Sap(level):
        return None if level == 1 else ["down","up","left","right","center"][(level-2)%5]

    def Tu_Dong(doi_tuong):
        for i in range(1,11):
            for j in range(1,11):
                if ma_tran[i][j] != 0:
                    TT_BD = (ma_tran[i][j], (i,j), 0, -1)
                    for x in range(1,11):
                        for y in range(1,11):
                            if (x!=i or y!=j) and ma_tran[i][j] == ma_tran[x][y]:
                                TT_GOAL = (ma_tran[x][y], (x,y), None, None)
                                path, cost = [], []
                                doi_tuong.simulation = []
                                if isinstance(doi_tuong, BFS):
                                    path = doi_tuong.BFS(TT_BD, TT_GOAL)
                                elif isinstance(doi_tuong, DFS):
                                    path = doi_tuong.DFS(TT_BD, TT_GOAL)
                                elif isinstance(doi_tuong, A_SAO):
                                    path, cost = doi_tuong.Asao(TT_BD, TT_GOAL)
                                elif isinstance(doi_tuong,  HILL_CLAMBING):
                                    path, cost = doi_tuong.hill_clambing(TT_BD, TT_GOAL)
                                elif isinstance(doi_tuong, Greedy):
                                    path, cost = doi_tuong.Greedy(TT_BD, TT_GOAL)
                                elif isinstance(doi_tuong,BEAM_SEARCH):
                                    path,cost = doi_tuong.beam_search(TT_BD, TT_GOAL)
                                if path:
                                    doi_tuong.Ve_Simulation(panel)
                                    (x1,y1) = path[0]
                                    (x2,y2) = path[-1]
                                    ma_tran[x1][y1] = 0
                                    ma_tran[x2][y2] = 0
                                    if cost:
                                        Ve_Duong_Di_1(path, cost, panel)
                                    else:
                                        Ve_Duong_Di(path, panel)
                                    man_hinh.blit(img_bg,(0,0))
                                    man_hinh.blit(panel,(100,170))
                                    Gan_icon(ma_tran, panel)
                                    pygame.display.update()
                                    pygame.time.delay(450)
                                    hs = Lay_Huong_Sap(level)
                                    if hs: Sap_Hinh(hs)
                                    return True
        return False
    def Tu_Dong_1(doi_tuong):
        for i in range(1,11):
            for j in range(1,11):
                if ma_tran[i][j] != 0:
                    X1 = (i,j)
                    for x in range(1,11):
                        for y in range(1,11):
                            if (x!=i or y!=j) and ma_tran[i][j] == ma_tran[x][y]:
                                Xn = (x,y)
                                visited = set([(i,j)])
                                path = None
                                try:
                                    from BK import BK as BKClass
                                    from Foward_Checking import FW_BK as FWClass
                                except:
                                    BKClass = object; FWClass = object
                                if doi_tuong.__class__.__name__ == "BK":
                                    path = doi_tuong.Backtracking(X1, Xn, [X1], 0, visited, -1)
                                else:
                                    path = doi_tuong.FW_Backtracking(X1, Xn, [X1], 0, visited, -1)
                                if path:
                                    doi_tuong.Ve_Simulation(panel)
                                    (x1,y1) = path[0]; (x2,y2) = path[-1]
                                    ma_tran[x1][y1] = 0; ma_tran[x2][y2] = 0
                                    Ve_Duong_Di(path, panel)
                                    man_hinh.blit(img_bg,(0,0)); man_hinh.blit(panel,(100,170))
                                    Gan_icon(ma_tran, panel); pygame.display.update(); pygame.time.delay(450)
                                    hs = Lay_Huong_Sap(level)
                                    if hs: Sap_Hinh(hs)
                                    return True
        return False

    def Tu_Dong_BFS_Non(doi_tuong,max_steps=5000, pham_vi_init=2):
        nonlocal ma_tran
        agent_map = [[-1] * 12 for _ in range(12)]
        niemtin = doi_tuong.KhoiTao_NiemTin_Non(10)

        start_candidates = [(i, j) for i in range(1, 11) for j in range(1, 11) if ma_tran[i][j] != 0]
        if not start_candidates:
            print("Kết thúc")
            return
        x, y = random.choice(start_candidates)

        danh_sach = doi_tuong.Quan_Sat(agent_map,  x, y, pham_vi=pham_vi_init)
        doi_tuong.Cap_Nhat_Niem_Tin_Sau_Quan_Sat(niemtin, agent_map, danh_sach)

        def cap_nhat_giao_dien():
            try:
                man_hinh.blit(img_bg, (0, 0))
                man_hinh.blit(panel, (100, 170))
                ma_tran = doi_tuong.ma_tran
                Gan_icon(ma_tran, panel)
                pygame.display.update()
                pygame.time.wait(600)
            except Exception:
                pass

        step = 0
        while step < max_steps:
            step += 1
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    return "quit"
                if ev.type == pygame.KEYDOWN and ev.key == pygame.K_p:
                    # báo cho main loop biết đã pause — trả về để main xử lý
                    return "paused"


            if step % 10 == 1:
                print(
                    f"[Bước {step}] Số ô đã biết: {sum(1 for i in range(12) for j in range(12) if agent_map[i][j] != -1)}")

            if all(ma_tran[i][j] == 0 for i in range(1, 11) for j in range(1, 11)):
                break
            if not doi_tuong.Cap_Kha_Nang_An(niemtin):
                unknowns = [(i, j) for i in range(1, 11) for j in range(1, 11) if
                            agent_map[i][j] == -1 and ma_tran[i][j] != 0]
                if not unknowns:
                    print("Không còn ô chưa biết để mở rộng niềm tin. Dừng.")
                    break
                x_new, y_new = random.choice(unknowns)
                print(f"Không thấy cặp khả năng nên chuyển đến quan sát ô chưa biết {(x_new, y_new)}")
                danh_sach = doi_tuong.Quan_Sat(agent_map,  x_new, y_new, pham_vi=pham_vi_init)
                doi_tuong.Cap_Nhat_Niem_Tin_Sau_Quan_Sat(niemtin, agent_map, danh_sach)
                cap_nhat_giao_dien()
                continue
            v, p1, p2 = doi_tuong.Doan_Cap_Tu_Niem_Tin(niemtin)
            if v is None:
                print("Không tìm được cặp nào")
                break

            print(f"Agent đoán: ô {p1} và ô {p2} có thể là loại {v}")

            ds1 = doi_tuong.Quan_Sat(agent_map, p1[0], p1[1], pham_vi=1)
            doi_tuong.Cap_Nhat_Niem_Tin_Sau_Quan_Sat(niemtin, agent_map, ds1)
            ds2 = doi_tuong.Quan_Sat(agent_map,  p2[0], p2[1], pham_vi=1)
            doi_tuong.Cap_Nhat_Niem_Tin_Sau_Quan_Sat(niemtin, agent_map, ds2)

            if doi_tuong.Co_The_An_BFS(agent_map, p1, p2, niemtin):
                print(f"Ăn đuọce cặp {v} tại {p1} và {p2}!\n")
                try:
                    Ve_Duong_Di([p1, p2], panel)
                    cap_nhat_giao_dien()
                    pygame.time.wait(180)
                except Exception:
                    pass
                ma_tran[p1[0]][p1[1]] = ma_tran[p2[0]][p2[1]] = 0
                agent_map[p1[0]][p1[1]] = agent_map[p2[0]][p2[1]] = 0
                niemtin[p1].clear()
                niemtin[p2].clear()
                x, y = p2
            cap_nhat_giao_dien()

    def Tu_Dong_BFS_1_P(doi_tuong, max_steps=5000, pham_vi_init=2):
        nonlocal ma_tran
        start_candidates = [(i, j) for i in range(1, 11) for j in range(1, 11) if ma_tran[i][j] != 0]
        if not start_candidates:
            print("Không có ô hợp lệ để bắt đầu.")
            return
        x, y = random.choice(start_candidates)

        agent_map, niemtin = doi_tuong.KhoiTao_NiemTin_1_P(ma_tran, (x, y), pham_vi=pham_vi_init)

        queue = doi_tuong.deque([(x, y)])
        visited = set([(x, y)])

        def cap_nhat_giao_dien():
            try:
                man_hinh.blit(img_bg, (0, 0))
                man_hinh.blit(panel, (100, 170))
                Gan_icon(ma_tran, panel)
                pygame.display.update()
                pygame.time.wait(120)
            except Exception:
                pass

        step = 0
        while queue and step < max_steps:
            step += 1
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    return "quit"
                if ev.type == pygame.KEYDOWN and ev.key == pygame.K_p:
                    return "paused"


            x, y = queue.popleft()

            if step % 10 == 1:
                print(f"[Bước {step}] Agent tại {(x, y)}")

            if all(ma_tran[i][j] == 0 for i in range(1, 11) for j in range(1, 11)):
                print("Xong")
                break

            danh_sach_thay_doi = doi_tuong.Quan_Sat_1_P(agent_map, ma_tran, x, y, pham_vi=pham_vi_init)
            for (nx, ny) in danh_sach_thay_doi:
                val = agent_map[nx][ny]
                niemtin[(nx, ny)] = {val} if val != 0 else set()

            cap = []
            for v in range(1, 11):
                pos = [(i, j) for (i, j), tap in niemtin.items() if v in tap]
                for i in range(len(pos)):
                    for j in range(i + 1, len(pos)):
                        p1, p2 = pos[i], pos[j]
                        if doi_tuong.Co_The_An_BFS(agent_map, p1, p2, niemtin):
                            cap.append((v, p1, p2))

            if cap:
                v, p1, p2 = random.choice(cap)
                print(f"==> Ăn cặp {v} tại {p1} và {p2}")
                try:
                    Ve_Duong_Di([p1, p2], panel)
                    cap_nhat_giao_dien()
                except Exception:
                    pass
                ma_tran[p1[0]][p1[1]] = ma_tran[p2[0]][p2[1]] = 0
                agent_map[p1[0]][p1[1]] = agent_map[p2[0]][p2[1]] = 0
                niemtin[p1].clear()
                niemtin[p2].clear()
                cap_nhat_giao_dien()

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 1 <= nx < 11 and 1 <= ny < 11 and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    if agent_map[nx][ny] != 0:
                        queue.append((nx, ny))

            cap_nhat_giao_dien()

    img_congrats = pygame.image.load("mankey (1).png").convert_alpha()

    def Show_Congrats(surface, bg_img,  seconds=1.2):
        # scale icon về kích thước gọn
        tw, th = 320, 320
        if level == 2:
            icon = pygame.image.load("pokeball (1) (1).png").convert_alpha()
        if level == 3:
            icon = pygame.image.load("ultra-ball (1).png").convert_alpha()
        if level == 4:
            icon = pygame.image.load("insignia (1).png").convert_alpha()
        if level == 5:
            icon = pygame.image.load("game (2) (1).png").convert_alpha()
        if level == 6:
            icon = pygame.image.load("crown (1).png").convert_alpha()


        icon = pygame.transform.smoothscale(icon, (tw, th))
        cx, cy = surface.get_width() // 2, surface.get_height() // 2

        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))  # nền đen mờ

        start_ticks = pygame.time.get_ticks()
        duration_ms = int(seconds * 1000)
        clock = pygame.time.Clock()

        while True:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    return
                if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    return

            now = pygame.time.get_ticks()
            t = (now - start_ticks) / duration_ms

            surface.blit(bg_img, (0, 0))
            surface.blit(overlay, (0, 0))

            a = int(255 * t)
            icon_a = icon.copy()
            icon_a.set_alpha(a)

            rect = icon_a.get_rect(center=(cx, cy))
            surface.blit(icon_a, rect.topleft)

            pygame.display.update()
            clock.tick(60)
            if t >= 1.0:
                break
        pygame.time.delay(600)

    running_game = True
    paused = False
    clock = pygame.time.Clock()
    while running_game:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_game = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running_game = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                paused = not paused   # bật / tắt chế độ tạm dừng
                if paused:
                    print(" Game paused")
                else:
                    print(" Game resumed")

        man_hinh.blit(img_bg,(0,0))
        man_hinh.blit(panel,(100,170))
        Gan_icon(ma_tran, panel)

        if paused:
            Ghi_Lich_Su(selected_alg, level, start_time)

            # Vẽ chữ "PAUSED" giữa màn hình
            text = font.render("PAUSED", True, (255, 50, 50))
            man_hinh.blit(text, (GAME_W//2 - text.get_width()//2, GAME_H//2 - text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(100)
            continue  # bỏ qua phần xử lý tự động, chỉ giữ hình tĩnh


        name = doi_tuong.__class__.__name__.lower()

        if ("bk" in name) : ham = Tu_Dong_1(doi_tuong)
        elif any(k in name for k in ("mu1phan", "mu1p", "mu_1_phan", "mu_1", "mu 1 phan")):ham = Tu_Dong_BFS_1_P(doi_tuong)
        elif "mu" in name : ham = Tu_Dong_BFS_Non(doi_tuong)
        else: ham = Tu_Dong(doi_tuong)
        # Nếu hàm trả "paused" thì bật paused ở main và lưu lịch sử
        if ham == "paused":
            paused = True
            try:
                Ghi_Lich_Su(selected_alg, level, start_time)
            except Exception as e:
                print("Lỗi khi lưu lịch sử khi pause:", e)
            continue

        # nếu hàm trả "quit" -> thoát vòng game
        if ham == "quit":
            running_game = False
            break
        if not ham:
            if Kiem_Tra_Het():
                try:
                    sfx_levelup = pygame.mixer.Sound("PIKACHU SONG 1 HOUR")
                    sfx_levelup.set_volume(0.8)
                    sfx_levelup.play()
                except:
                    pass
                Show_Congrats(man_hinh, img_bg, seconds=1.0)


                ma_tran = Tao_board_game()
                doi_tuong.ma_tran = ma_tran
            else:
                ham_reset()
        pygame.display.update()
        pygame.time.delay(150)

    pygame.display.set_mode((MENU_W, MENU_H))
    pygame.display.set_caption("Pikachu Menu")





def main():

    global selected, choosing_screen, temp_selected
    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not choosing_screen:
                    if play_button.collidepoint(event.pos):
                        if selected is not None:
                            run_pikachu(algorithms[selected])
                        else:
                            print("Chưa chọn thuật toán!")
                    elif history_button.collidepoint(event.pos):
                        from history_gui import Mo_Giao_Dien_Lich_Su
                        Mo_Giao_Dien_Lich_Su()

                    elif choose_button.collidepoint(event.pos):
                        choosing_screen = True
                        temp_selected = selected
                else:
                    for i, rect in enumerate(algorithm_rects):
                        if rect and rect.collidepoint(event.pos):
                            temp_selected = i
                    if confirm_button.collidepoint(event.pos):
                        selected = temp_selected
                        choosing_screen = False
                    elif cancel_button.collidepoint(event.pos):
                        choosing_screen = False

        if not choosing_screen:
            draw_main_menu()
        else:
            draw_choose_screen()

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
