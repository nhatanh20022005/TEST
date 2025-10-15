import pygame, sys, random

pygame.init()

WIDTH, HEIGHT = 977, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pikachu Menu")


bg_image = pygame.image.load("bg_menu2.jpg").convert()
bg_x, bg_y = 0, 0
bg_dx, bg_dy = 0.2, 0.1  # tốc độ chuyển động nền

font = pygame.font.SysFont("Tahoma", 28, bold=True)

algorithms = [
    "BFS", "DFS", "A*",
     "Greedy", "HillClimb", "BeamSearch",
    "Backtrack", "ForwardChk", "Mu1Phan","MuTP"
]

# --------- Nút ---------
play_button = pygame.Rect(WIDTH//2 - 150, HEIGHT - 100, 120, 50)
choose_button = pygame.Rect(WIDTH//2 + 30, HEIGHT - 100, 150, 50)

# --------- Rect cho màn chọn ---------
algorithm_rects = [None] * len(algorithms)
confirm_button = pygame.Rect(WIDTH//2 - 200, HEIGHT - 80, 150, 50)
cancel_button  = pygame.Rect(WIDTH//2 + 50, HEIGHT - 80, 150, 50)

# --------- Biến trạng thái ---------
selected = None
choosing_screen = False
temp_selected = None

# --------- Hàm vẽ background động ---------
def draw_background():
    global bg_x, bg_y, bg_dx, bg_dy
    bg_x += bg_dx
    bg_y += bg_dy
    if bg_x > 5 or bg_x < -6:
        bg_dx *= -1
    if bg_y > 7 or bg_y < -6:
        bg_dy *= -1
    screen.blit(bg_image, (int(bg_x), int(bg_y)))

# --------- Hàm vẽ menu chính ---------
def draw_main_menu():
    draw_background()
    mx, my = pygame.mouse.get_pos()

    # Hover cho Play
    play_color = (255, 235, 100) if play_button.collidepoint(mx, my) else (255, 215, 0)
    pygame.draw.rect(screen, play_color, play_button, border_radius=12)
    text = font.render("PLAY", True, (0, 0, 0))
    screen.blit(text, (play_button.centerx - text.get_width()//2,
                       play_button.centery - text.get_height()//2))

    # Hover cho Options
    opt_color = (150, 230, 255) if choose_button.collidepoint(mx, my) else (100, 200, 255)
    pygame.draw.rect(screen, opt_color, choose_button, border_radius=12)
    text = font.render("OPTIONS", True, (0, 0, 0))
    screen.blit(text, (choose_button.centerx - text.get_width()//2,
                       choose_button.centery - text.get_height()//2))

    # Hiện thuật toán đã chọn
    if selected is not None:
        label = font.render(f"CHECKED: {algorithms[selected]}", True, (0, 0, 0))
        pygame.draw.rect(screen, (230, 230, 230),
                         (WIDTH//2 - 160, HEIGHT - 160, 360, 50), border_radius=8)
        screen.blit(label, (WIDTH//2 - label.get_width()//2, HEIGHT - 155))

# --------- Hàm vẽ màn chọn thuật toán ---------
def draw_choose_screen():
    screen.fill((246, 241, 233))
    mx, my = pygame.mouse.get_pos()

    title = font.render("OPTIONS", True, (0, 0, 0))
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 30))

    cols = 3
    gap_x, gap_y = 220, 100
    start_x, start_y = 150, 100

    for i, alg in enumerate(algorithms):
        row, col = divmod(i, cols)
        rect = pygame.Rect(start_x + col * gap_x, start_y + row * gap_y, 200, 70)
        algorithm_rects[i] = rect

        if rect.collidepoint(mx, my):
            color = (130, 220, 255)
        elif temp_selected == i:
            color = (100, 200, 255)
        else:
            color = (255, 217, 61)

        pygame.draw.rect(screen, color, rect, border_radius=10)
        text = font.render(alg, True, (0, 0, 0))
        screen.blit(text, (rect.centerx - text.get_width()//2, rect.centery - text.get_height()//2))

    # Hover cho nút Accept/Cancel
    conf_color = (0, 230, 120) if confirm_button.collidepoint(mx, my) else (0, 200, 100)
    pygame.draw.rect(screen, conf_color, confirm_button, border_radius=12)
    text = font.render("ACCEPT", True, (255, 255, 255))
    screen.blit(text, (confirm_button.centerx - text.get_width()//2,
                       confirm_button.centery - text.get_height()//2))

    canc_color = (230, 70, 70) if cancel_button.collidepoint(mx, my) else (200, 50, 50)
    pygame.draw.rect(screen, canc_color, cancel_button, border_radius=12)
    text = font.render("CANCEL", True, (255, 255, 255))
    screen.blit(text, (cancel_button.centerx - text.get_width()//2,
                       cancel_button.centery - text.get_height()//2))

running = True
clock = pygame.time.Clock()

while running:
    clock.tick(60)  # FPS ổn định
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not choosing_screen:
                if play_button.collidepoint(event.pos):
                    if selected is not None:
                        print("Chạy thuật toán:", algorithms[selected])
                    else:
                        print("Chưa chọn thuật toán!")
                elif choose_button.collidepoint(event.pos):
                    choosing_screen = True
                    temp_selected = selected

            else:
                for i, rect in enumerate(algorithm_rects):
                    if rect and rect.collidepoint(event.pos):
                        temp_selected = i
                        print("Đang chọn:", algorithms[i])

                if confirm_button.collidepoint(event.pos):
                    selected = temp_selected
                    choosing_screen = False
                    print("Xác nhận:", algorithms[selected] if selected is not None else "Chưa chọn")
                elif cancel_button.collidepoint(event.pos):
                    choosing_screen = False
                    print("Hủy chọn")

    if not choosing_screen:
        draw_main_menu()
    else:
        draw_choose_screen()

    pygame.display.flip()

pygame.quit()
sys.exit()
