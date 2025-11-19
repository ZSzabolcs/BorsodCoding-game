import pygame
import os

class Fireball(pygame.sprite.Sprite):
    # 📐 Konstansok (ezek nem változnak az átméretezéssel)
    ORIGINAL_WIDTH = 25
    ORIGINAL_HEIGHT = 25
    ORIGINAL_OFFSET_X = 15 # Az eredeti +15 pixel eltolás X-ben a csempéhez képest
    ORIGINAL_VERTICAL_VELOCITY = -4
    ORIGINAL_MAX_DISTANCE = 200 # Az eredeti 200 pixel maximális távolság

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        
        # Eredeti kép betöltése és tárolása
        self.img_orig = pygame.image.load(os.path.join("kepek", "tuzgolyo.png")).convert_alpha()
        
        # Kezdeti méretezés
        self.image = pygame.transform.scale(self.img_orig, (Fireball.ORIGINAL_WIDTH, Fireball.ORIGINAL_HEIGHT))
        self.rect = self.image.get_rect()
        
        # Eredeti (arányosítatlan) pozíciók tárolása (valószínűleg csempe alapú)
        self.original_x = x
        self.original_y = y
        
        # Kezdeti dinamikus pozíciók
        self.rect.x = x + Fireball.ORIGINAL_OFFSET_X
        self.rect.y = y
        self.initial_y = y # Ez a visszatérési pont
        
        # Dinamikus mozgási értékek
        self.vertical_velocity = Fireball.ORIGINAL_VERTICAL_VELOCITY
        self.max_distance = Fireball.ORIGINAL_MAX_DISTANCE

    # 🔄 RESZPONZIVITÁS KEZELŐ METÓDUS (A FŐ JAVÍTÁS)
    def handle_resize(self, scale_ratio, new_tile_size):
        """
        Frissíti a méretet, sebességet és a pozíciókat az átméretezéskor.
        """
        
        # 1. Sprite átméretezése
        new_width_scaled = int(Fireball.ORIGINAL_WIDTH * scale_ratio)
        new_height_scaled = int(Fireball.ORIGINAL_HEIGHT * scale_ratio)

        self.image = pygame.transform.scale(self.img_orig, (new_width_scaled, new_height_scaled))
        
        # 2. Fizikai értékek arányosítása
        self.vertical_velocity = Fireball.ORIGINAL_VERTICAL_VELOCITY * scale_ratio
        self.max_distance = Fireball.ORIGINAL_MAX_DISTANCE * scale_ratio
        
        # 3. Pozíciók frissítése az eredeti adatok alapján
        tile_scale_ratio = new_tile_size / 50.0 # Feltételezzük, hogy 50 volt az ORIGINAL_TILE_SIZE
        
        # Az X eltolás is arányosítva van
        scaled_offset_x = Fireball.ORIGINAL_OFFSET_X * tile_scale_ratio
        
        # Frissítjük a kezdeti és az aktuális pozíciókat is, a duplázódás elkerülésére
        self.rect.x = int(self.original_x * tile_scale_ratio + scaled_offset_x)
        self.rect.y = int(self.original_y * tile_scale_ratio)
        self.initial_y = self.rect.y # A visszatérési pont frissítése

        # A Rect objektumot újra kell szinkronizálni az új mérettel/pozícióval
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        
        # Frissítjük a függőleges sebességet is, hogy az arányos mozgás folytatódjon
        # (A self.vertical_velocity már frissítve lett a scale_ratio-val a 2. pontban)


    def update(self):
        # Az update metódus most a dinamikusan skálázott értékeket használja
        
        self.rect.y += self.vertical_velocity
        distance_revealed = abs(self.initial_y - self.rect.y) # A távolság a kezdőponttól
        
        # --- Mozgás Logika ---

        if self.vertical_velocity < 0:
            # Felfelé haladás: Elérte-e a maximális távolságot?
            if distance_revealed >= self.max_distance:
                self.vertical_velocity *= -1
                
        elif self.vertical_velocity > 0:
            # Lefelé haladás: Visszaért-e a kezdőpontra?
            if self.rect.y >= self.initial_y:
                self.vertical_velocity = self.vertical_velocity / abs(self.vertical_velocity) * Fireball.ORIGINAL_VERTICAL_VELOCITY # Visszaállítjuk az eredeti, de skálázott sebességet a kezdőirányba
                self.rect.y = self.initial_y # Fixáljuk a pozíciót a kezdőponton