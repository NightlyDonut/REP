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


def startg(screen, w, h, hard_mode=False):
    print("PRESS [ESC] FOR PAUSE/SHOP MENU")
    if hard_mode:
        print("hard")

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
    isUhi = False
    bot_x = w // 4
    bot_y = h - pl_r - 10
    bot_last_shot = 0
    uhiDel = 1500 

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
    
    bssl = -1
    upgs = {
        "af1": False, 
        "af2": False,  
        "trsh": False,  
        "uhilyant": False    
    }
    
    cash_m = {
        "af1": 1000,
        "af2": 2500,
        "trsh": 5000,
        "uhilyant": 10000
    }
    
    last_auto_shot = 0
    auto_fire_delay = 2000

    try:
        with open("s.txt", "r") as f:
            high_sc = int(f.read())
    except:
        pass

    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)
    small_font = pygame.font.SysFont(None, 20)
    smaller_font = pygame.font.SysFont(None, 16)

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
                    if upgs["trsh"]:
                        bs.append([pl_x, pl_y - pl_r, b_width, b_height])  
                        bs.append([pl_x - 15, pl_y - pl_r + 5, b_width, b_height])  
                        bs.append([pl_x + 15, pl_y - pl_r + 5, b_width, b_height])  
                    else:
                        bs.append([pl_x, pl_y - pl_r, b_width, b_height])
                elif freeze:
                    mouse_pos = event.pos
                    shop_x = w // 2 - shop_uw.get_width() // 2
                    shop_y = 120
                    button_height = 50
                    button_margin = 10
                    upg1_button = pygame.Rect(shop_x + 20, shop_y + 20, shop_uw.get_width() - 40, button_height)
                    if upg1_button.collidepoint(mouse_pos):
                        if cash >= cash_m["af1"] and not upgs["af1"]:
                            cash -= cash_m["af1"]
                            upgs["af1"] = True
                            print(f"-{cash_m['af1']} $ - bought auto fire (delay 2s)")
                    upg2_button = pygame.Rect(shop_x + 20, shop_y + 20 + button_height + button_margin, shop_uw.get_width() - 40, button_height)
                    if upg2_button.collidepoint(mouse_pos):
                        if cash >= cash_m["af2"] and upgs["af1"] and not upgs["af2"]:
                            cash -= cash_m["af2"]
                            upgs["af2"] = True
                            auto_fire_delay = 900
                            print(f"-{cash_m['af2']} $ - bought auto fire (delay 1s)")
                    upg3_button = pygame.Rect(shop_x + 20, shop_y + 20 + 2 * (button_height + button_margin), shop_uw.get_width() - 40, button_height)
                    if upg3_button.collidepoint(mouse_pos):
                        if cash >= cash_m["trsh"] and not upgs["trsh"]:
                            cash -= cash_m["trsh"]
                            upgs["trsh"] = True
                            print(f"-{cash_m['trsh']} $ - bought triple shot")
                    
                    upg4_button = pygame.Rect(shop_x + 20, shop_y + 20 + 3 * (button_height + button_margin), shop_uw.get_width() - 40, button_height)
                    if upg4_button.collidepoint(mouse_pos):
                        if cash >= cash_m["uhilyant"] and not upgs["uhilyant"]:
                            cash -= cash_m["uhilyant"]
                            upgs["uhilyant"] = True
                            isUhi = True
                            print(f"-{cash_m['uhilyant']} $ - bought Друга Ухилянта")
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    freeze = not freeze 
                    if freeze:
                        screen.blit(frezgui, (0, 0))
                        shop_x = w // 2 - shop_uw.get_width() // 2
                        shop_y = 120 
                        screen.blit(shop_uw, (shop_x, shop_y))
                        
                        frzgui = font.render(f"Score: {sc} | Cash: {cash}", True, (255, 255, 255))
                        text_x = w // 2 - frzgui.get_width() // 2 
                        text_y = 80 
                        screen.blit(frzgui, (text_x, text_y))
                        
                        button_height = 50
                        button_margin = 10
                        
                        #first upg
                        button_color = (50, 200, 50) if cash >= cash_m["af1"] and not upgs["af1"] else (200, 50, 50) if not upgs["af1"] else (100, 100, 100)
                        pygame.draw.rect(screen, button_color, (shop_x + 20, shop_y + 20, shop_uw.get_width() - 40, button_height))
                        pygame.draw.rect(screen, BLACK, (shop_x + 20, shop_y + 20, shop_uw.get_width() - 40, button_height), 2)
                        if upgs["af1"]:
                            sh0p = "auto fire (delay 2s) - bought"
                        else:
                            sh0p = f"auto fire (delay 2s) [{cash_m['af1']} $]"
                        button_label = small_font.render(sh0p, True, BLACK)
                        screen.blit(button_label, (shop_x + shop_uw.get_width()//2 - button_label.get_width()//2, 
                                                  shop_y + 20 + button_height//2 - button_label.get_height()//2))
                        
                        #second upg
                        button_color = (50, 200, 50) if cash >= cash_m["af2"] and upgs["af1"] and not upgs["af2"] else (200, 50, 50) if not upgs["af2"] else (100, 100, 100)
                        pygame.draw.rect(screen, button_color, (shop_x + 20, shop_y + 20 + button_height + button_margin, shop_uw.get_width() - 40, button_height))
                        pygame.draw.rect(screen, BLACK, (shop_x + 20, shop_y + 20 + button_height + button_margin, shop_uw.get_width() - 40, button_height), 2)
                        if upgs["af2"]:
                            sh0p = "auto fire (delay 1s) bought"
                        else:
                            sh0p = f"auto fire (delay 1s) [{cash_m['af2']} $]"
                            if not upgs["af1"]:
                                sh0p += " need auto fire 2s"
                        button_label = small_font.render(sh0p, True, BLACK)
                        screen.blit(button_label, (shop_x + shop_uw.get_width()//2 - button_label.get_width()//2, 
                                                  shop_y + 20 + button_height + button_margin + button_height//2 - button_label.get_height()//2))
                        
                        #third upg
                        button_color = (50, 200, 50) if cash >= cash_m["trsh"] and not upgs["trsh"] else (200, 50, 50) if not upgs["trsh"] else (100, 100, 100)
                        pygame.draw.rect(screen, button_color, (shop_x + 20, shop_y + 20 + 2*(button_height + button_margin), shop_uw.get_width() - 40, button_height))
                        pygame.draw.rect(screen, BLACK, (shop_x + 20, shop_y + 20 + 2*(button_height + button_margin), shop_uw.get_width() - 40, button_height), 2)
                        if upgs["trsh"]:
                            sh0p = "triple shot [bought]"
                        else:
                            sh0p = f"triple shot [{cash_m['trsh']} $]"
                        button_label = small_font.render(sh0p, True, BLACK)
                        screen.blit(button_label, (shop_x + shop_uw.get_width()//2 - button_label.get_width()//2, 
                                                  shop_y + 20 + 2*(button_height + button_margin) + button_height//2 - button_label.get_height()//2))
                        
                        #fourth upg
                        button_color = (50, 200, 50) if cash >= cash_m["uhilyant"] and not upgs["uhilyant"] else (200, 50, 50) if not upgs["uhilyant"] else (100, 100, 100)
                        pygame.draw.rect(screen, button_color, (shop_x + 20, shop_y + 20 + 3*(button_height + button_margin), shop_uw.get_width() - 40, button_height))
                        pygame.draw.rect(screen, BLACK, (shop_x + 20, shop_y + 20 + 3*(button_height + button_margin), shop_uw.get_width() - 40, button_height), 2)
                        if upgs["uhilyant"]:
                            sh0p = "You bought - Друг Ухилянт"
                        else:
                            sh0p = f"Друг Ухилянт [{cash_m['uhilyant']} $]"
                        button_label = small_font.render(sh0p, True, BLACK)
                        screen.blit(button_label, (shop_x + shop_uw.get_width()//2 - button_label.get_width()//2, 
                                                  shop_y + 20 + 3*(button_height + button_margin) + button_height//2 - button_label.get_height()//2))
                        
                        pygame.display.flip()

        if not freeze:
            if (upgs["af1"] or upgs["af2"]) and curt - last_auto_shot >= auto_fire_delay:
                if upgs["trsh"]:
                    bs.append([pl_x, pl_y - pl_r, b_width, b_height])
                    bs.append([pl_x - 15, pl_y - pl_r + 5, b_width, b_height])
                    bs.append([pl_x + 15, pl_y - pl_r + 5, b_width, b_height])
                else:
                    bs.append([pl_x, pl_y - pl_r, b_width, b_height])
                last_auto_shot = curt
                
            if upgs["uhilyant"] and isUhi:
                if bot_x < pl_x - 100:
                    bot_x += 1
                elif bot_x > pl_x + 100:
                    bot_x -= 1
                    
                if curt - bot_last_shot >= uhiDel:
                    target_found = False
                    for npc in npcs:
                        if abs(npc[0] - bot_x) < 50:
                            target_found = True
                            bs.append([bot_x, bot_y - pl_r, b_width, b_height])
                            bot_last_shot = curt
                            break
                    if not target_found and random.random() < 0.3: 
                        bs.append([bot_x, bot_y - pl_r, b_width, b_height])
                        bot_last_shot = curt
                
            boss_active = any(npc[6] == 6666.666 for npc in npcs)
            if not boss_active and curt - n > n1:
                for _ in range(1):
                    texture = random.choice(n_png)
                    if hard_mode and sc > 0 and sc % 100 == 0 and sc != bssl:
                        boss_texture = pygame.transform.scale(texture, (80, 80)) 
                        npcs.append([random.randint(10, w-40), -10, 50, 5, 0.1, boss_texture, 6666.666, 6666.666])
                        bssl = sc 
                    else:
                        if hard_mode:
                            hp = random.choice([25, 100, 150, 245])
                            npcs.append([random.randint(10, w-20), -10, 25, 5, 1.5, texture, hp, hp])
                        else:
                            hp = random.choice([25, 100, 150])
                            npcs.append([random.randint(10, w-20), -10, 25, 5, 0.5, texture, hp, hp])
                n = curt

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
                    npc_rect = pygame.Rect(npc[0], npc[1], npc[2], npc[2])

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
            if upgs["uhilyant"] and isUhi:
                try:
                    helper_color = (100, 100, 255) 
                    helper_surface = pygame.Surface((40, 40))
                    helper_surface.fill(helper_color)
                    screen.blit(helper_surface, (bot_x - pl_r, bot_y - pl_r))
                    helper_txt = smaller_font.render("BOT", True, (255, 255, 255))
                    screen.blit(helper_txt, (bot_x - helper_txt.get_width()//2, bot_y - helper_txt.get_height()//2))
                except:
                    pass

            ###############################################
            stxt = font.render(f"Score: {sc}", True, (255,255,255))
            ctxt = font.render(f"Cash: {cash}", True, (255,255,0))
            screen.blit(stxt, (w - stxt.get_width() - 20, 20))
            screen.blit(ctxt, (w - ctxt.get_width() - 20, 60))
            y_offset = 20
            if upgs["af1"]:
                if upgs["af2"]:
                    auto_txt = small_font.render("auto: 1", True, (0, 255, 0))
                else:
                    auto_txt = small_font.render("auto: 2", True, (0, 255, 0))
                screen.blit(auto_txt, (20, y_offset))
                y_offset += 25
                
            if upgs["trsh"]:
                triple_txt = small_font.render("tripple shot", True, (0, 255, 0))
                screen.blit(triple_txt, (20, y_offset))
                y_offset += 25
                
            if upgs["uhilyant"]:
                bot_txt = small_font.render("ухилянта зловлено", True, (0, 255, 0))
                screen.blit(bot_txt, (20, y_offset))
                y_offset += 25
                
            if hard_mode:
                hard_txt = small_font.render("DEVILS WAIT FOR YOU", True, (255, 0, 0))
                screen.blit(hard_txt, (20, y_offset))
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
                helpC()
                startg(screen, w, h, hard_mode=True)

    screen.fill(WHITE)
    pygame.draw.rect(screen, GRAY, b1)
    pygame.draw.rect(screen, GRAY, b2)
    pygame.draw.rect(screen, GRAY, b3)
    pygame.draw.rect(screen, BLACK, b1, 2)
    pygame.draw.rect(screen, BLACK, b2, 2)
    pygame.draw.rect(screen, BLACK, b3, 2)

    h1 = font.render("Infinite Mayhem", True, BLACK)
    h2 = font.render("CREDITS", True, BLACK)
    h3 = font.render("HARDMODE", True, BLACK)

    screen.blit(h1, (b1.x + b_width//2 - h1.get_width()//2, b1.y + b_height//2 - h1.get_height()//2))
    screen.blit(h2, (b2.x + b_width//2 - h2.get_width()//2, b2.y + b_height//2 - h2.get_height()//2))
    screen.blit(h3, (b3.x + b_width//2 - h3.get_width()//2, b3.y + b_height//2 - h3.get_height()//2))

    pygame.display.flip()

pygame.quit()
sys.exit()