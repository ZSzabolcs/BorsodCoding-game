import pygame
import os
from disappearingBlock import DisappearingBlock
from enemy import Enemy
from fireball import Fireball
from styles import Color
from stalactite import Stalactite
from player import Player
from entities import Entities

class World():
    # 📐 Konstansok az átméretezéshez
    ORIGINAL_TILE_SIZE = 50
    ORIGINAL_WIDTH = 1000
    ORIGINAL_HEIGHT = 1000
    
    tile_size = ORIGINAL_TILE_SIZE # Kezdeti csempeméret (dinamikusan változik)
    in_game_menu_rects = []
    worlds_list = []

    # 🟢 JAVÍTÁS 1: Statikus metódussá tesszük
    @staticmethod
    def set_player_next_level(level, completed, checkpoint_x, checkpoint_y):
        return Player(level, completed, checkpoint_x, checkpoint_y)

    def __init__(self, data : list, level : int, level_name : str):
        self.level = level - 1
        self.level_name = level_name
        self.tile_list = []
        self.world_enemy_group = pygame.sprite.Group()
        self.fireballs_group = pygame.sprite.Group()
        self.stalactite_group = pygame.sprite.Group()
        self.player_place = None
        self.dissaperaingBlocks = []

        # Képek betöltése (Csak az ORIGINÁLIS képeket töltjük be)
        self.dirt_img_orig = pygame.image.load(os.path.join("kepek", "dirt.png")).convert_alpha()
        self.grass_img_orig = pygame.image.load(os.path.join("kepek","grass.png")).convert_alpha()
        self.goal_img_orig = pygame.image.load(os.path.join("kepek", "goal.png")).convert_alpha()
        self.water_img_orig = pygame.image.load(os.path.join("kepek", "water.png")).convert_alpha()
        self.water2_img_orig = pygame.image.load(os.path.join("kepek", "water2.png")).convert_alpha()
        self.goal2_img_orig = pygame.image.load(os.path.join("kepek", "goal2.png")).convert_alpha()
        self.rock_img_orig = pygame.image.load(os.path.join("kepek", "rock.png")).convert_alpha()
        self.lava_img_orig = pygame.image.load(os.path.join("kepek", "lava.png")).convert_alpha()
        self.snow_img_orig = pygame.image.load(os.path.join("kepek", "snow.png")).convert_alpha()
        self.snow2_img_orig = pygame.image.load(os.path.join("kepek", "snow2.png")).convert_alpha()
        self.ice_img_orig = pygame.image.load(os.path.join("kepek", "ice.png")).convert_alpha()


        def make_just_disappearing_block(image_orig, col_count, row_count, seconds):
            # Csempe méretezése a World.tile_size alapján
            img = pygame.transform.scale(image_orig, (World.tile_size, World.tile_size))
            img_rect = img.get_rect()
            img_rect.x = col_count * World.tile_size
            img_rect.y = row_count * World.tile_size
            
            # 🟢 JAVÍTÁS 2: A FÖLÖSLEGES 5. ARGUMENTUM ELHAGYÁSA!
            # A DisappearingBlock __init__ metódusa 4 argumentumot vár (x, y, image, second).
            block = DisappearingBlock(img_rect.x, img_rect.y, img, seconds) 
            
            # Mivel a DisappearingBlock.py-t már javítottuk, hogy a konstruktorban 
            # az image.copy()-t használja az img_orig helyett, ez így már működik.
            
            # Az eredeti pozíciók beállítása a reszponzivitáshoz
            block.original_x = col_count * World.ORIGINAL_TILE_SIZE
            block.original_y = row_count * World.ORIGINAL_TILE_SIZE
            
            self.dissaperaingBlocks.append(block)


        def make_just_tile(image_orig, col_count, row_count, typeofnumber):
            # Csempe méretezése a World.tile_size alapján
            img = pygame.transform.scale(image_orig, (World.tile_size, World.tile_size))
            img_rect = img.get_rect()
            img_rect.x = col_count * World.tile_size
            img_rect.y = row_count * World.tile_size
            tile = {
                "image" : img,
                "imageRect" : img_rect, 
                "number" : typeofnumber,
                "image_orig": image_orig, # Eredeti kép tárolása
                "col": col_count, # Oszlop és sor tárolása az átméretezéshez
                "row": row_count
            }
            self.tile_list.append(tile)

        # make_tile elhagyható, mivel make_just_tile is létezik, de megtartjuk, ha használatban van máshol
        def make_tile(image_orig, col_count, row_count, typeofnumber):
             # Csempe méretezése a World.tile_size alapján
            img = pygame.transform.scale(image_orig, (World.tile_size, World.tile_size))
            img_rect = img.get_rect()
            img_rect.x = col_count * World.tile_size
            img_rect.y = row_count * World.tile_size
            tile = {
                "image" : img,
                "imageRect" : img_rect, 
                "number" : typeofnumber,
                "image_orig": image_orig, # Eredeti kép tárolása
                "col": col_count, # Oszlop és sor tárolása az átméretezéshez
                "row": row_count
            }
            return tile
        
        # --- Világépítés a World.tile_size alapértelmezett értékével (50) ---
        DEADLY = 4
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    make_just_tile(self.dirt_img_orig, col_count, row_count, 1)
                    
                if tile == 2:
                    make_just_tile(self.grass_img_orig, col_count, row_count, 2)
                    
                if tile == 3:
                    make_just_tile(self.goal_img_orig, col_count, row_count, 3)

                if tile == DEADLY:
                    make_just_tile(self.water_img_orig, col_count, row_count, DEADLY)

                if tile == 5:
                    make_just_tile(self.goal2_img_orig, col_count, row_count, 5)

                if tile == 6:
                    # Enemy létrehozása a World.tile_size arányában
                    enemy = Enemy(col_count * World.tile_size, row_count * World.tile_size + 15, self.level)
                    self.world_enemy_group.add(enemy)
                
                if tile == 7:
                    make_just_tile(self.rock_img_orig, col_count, row_count, 7)
                
                if tile == 8:
                    make_just_tile(self.lava_img_orig, col_count, row_count, DEADLY)

                if tile == 9:
                    make_just_tile(self.snow2_img_orig, col_count, row_count, 9)
                
                if tile == 10:
                    make_just_tile(self.snow_img_orig, col_count, row_count, 10)

                if tile == 11:
                    make_just_tile(self.water2_img_orig, col_count, row_count, DEADLY)

                if tile == 12:
                    make_just_tile(self.ice_img_orig, col_count, row_count, 12)

                # 🟢 JAVÍTÁS 2: Eltűnő blokk hívások
                if tile == "b1":
                    make_just_disappearing_block(self.rock_img_orig, col_count, row_count, 2)

                if tile == "b2":
                    make_just_disappearing_block(self.grass_img_orig, col_count, row_count, 3)

                if tile == "b3":
                    make_just_disappearing_block(self.snow_img_orig, col_count, row_count, 2)

                if tile == "b4":
                    make_just_disappearing_block(self.snow_img_orig, col_count, row_count, 2)

                if tile == "p":
                    # Player létrehozása (a Player osztály kezeli a reszponzivitást a konstruktorban)
                    self.player_place = Player(level, 0, col_count * World.tile_size, row_count * World.tile_size)

                if tile == "fb":
                    fireball = Fireball(col_count * World.tile_size, row_count * World.tile_size)
                    tile_data = make_tile(self.lava_img_orig, col_count, row_count, DEADLY)
                    self.fireballs_group.add(fireball)
                    self.tile_list.append(tile_data)
                
                if tile == "st":
                    tile_data = make_tile(self.rock_img_orig, col_count, row_count, 7)
                    stalactite = Stalactite(col_count * World.tile_size, row_count * World.tile_size, tile_data)
                    self.stalactite_group.add(stalactite)
                    self.tile_list.append(tile_data)

                col_count += 1
            row_count += 1

        self.entities = Entities(enemy_group=self.world_enemy_group, 
                                 disappearing_blocks=self.dissaperaingBlocks, 
                                 fireball_group=self.fireballs_group, 
                                 stalactite_group=self.stalactite_group)

    # 🔄 RESZPONZIVITÁS KEZELŐ METÓDUS
    def handle_resize(self, new_width, new_height):
        
        # 1. Új csempeméret számítása és arány meghatározása
        scale_ratio = new_width / World.ORIGINAL_WIDTH
        World.tile_size = int(World.ORIGINAL_TILE_SIZE * scale_ratio)
        
        # 2. Csempék (tile_list) frissítése
        for tile in self.tile_list:
            # Új kép méretezése
            tile["image"] = pygame.transform.scale(tile["image_orig"], (World.tile_size, World.tile_size))
            
            # Új pozíció és méret
            tile["imageRect"] = tile["image"].get_rect()
            tile["imageRect"].x = tile["col"] * World.tile_size
            tile["imageRect"].y = tile["row"] * World.tile_size
            
            # A tile_data szótár frissítése a stalactite triggerhez
            if tile["number"] == 7: # Rock csempe (Stalactite csempe)
                for st in self.stalactite_group:
                    # Frissítenünk kell a Stalactite tile_data-ját is, ha az a triggerhez kell
                    # Jelenleg a Stalactite csak a saját rect-jét és a csempe rect-jét használja
                    # A Stalactite.py-ban a tile_data['imageRect']-et használja, amit itt frissítettünk.
                    pass

        # 3. Speciális elemek (blokkok, ellenségek, játékos) frissítése
        
        # Játékos átméretezése
        if self.player_place:
            self.player_place.handle_resize(new_width, new_height, World.tile_size)

        # Ellenségek és egyéb entitások átméretezése (a többi már javítva lett)
        self.entities.handle_resize(scale_ratio, World.tile_size)


    def draw(self, pause, run, lang, ch_lang, fonts, screen, mouse = None):
        current_width, current_height = screen.get_size()
        
        # 🎨 Csempék kirajzolása (mindig először)
        for tile in self.tile_list:
            screen.blit(tile["image"], tile["imageRect"])

        def draw_left_top_texts():
            # A pozíció arányosítása (pl. 10 pixel az eredeti 1000-ből = 0.01 arány)
            x_pos = current_width * 0.01 
            y_pos = current_height * 0.01 

            if self.level < 5:
                chosen_color = Color().BLACK
            else:
                chosen_color = Color().WHITE

            # Feltételezzük, hogy a fonts.font_size50 is dinamikusan generálódik
            level_text = fonts.font_size50.render(lang[ch_lang]['in game'][0] + " " + str(self.level + 1) + ": " + self.level_name, 0, chosen_color)
            screen.blit(level_text, (x_pos, y_pos))


        draw_left_top_texts() 

        if pause and not run:
            # 🖼️ PAUSE/MENU kirajzolása (Arányosan)
            
            # A menü szövegének elhelyezése a gomb közepéhez képest
            if World.in_game_menu_rects:
                menu_rect = World.in_game_menu_rects[0]
                
                # Kiszámoljuk a szöveg elhelyezését a rect pozíciójához és méretéhez képest
                offset_y = menu_rect.height * 0.15 
                
                # Arányos eltolás az X-tengelyen a szöveg hosszához (ez a fix 1000-hez képest jó)
                if ch_lang == "en":
                    offset_x = menu_rect.width * 0.30
                else:
                    offset_x = menu_rect.width * 0.45

                quit_game_text_place = (menu_rect.centerx - offset_x, menu_rect.centery - offset_y)
                
                for rect in World.in_game_menu_rects:
                    square = pygame.draw.rect(screen, Color().BLACK, rect)
                    
                    if mouse is not None:
                        # 💡 JAVÍTÁS: Egész számú koordináták használata a collidepoint-hoz
                        if square.collidepoint(int(mouse[0]), int(mouse[1])):
                            square = pygame.draw.rect(screen, Color().BLUE, rect)
                    
                quit_game_text = fonts.font_size50.render(lang[ch_lang][5], 0, Color().RED)
                screen.blit(quit_game_text, quit_game_text_place)
            
            pygame.display.update()

            
    def draw_broken_blocks(self, screen):
        # Eltűnő blokkok frissítése és kirajzolása (update és draw a DisappearingBlock.py-ból)
        for bloc in self.dissaperaingBlocks:
            bloc.update()
            bloc.draw(screen)

    def get_player(self):
        return self.player_place