import pygame
import os

class Enemy(pygame.sprite.Sprite):
    # 📐 Konstansok (ezek nem változnak az átméretezéssel)
    ORIGINAL_WIDTH = 40
    ORIGINAL_HEIGHT = 40
    ORIGINAL_SPEED = 1
    ORIGINAL_SCREEN_WIDTH = 1000 # Eredeti ablak szélessége (referencia)
    ORIGINAL_TILE_SIZE = 50 # Új konstans a csempe alapméretéhez
    
    def __init__(self, x, y, level):
        pygame.sprite.Sprite.__init__(self)
        
        # Eredeti kép betöltése és tárolása (hogy átméretezhessük)
        self.img_orig = pygame.image.load(os.path.join("kepek", "enemy.png")).convert()
        
        # Kezdeti méretezés
        self.image = pygame.transform.scale(self.img_orig, (Enemy.ORIGINAL_WIDTH, Enemy.ORIGINAL_HEIGHT))
        self.rect = self.image.get_rect()
        
        # Pozíciók (Eredeti arányosítatlan pozíciók tárolása)
        self.rect.x = x
        self.rect.y = y
        self.original_x = x
        self.original_y = y
        
        # Dinamikus mozgási értékek
        self.move_direction = 1
        self.speed = Enemy.ORIGINAL_SPEED # Kezdeti sebesség
        self.level = level

    # 🔄 RESZPONZIVITÁS KEZELŐ METÓDUS
    def handle_resize(self, scale_ratio, new_tile_size):
        
        # 1. Sprite átméretezése
        new_width_scaled = int(Enemy.ORIGINAL_WIDTH * scale_ratio)
        new_height_scaled = int(Enemy.ORIGINAL_HEIGHT * scale_ratio)

        self.image = pygame.transform.scale(self.img_orig, (new_width_scaled, new_height_scaled))
        
        # 2. Sebesség arányosítása
        self.speed = Enemy.ORIGINAL_SPEED * scale_ratio
        
        # 3. Pozíciók frissítése az eredeti adatok alapján
        tile_scale_ratio = new_tile_size / Enemy.ORIGINAL_TILE_SIZE

        # Frissítjük az aktuális pozíciót az eredeti alapján
        self.rect.x = int(self.original_x * tile_scale_ratio)
        self.rect.y = int(self.original_y * tile_scale_ratio)
        
        # A Rect objektumot újra kell szinkronizálni az új mérettel/pozícióval
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        

    def update(self, tile_list):
        
        # A következő pozíció számítása (használva a dinamikus sebességet)
        next_x = self.rect.x + self.move_direction * self.speed
        # Az "1" pixel eltolás arányosítása a sebességgel
        next_bottom = self.rect.bottom + int(1 * self.speed) 
        ground_beneath_next = 0
        
        # LÉPÉS
        self.rect.x += self.move_direction * self.speed

        for tile in tile_list:
            # 1. Falba ütközés jobbra
            if tile["imageRect"].collidepoint(self.rect.right, self.rect.midright[1]) and tile["number"] > 0:
                self.move_direction *= -1
            
            # 2. Falba ütközés balra
            if tile["imageRect"].collidepoint(self.rect.left, self.rect.midleft[1]) and tile["number"] > 0:
                self.move_direction *= -1
            
            # 3. Talaj ellenőrzése a következő lépésnél
            check_x = next_x + self.rect.width // 2 
            
            # Ellenőrizzük, hogy van-e csempe a check_x pozíciónál next_bottom magasságban
            if tile["imageRect"].colliderect(check_x, next_bottom, 1, 1):
                ground_beneath_next = 1

        # Ha a következő lépésnél nincs talaj, irányváltás
        if not ground_beneath_next:
            self.move_direction *= -1