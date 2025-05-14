import pygame
import sys
import random
import os
from pygame import time

def helpC():
    try:
        sx1 = pygame.image.load("sx1.png")
        sx1_rect = sx1.get_rect()
        scale_w, scale_h = 1124, 450
        width, height = scale_w, scale_h
        sx1 = pygame.transform.scale(sx1, (width, height))
    except:
        width, height = 1124, 450
        sx1 = pygame.Surface((width, height))
        sx1.fill((0, 0, 0))

    try:
        sx2 = pygame.image.load("sx2.png")
        sx2 = pygame.transform.scale(sx2, (width, height)) 
    except:
        sx2 = pygame.Surface((width, height))
        sx2.fill((50, 50, 50))

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Welcome")

    cur_cutscene = 1 
    screen.blit(sx1, (0, 0))
    pygame.display.flip()

    delay = True
    while delay:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if cur_cutscene == 1:
                        screen.blit(sx2, (0, 0))
                        pygame.display.flip()
                        cur_cutscene = 2
                    else:
                        delay = False
                elif event.key == pygame.K_ESCAPE:
                    delay = False


def startg(screen, w, h):
    print("PRESS [ESC] FOR PAUSE/SHOP MENU")

    info = pygame.display.Info()
    w = 640
    h = 1000
    screen = pygame.display.set_mode((w, h))
    pygame.display.set_caption("worldofwarplanes")
    bg = pygame.image.load("bg.png")
    bg = pygame.transform.scale(bg, (w, h))
    try:
        pl_uw = pygame.image.load("pl.png")
        pl_uw = pygame.transform.scale(pl_uw, (40, 40))
    except:
        pl_uw = pygame.Surface((40, 40))
        pl_uw.fill((255, 0, 0))
    try:
        shop_uw = pygame.image.load("shop.png")
        shop_uw = pygame.transform.scale(shop_uw, (w // 2, h // 3))
    except:
        shop_uw = pygame.Surface((w // 2, h // 3))
        shop_uw.fill((100, 100, 255))
    
    n_png = []
    for i in range(1, 3):
        try:
            texture = pygame.image.load(f"npc{i}.png")
            texture = pygame.transform.scale(texture, (40, 40))
            n_png.append(texture)
        except:
            pass
    if not n_png:
        n_pngs = pygame.Surface((40, 40))
        n_pngs.fill((255, 0, 0))
        n_png.append(n_pngs)
    pl_r = 20 
    pl_x = w // 2
    pl_y = h - pl_r - 10
    speed = 102

    npcs = []
    n = 0
    n1 = 2000

    bs = []
    b_speed = 10
    b_height = 15
    b_width = 3

    sc = 0
    cash = 0
    high_sc = 0

    upg = False
    l_upg = 0
    upg_delay = 250

    try:
        with open("s.txt", "r") as f:
            high_sc = int(f.read())
    except:
        pass

    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)
    small_font = pygame.font.SysFont(None, 20)


    endg = False
    freeze = False
    frezgui = pygame.Surface((w, h))
    frezgui.set_alpha(200)
    frezgui.fill((52, 69, 56))

    while not endg:
        curt = time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not endg and not freeze:
                    bs.append([pl_x, pl_y - pl_r, b_width, b_height])
                elif freeze:
                    mouse_pos = event.pos
                    shop_x = w // 2 - shop_uw.get_width() // 120
                    shop_y = 120
                    bsh_x = shop_x - 100 
                    bsh_y = shop_y + shop_uw.get_height() // 2 
                    bsh_w = 150
                    bsh_h = 50
                    upg_button = pygame.Rect(bsh_x, bsh_y, bsh_w, bsh_h)
                    if upg_button.collidepoint(mouse_pos):
                        if cash >= 1000 and not upg:
                            cash -= 1000
                            upg = True
                            print("-1000 $")
                            print("bought upgrade")
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    freeze = not freeze 
                    if freeze:
                        screen.blit(frezgui, (0, 0))
                        shop_x = w // 2 - shop_uw.get_width() // 120
                        shop_y = 120 
                        screen.blit(shop_uw, (shop_x, shop_y))
                        
                        frzgui = font.render(f"[-]  [-]  . . . Score: {sc}", True, (255, 255, 255))
                        text_x = w // 2 - frzgui.get_width() // 2 
                        text_y = h - 100 
                        screen.blit(frzgui, (text_x, text_y))
                        bsh_x = shop_x - 100
                        bsh_y = shop_y + shop_uw.get_height() // 2
                        bsh_w = 150
                        bsh_h = 50
                        
                        button_color = (50, 200, 50) if cash >= 1000 and not upg else (200, 50, 50)
                        pygame.draw.rect(screen, button_color, (bsh_x, bsh_y, bsh_w, bsh_h))
                        pygame.draw.rect(screen, BLACK, (bsh_x, bsh_y, bsh_w, bsh_h), 2)
                        if upg:
                            button_text = "upgraded"
                        else:
                            button_text = "1000 $"
                            
                        button_label = font.render(button_text, True, BLACK)
                        screen.blit(button_label, (bsh_x + bsh_w//2 - button_label.get_width()//2, 
                                                  bsh_y + bsh_h//2 - button_label.get_height()//2))
                        
                        pygame.display.flip()

        if not freeze:
            if curt - n > n1:
                for _ in range(1):
                    texture = random.choice(n_png)
                    hp = random.choice([25, 100, 150])
                    npcs.append([random.randint(10, w-20), -10, 25, 5, 0.5, texture, hp, hp])
                n = curt
            if upg and curt - l_upg >= upg_delay:
                bs.append([pl_x, pl_y - pl_r, b_width, b_height])
                l_upg = curt

            mouse_x, mouse_y = pygame.mouse.get_pos()
            if mouse_x > pl_x:
                pl_x += min(speed, mouse_x - pl_x)
            elif mouse_x < pl_x:
                pl_x -= min(speed, pl_x - mouse_x)

            if pl_x < pl_r: pl_x = pl_r
            if pl_x > w - pl_r: pl_x = w - pl_r

            screen.blit(bg, (0, 0))

            for npc in npcs[:]:
                npc[1] += npc[4]
                if npc[1] > pl_y + pl_r:
                    endg = True
                else:
                    screen.blit(npc[5], (npc[0], npc[1]))
                    hp_text = small_font.render(f"{npc[6]} /of/ {npc[7]}", True, (255, 255, 255))
                    screen.blit(hp_text, (npc[0], npc[1] - 10))

            for b in bs[:]:
                b[1] -= b_speed

                if b[1] < 0:
                    bs.remove(b)
                    continue

                hit = False
                for npc in npcs[:]:
                    b_rect = pygame.Rect(b[0], b[1], b[2], b[3])
                    npc_rect = pygame.Rect(npc[0], npc[1], 25, 25)

                    if b_rect.colliderect(npc_rect):
                        npc[6] -= 25
                        if npc[6] <= 0:
                            npcs.remove(npc)
                            sc += 1
                            cash += 25
                        hit = True
                        break

                if hit:
                    bs.remove(b)
                    continue

                pygame.draw.rect(screen, (0, 255, 0), (b[0], b[1], b[2], b[3]))
            screen.blit(pl_uw, (pl_x - pl_r, pl_y - pl_r))

            ###############################################
            stxt = font.render(f"Score: {sc}", True, (255,255,255))
            ctxt = font.render(f"Cash: {cash}", True, (255,255,0))
            screen.blit(stxt, (w - stxt.get_width() - 20, 20))
            screen.blit(ctxt, (w - ctxt.get_width() - 20, 60))
            if upg:
                auto_txt = small_font.render("upgraded", True, (0, 255, 0))
                screen.blit(auto_txt, (20, 20))
            ###############################################
            if endg:
                if sc > high_sc:
                    high_sc = sc
                    with open("s.txt", "w") as f:
                        f.write(str(high_sc))
                screen.fill((0, 0, 0))
                end = font.render(f"End.//Результат: {sc}", True, (255, 255, 255))
                high = font.render(f"Найбільший: {high_sc}", True, (255, 255, 255))
                screen.blit(end, (w//2 - end.get_width()//2, h//2 - 50))
                screen.blit(high, (w//2 - high.get_width()//2, h//2 + 10))
                pygame.display.flip()
                pygame.time.wait(5000)
                break

            pygame.display.flip()
        clock.tick(120)

    pygame.quit()
    sys.exit()

def cred():
    pygame.init()
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("credits")
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    font = pygame.font.SysFont("Arial", 24)
    Cspd = 1 
    text_y = HEIGHT
    lh = 30

    def load_text(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                return file.read().splitlines()
        except:
            print(f"'{filename}' not found.")
            return []

    text_lines = load_text("cred.txt")
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        screen.fill(WHITE)
        c_y = text_y

        for line in text_lines:
            if c_y > -lh and c_y < HEIGHT:
                text_surface = font.render(line, True, BLACK)
                text_rect = text_surface.get_rect(centerx=WIDTH//2, y=c_y)
                screen.blit(text_surface, text_rect)
            c_y += lh

        text_y -= Cspd
        if c_y < 0:
            text_y = HEIGHT

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

pygame.init()
info = pygame.display.Info()
w = info.current_w // 3
h = int(info.current_h // 1.1)
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption("///----///")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
b_width = w - 40
b_height = 50
b_margin = 20
tb_height = 3 * b_height + 2 * b_margin
start_y = (h - tb_height) // 2

b1 = pygame.Rect(20, start_y, b_width, b_height)
b2 = pygame.Rect(20, start_y + b_height + b_margin, b_width, b_height)
b3 = pygame.Rect(20, start_y + 2*(b_height + b_margin), b_width, b_height)

font = pygame.font.SysFont('Arial', 20)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if b1.collidepoint(mouse_pos):
                helpC()
                startg(screen, w, h)
            elif b2.collidepoint(mouse_pos):
                cred()
            elif b3.collidepoint(mouse_pos):
                print("3")

    screen.fill(WHITE)
    pygame.draw.rect(screen, GRAY, b1)
    pygame.draw.rect(screen, GRAY, b2)
    pygame.draw.rect(screen, GRAY, b3)
    pygame.draw.rect(screen, BLACK, b1, 2)
    pygame.draw.rect(screen, BLACK, b2, 2)
    pygame.draw.rect(screen, BLACK, b3, 2)

    h1 = font.render("PLAY", True, BLACK)
    h2 = font.render("CREDITS", True, BLACK)
    h3 = font.render("HARDMODE", True, BLACK)

    screen.blit(h1, (b1.x + b_width//2 - h1.get_width()//2, b1.y + b_height//2 - h1.get_height()//2))
    screen.blit(h2, (b2.x + b_width//2 - h2.get_width()//2, b2.y + b_height//2 - h2.get_height()//2))
    screen.blit(h3, (b3.x + b_width//2 - h3.get_width()//2, b3.y + b_height//2 - h3.get_height()//2))

    pygame.display.flip()

pygame.quit()
sys.exit()
