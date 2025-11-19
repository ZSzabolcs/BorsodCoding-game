import pygame
from pygame.locals import *
import os
import worlds
import asyncio
import json
import requests
import datetime
# Feltételezett külső modulok importálása
from login import loginWindow
from menu import menu_page
from styles import Color
from styles import set_language
from styles import languages
from styles import Selected_fonts
from world import World

# 📐 Konstansok a reszponzivitáshoz
# Ez a fix felbontás az arányok számításának alapja.
ORIGINAL_WIDTH = 1000
ORIGINAL_HEIGHT = 1000

# 💾 Játékmentés
def saving_game(points, level, chosen_lang, name):
    saving = {
        "name": name,
        "points" : points,
        "level" : level,
        "language" : chosen_lang,
        "date" : datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    }
    url = "http://localhost:5233/api/UserSaveData"

    try:
        response = requests.post(url=url, json=saving)
        response.raise_for_status()
        print(response.text)
    except requests.exceptions.RequestException as e:
        print(f"Hiba történt a mentéskor: {e}")
    
    with open("saves.csv", "w") as file:
        file.write(f"{str(points)} {str(level)} {chosen_lang}")

# 👤 Inicializálás
NAME = "Guest"

pygame.init()

fonts = Selected_fonts()

screen_width = ORIGINAL_WIDTH
screen_height = ORIGINAL_HEIGHT

choosen_language = set_language()

# Feltételezve, hogy a menu_page ORIGINAL_WIDTH/HEIGHT értékeket használ.
data = menu_page(ORIGINAL_WIDTH, ORIGINAL_HEIGHT, fonts, choosen_language, languages)

points = data[0]
level = data[1]
choosen_language = data[2]
music_is_on = data[3]

if music_is_on:
    background_music = pygame.mixer.Sound("Jazz In Paris  Media Right Productions (No Copyright Music).mp3")
    background_music.set_volume(0.6)
    background_music.play(-1)


# Képernyő beállítása RESIZABLE flaggel
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption(languages[choosen_language][0])

# Eredeti képek betöltése
bg_img_orig = pygame.image.load(os.path.join("kepek", "hatter.png")).convert()
bg2_img_orig = pygame.image.load(os.path.join("kepek", "hatter2.png")).convert()
bg3_img_orig = pygame.image.load(os.path.join("kepek", "hatter3.png")).convert()
bg4_img_orig = pygame.image.load(os.path.join("kepek", "hatter4.png")).convert()

# --- Háttérképek dinamikus méretezése ---
def scale_backgrounds(width, height):
    global bg_img, bg2_img, bg3_img, bg4_img
    bg_img = pygame.transform.scale(bg_img_orig, (width, height))
    bg2_img = pygame.transform.scale(bg2_img_orig, (width, height))
    bg3_img = pygame.transform.scale(bg3_img_orig, (width, height))
    bg4_img = pygame.transform.scale(bg4_img_orig, (width, height))

scale_backgrounds(screen_width, screen_height)

# --- In-game menü rect-ek arányosítása ---
def update_menu_rects(current_width, current_height):
    World.in_game_menu_rects = [
        # Az eredeti arányokat használjuk (270, 450, 500, 100)
        pygame.rect.Rect(
            current_width * 0.27, 
            current_height / 2 - current_height * 0.05, 
            current_width * 0.5, 
            current_height * 0.1
        )
    ]

# 🗺️ Világszintek létrehozása
level_name = languages[choosen_language]["in game"][0]
world = World(worlds.world_data, 1, f"{level_name}: 1")
world2 = World(worlds.world2_data, 2, f"{level_name}: 2")
world3 = World(worlds.world3_data, 3, f"{level_name}: 3")
world4 = World(worlds.world4_data, 4, f"{level_name}: 4")
world5 = World(worlds.world5_data, 5, f"{level_name}: 5")
world6 = World(worlds.world6_data, 6, f"{level_name}: 6")
world7 = World(worlds.world7_data, 7, f"{level_name}: 7")
world8 = World(worlds.world8_data, 8, f"{level_name}: 8")
world9 = World(worlds.world9_data, 9, f"{level_name}: 9")
world10 = World(worlds.world10_data, 10, f"{level_name}: 10")
World.worlds_list = [world, world2, world3, world4, world5, world6, world7, world8, world9, world10]

update_menu_rects(screen_width, screen_height)


# 🕹️ Fő játékhurok
async def main(level):
    run = 1
    completed = 0
    clock = pygame.time.Clock()
    FPS = 60
    pause = 0
    
    global screen_width, screen_height 
    
    while run and not pause:
        
        current_world = World.worlds_list[level - 1]
        clock.tick(FPS)
        
        # Háttér kirajzolása (dinamikusan méretezve)
        if level < 4:
            screen.blit(bg_img, (0, 0))
        elif level >= 4 and level <= 5:
            screen.blit(bg2_img, (0, 0))
        elif level >= 6 and level <= 8:
            screen.blit(bg3_img, (0, 0))
        elif level >= 9:
            screen.blit(bg4_img, (0, 0))

        # Játék elemek kirajzolása és frissítése
        current_world.draw(pause, run, languages, choosen_language, fonts, screen, mouse=None)
        current_world.draw_broken_blocks(screen)
        player = current_world.get_player()
        current_world.world_enemy_group.update(current_world.tile_list)
        current_world.world_enemy_group.draw(screen)
        current_world.fireballs_group.update()
        current_world.fireballs_group.draw(screen)
        current_world.stalactite_group.draw(screen)
        current_world.stalactite_group.update(player, current_world.tile_list)
        completed = player.update(current_world.tile_list, current_world.entities, screen)

        if completed == 1:
            level += 1
            completed = 0
            player = World.set_player_next_level(level, completed, player.checkpoint_x, player.checkpoint_y)
            continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = 0
            
            # ✅ RESIZE esemény kezelése
            elif event.type == pygame.VIDEORESIZE:
                screen_width = event.w
                screen_height = event.h
                scale_backgrounds(screen_width, screen_height)
                update_menu_rects(screen_width, screen_height)
                
                # 📢 A JÁTÉK ELEMEINEK ÁTMÉRETEZÉSE (feltételezett metódushívás)
                current_world.handle_resize(screen_width, screen_height) 
            # --------------------------

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pause = 1
                run = 0


        # ⏸️ Szüneteltetett hurok
        while not run and pause:
            mouse = pygame.mouse.get_pos()
            current_world.draw(pause, run, languages, fonts=fonts, ch_lang=choosen_language, screen=screen, mouse=mouse)

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pause = 0
                    run = 1
                elif event.type == pygame.QUIT:
                    pause = 0
                    run = 0
                
                # ✅ RESIZE esemény kezelése a szünetben is
                elif event.type == pygame.VIDEORESIZE:
                    screen_width = event.w
                    screen_height = event.h
                    scale_backgrounds(screen_width, screen_height)
                    update_menu_rects(screen_width, screen_height)
                    # 📢 JÁTÉK ELEMEINEK ÁTMÉRETEZÉSE
                    current_world.handle_resize(screen_width, screen_height)
                # ---------------------------------------------

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for rect in World.in_game_menu_rects:
                        if rect.collidepoint(float(mouse[0]), float(mouse[1])):
                            if World.in_game_menu_rects.index(rect) == 0:
                                pause, run = 0, 0


            pygame.display.flip()
            await asyncio.sleep(0)

    if not run and not pause:
        saving_game(points, level, choosen_language, NAME)
        pygame.quit()

asyncio.run(main(level))