import pygame
from pygame.locals import *
import sys
import time
from styles import Color # Feltételezzük, hogy a 'styles' modul létezik

# 📐 Konstansok az arányos szövegpozícióhoz
ORIGINAL_WIDTH = 1000
ORIGINAL_HEIGHT = 1000
ORIGINAL_FONT_OFFSET = 15 # Az eredeti -15 pixel eltolás y irányban

def start_new_game(ch_lang):
    with open("saves.csv", "w") as file:
        file.write(f"0 1 {ch_lang}")


def no_saves_warning(window, window_width, window_height, fonts, ch_lang, languages):
    # A szöveg és a pozíció arányosítása
    x_pos = window_width * 0.2
    y_pos = window_height * 0.4
    
    do_not_have_saves = fonts.font_size100.render(languages[ch_lang][6], 0, Color().BLUE, Color().BLACK)
    do_not_have_saves_place = (x_pos, y_pos)
    window.blit(do_not_have_saves, do_not_have_saves_place)
    pygame.display.update()
    time.sleep(2)


def load_saved_state(choosen_lang, music):
    changed = False
    d1_saved = 0
    d2_saved = 0
    d3_saved = ""
    try:
        with open("saves.csv", "r") as file:
            row = file.readline().split(" ")
            d1 = int(row[0])
            d2 = int(row[1])
            d3 = str(row[2]).strip() 
            
            if d3 != choosen_lang:
                changed = True
                d1_saved = d1
                d2_saved = d2
                d3_saved = choosen_lang
    except (FileNotFoundError, IndexError, ValueError):
        raise FileNotFoundError("A mentési fájl hibás vagy nem létezik.")
    
    
    if changed:
        with open("saves.csv", "w") as file:
            file.write(f"{str(d1_saved)} {str(d2_saved)} {d3_saved}")
        return d1_saved, d2_saved, d3_saved, music
    else:
        return d1, d2, d3, music


# ⚙️ Segédfüggvény a menü gombok generálásához
def create_menu_rects(w, h):
    # A menügombok arányos elhelyezése
    return [
        pygame.Rect(w*0.25, h*0.15, w*0.5, h*0.1),  # New Game
        pygame.Rect(w*0.25, h*0.3, w*0.5, h*0.1),   # Load Game
        pygame.Rect(w*0.25, h*0.45, w*0.5, h*0.1),  # Language
        pygame.Rect(w*0.25, h*0.6, w*0.5, h*0.1),   # Music
        pygame.Rect(w*0.25, h*0.75, w*0.5, h*0.1)   # Quit
    ]

# 📝 Segédfüggvény a szöveg elhelyezéséhez a gomb közepén (arányszámítás)
def get_text_place(rect, ch_lang, w, h):
    
    # 1. Kiszámoljuk az Y tengely eltolását (az eredeti -15 pixel arányosítva)
    y_offset = h * (ORIGINAL_FONT_OFFSET / ORIGINAL_HEIGHT)
    y_pos = rect.centery - y_offset
    
    # 2. X tengely eltolása (A mentett arányok alapján)
    index = menu_page.rects.index(rect) 
    
    if ch_lang == "en":
        ratios = [0.17, 0.25, 0.40, 0.20, 0.30] # New Game, Load Game, Language, Music, Quit
    else: # Hungarian (hu)
        ratios = [0.13, 0.25, 0.35, 0.15, 0.45] # Új játék, Mentés betöltése, Nyelvválasztás, Zene ki/be, Kilépés
    
    x_ratio = ratios[index]
    x_pos = rect.centerx * (1 - x_ratio)
    
    return (x_pos, y_pos)


def menu_page(window_width, window_height, fonts, ch_lang, languages):
    
    # Képernyő beállítása RESIZABLE flaggel
    window = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)
    
    # Globális változó, hogy a segédfüggvény hozzáférjen
    menu_page.rects = create_menu_rects(window_width, window_height)
    
    music_is_on = True
    run = 1
    
    while run:
        # Frissítjük a méreteket a ciklus elején
        current_w, current_h = window.get_size()
        mouse = pygame.mouse.get_pos()
        
        window.fill((255, 255, 255))

        for rect in menu_page.rects:
            square = pygame.draw.rect(window, Color().BLACK, rect)
            if square.collidepoint(float(mouse[0]), float(mouse[1])):
                square = pygame.draw.rect(window, Color().BLUE, rect)

        # Szövegek renderelése
        new_game_text = fonts.font_size50.render(languages[ch_lang][1], 0, Color().RED)
        load_game_text = fonts.font_size50.render(languages[ch_lang][2], 0, Color().RED)
        choosen_language_text = fonts.font_size50.render(languages[ch_lang][3], 0, Color().RED)

        if music_is_on:
            music_button_text = fonts.font_size50.render(languages[ch_lang][4][0], 0, Color().RED)
        else:
            music_button_text = fonts.font_size50.render(languages[ch_lang][4][1], 0, Color().RED)

        quit_game_text = fonts.font_size50.render(languages[ch_lang][5], 0, Color().RED)
        
        # 📝 Szövegpozíciók dinamikus számítása és kirajzolása
        text_list = [new_game_text, load_game_text, choosen_language_text, music_button_text, quit_game_text]
        
        for i, rect in enumerate(menu_page.rects):
            text_place = get_text_place(rect, ch_lang, current_w, current_h)
            window.blit(text_list[i], text_place)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # 🔄 RESIZE ESEMÉNY KEZELÉSE A MENÜBEN
            elif event.type == pygame.VIDEORESIZE:
                window_width = event.w
                window_height = event.h
                # Képernyő újra beállítása
                window = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)
                # Menü rects frissítése az új méretekkel
                menu_page.rects = create_menu_rects(window_width, window_height)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                for rect in menu_page.rects:
                    if rect.collidepoint(float(mouse[0]), float(mouse[1])):
                        index = menu_page.rects.index(rect)
                        
                        if index == 0:  # New Game
                            try:
                                start_new_game(ch_lang)
                                data = load_saved_state(ch_lang, music_is_on)
                                return data
                            except Exception:
                                no_saves_warning(window, window_width, window_height, fonts, ch_lang, languages)

                        elif index == 1:  # Load Game
                            try:
                                data = load_saved_state(ch_lang, music_is_on)
                                return data
                            except Exception:
                                no_saves_warning(window, window_width, window_height, fonts, ch_lang, languages)

                        elif index == 2:  # Language
                            ch_lang = "hu" if ch_lang == "en" else "en"
                        
                        elif index == 3:  # Music
                            music_is_on = not music_is_on

                        elif index == 4:  # Quit
                            pygame.quit()
                            sys.exit()

        pygame.display.flip()