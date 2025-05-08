import pygame
import sys
import random
from pygame import time
pygame.init()
info = pygame.display.Info()
w = info.current_w // 3
h = info.current_h // 1.1
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption("worldofwarplanes")
bg = pygame.image.load("bg.png")
bg = pygame.transform.scale(bg, (w, h))
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

pl_r = 10
pl_x = w // 2
pl_y = h - pl_r - 10
speed = 102

npcs = []
n = 0
n1 = 900

bs = []
b_speed = 10
b_height = 15
b_width = 3

sc = 0
high_sc = 0

try:
    with open("s.txt", "r") as f:
        high_sc = int(f.read())
except:
    pass

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

game_over = False

while not game_over:
    curt = time.get_ticks()
    
    if curt - n > n1:
        for _ in range(1):
            texture = random.choice(n_png)
            npcs.append([random.randint(10, w-10), -10, 25, 5, 0.5, texture])
        n = curt
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over:
            bs.append([pl_x, pl_y - pl_r, b_width, b_height])
    
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
            game_over = True
        else:
            screen.blit(npc[5], (npc[0], npc[1]))
    
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
                npcs.remove(npc)
                sc += 1
                hit = True
                break
        
        if hit:
            bs.remove(b)
            continue
        
        pygame.draw.rect(screen, (0, 255, 0), (b[0], b[1], b[2], b[3]))
    
    pygame.draw.circle(screen, (255, 0, 0), (pl_x, pl_y), pl_r)
    
    if game_over:
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
