import pygame
from pygame.locals import *
import sys
from modulok.styles import Color
from modulok.styles import Selected_fonts

class Option:
    def __init__(self, screen, language: str, languages: dict, selected_font: Selected_fonts, musicIsOn = True):
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.fonts = selected_font
        self.language = language
        self.languages = languages
        self.musicIsOn = musicIsOn

class Save():
    def __init__(self, points = 0, level = 0, language = "", musicIsOn = True):
        self.points = points
        self.level = level
        self.language = language
        self.musicIsOn = musicIsOn


async def start_new_game(language, musicIsOn):
    newSave = Save()
    with open("saves.csv", "w") as file:
        file.write(f"0 1 {language}")
        file.close()
    newSave.level = 1
    newSave.language = language
    newSave.musicIsOn = musicIsOn
    return newSave






async def load_saved_state(language, musicIsOn):
    save = Save()
    with open("saves.csv", "r") as file:
        row = file.readline().split(" ")
        save.points = int(row[0])
        save.level = int(row[1])
        save.language = language
    save.musicIsOn = musicIsOn
    return save



async def menu_page(option : Option):

    window = option.screen
    rects = [
        pygame.Rect(window.get_width()*0.25, window.get_height()*0.15, window.get_width()*0.5, window.get_height()*0.1),
        pygame.Rect(window.get_width()*0.25, window.get_height()*0.3, window.get_width()*0.5, window.get_height()*0.1),
        pygame.Rect(window.get_width()*0.25, window.get_height()*0.45, window.get_width()*0.5, window.get_height()*0.1),
        pygame.Rect(window.get_width()*0.25, window.get_height()*0.6, window.get_width()*0.5, window.get_height()*0.1),
        pygame.Rect(window.get_width()*0.25, window.get_height()*0.75, window.get_width()*0.5, window.get_height()*0.1)

    ]
    run = 1
    loadedSave = Save()
    font_size = option.fonts.font_size40
    if window.get_width() == 1000 and window.get_height() == 1000:
        font_size = option.fonts.font_size50

    while run:
        mouse = pygame.mouse.get_pos()
        
        window.fill((255, 255, 255))

        for rect in rects:
            square = pygame.draw.rect(window, Color().BLACK, rect)
            if square.collidepoint(float(mouse[0]), float(mouse[1])):
                square = pygame.draw.rect(window, Color().BLUE, rect)

        new_game_text = font_size.render(option.languages[option.language][1], 0, Color().RED)

        load_game_text = font_size.render(option.languages[option.language][2], 0, Color().RED)

        choosen_language_text = font_size.render(option.languages[option.language][3], 0, Color().RED)

        if option.musicIsOn:
            music_button_text = font_size.render(option.languages[option.language][4][0], 0, Color().RED)
        else:
            music_button_text = font_size.render(option.languages[option.language][4][1], 0, Color().RED)

        quit_game_text = font_size.render(option.languages[option.language][7], 0, Color().RED)

        if option.language == "en":
            new_game_text_place = ((rects[0].center[0])-(rects[0].center[0]*0.17), rects[0].center[1]-15)

            load_game_text_place = ((rects[1].center[0])-(rects[1].center[0]*0.25), rects[1].center[1]-15)

            choosen_language_text_place = ((rects[2].center[0])-(rects[2].center[0]*0.4), rects[2].center[1]-15)

            music_button_text_place = ((rects[3].center[0])-(rects[3].center[0]*0.2), rects[3].center[1]-15)

            quit_game_text_place = ((rects[4].center[0])-(rects[4].center[0]*0.2), rects[4].center[1]-15)
            
        else:
            new_game_text_place = ((rects[0].center[0])-(rects[0].center[0]*0.13), rects[0].center[1]-15)

            load_game_text_place = ((rects[1].center[0])-(rects[1].center[0]*0.25), rects[1].center[1]-15)

            choosen_language_text_place = ((rects[2].center[0])-(rects[2].center[0]*0.35), rects[2].center[1]-15)

            music_button_text_place = ((rects[3].center[0])-(rects[3].center[0]*0.15), rects[3].center[1]-15)

            quit_game_text_place = ((rects[4].center[0])-(rects[4].center[0]*0.27), rects[4].center[1]-15)

        window.blit(new_game_text, new_game_text_place)
        window.blit(load_game_text, load_game_text_place)
        window.blit(choosen_language_text, choosen_language_text_place)
        window.blit(music_button_text, music_button_text_place)
        window.blit(quit_game_text, quit_game_text_place)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                for rect in rects:
                    if rect.collidepoint(float(mouse[0]), float(mouse[1])):
                        if rects.index(rect) == 0:
                            try:
                                loadedSave = await start_new_game(option.language, option.musicIsOn)
                                run = 0
                            except Exception as e:
                                pygame.display.message_box(option.languages[option.language][0], e.__str__())

                        elif rects.index(rect) == 1:
                            try:
                                loadedSave = await load_saved_state(option.language, option.musicIsOn)
                                run = 0
                            except Exception as e:
                                pygame.display.message_box(option.languages[option.language][0], option.languages[option.language][6])
                            

                        elif rects.index(rect) == 2:
                            if option.language == "en":
                                option.language = "hu"
                            else:
                                option.language = "en"
                        elif rects.index(rect) == 3:
                            if option.musicIsOn:
                                option.musicIsOn = False
                            else:
                                option.musicIsOn = True

                        elif rects.index(rect) == len(rects)-1:
                            pygame.quit()
                            sys.exit()

        pygame.display.flip()
    

    return loadedSave