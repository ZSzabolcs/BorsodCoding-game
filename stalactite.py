import pygame
import os

class Stalactite(pygame.sprite.Sprite):
    # 📐 Konstansok (ezek nem változnak az átméretezéssel)
    ORIGINAL_WIDTH = 25
    ORIGINAL_HEIGHT = 25
    ORIGINAL_OFFSET_X = 15 # A cseppkő X eltolása a csempe közepétől
    ORIGINAL_OFFSET_Y = 30 # A cseppkő Y eltolása a csempe aljától
    ORIGINAL_VERTICAL_VELOCITY = 7
    ORIGINAL_TRIGGER_DISTANCE = 250 # A leesést kiváltó eredeti 250 pixeles távolság
    ORIGINAL_TILE_SIZE = 50 # Feltételezett eredeti csempe méret

    def __init__(self, x, y, tile):
        pygame.sprite.Sprite.__init__(self)
        
        # Eredeti kép betöltése és tárolása
        self.img_orig = pygame.image.load(os.path.join("kepek", "tuzgolyo.png")).convert_alpha()
        
        # Kezdeti méretezés
        self.image = pygame.transform.scale(self.img_orig, (Stalactite.ORIGINAL_WIDTH, Stalactite.ORIGINAL_HEIGHT))
        self.rect = self.image.get_rect()
        
        # Eredeti (arányosítatlan) pozíciók tárolása (valószínűleg csempe alapú)
        self.original_x = x
        self.original_y = y
        
        # Kezdeti dinamikus pozíciók
        self.rect.x = x + Stalactite.ORIGINAL_OFFSET_X
        self.rect.y = y + Stalactite.ORIGINAL_OFFSET_Y
        
        self.fall = 0
        self.vertical_velocity = Stalactite.ORIGINAL_VERTICAL_VELOCITY
        self.trigger_distance = Stalactite.ORIGINAL_TRIGGER_DISTANCE
        
        # ⚠️ Fontos: A starting_tile-t nem elég átvenni, mert az is egy Rect objektum.
        # Tároljuk az eredeti pozícióját/méretét a későbbi arányosításhoz!
        self.starting_tile_rect = tile["imageRect"] 
        

    # 🔄 RESZPONZIVITÁS KEZELŐ METÓDUS (A FŐ JAVÍTÁS)
    def handle_resize(self, scale_ratio, new_tile_size):
        """
        Frissíti a méretet, sebességet és a pozíciókat az átméretezéskor.
        """
        
        # 1. Sprite átméretezése
        new_width_scaled = int(Stalactite.ORIGINAL_WIDTH * scale_ratio)
        new_height_scaled = int(Stalactite.ORIGINAL_HEIGHT * scale_ratio)

        self.image = pygame.transform.scale(self.img_orig, (new_width_scaled, new_height_scaled))
        
        # 2. Fizikai értékek arányosítása
        self.vertical_velocity = Stalactite.ORIGINAL_VERTICAL_VELOCITY * scale_ratio
        self.trigger_distance = Stalactite.ORIGINAL_TRIGGER_DISTANCE * scale_ratio
        
        # 3. Pozíciók frissítése az eredeti adatok alapján
        tile_scale_ratio = new_tile_size / Stalactite.ORIGINAL_TILE_SIZE
        
        # Az X és Y eltolások is arányosítva vannak
        scaled_offset_x = Stalactite.ORIGINAL_OFFSET_X * tile_scale_ratio
        scaled_offset_y = Stalactite.ORIGINAL_OFFSET_Y * tile_scale_ratio
        
        # Frissítjük az aktuális pozíciót az eredeti alapján
        self.rect.x = int(self.original_x * tile_scale_ratio + scaled_offset_x)
        self.rect.y = int(self.original_y * tile_scale_ratio + scaled_offset_y)

        # A Rect objektumot újra kell szinkronizálni az új mérettel/pozícióval
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        
        # 4. Starting tile Rect frissítése (ha szükséges, bár a tile_list-tel frissülne)
        # Itt csak a referenciát frissítjük a méretezett csempére, ha a World osztály frissíti a tile_listet.
        # Mivel a starting_tile az update-ben csak ütközésvizsgálatra kell, feltételezzük, hogy
        # a 'tile_list' tartalmazza a már méretezett csempéket.


    def update(self, player, tile_list : list):
        # Az update most a dinamikusan skálázott értékeket használja (self.trigger_distance, self.vertical_velocity)
        
        # 1. Leesés trigger (a távolság dinamikus)
        # Csak akkor kezd el esni, ha a játékos elég közel van (és valamennyire alatt is)
        if player.rect.y - self.trigger_distance <= self.rect.y and player.rect.x + (player.width / 2) >= self.rect.x:
            self.fall = 1

        if self.fall:
            # Leesés a skálázott sebességgel
            self.rect.y += self.vertical_velocity
            
            # 2. Ütközésvizsgálat csempékkel (megsemmisülés)
            for tile in tile_list:
                # Ütközés, ÉS NEM a saját kiinduló csempéjével ütközik (így elkerüljük az azonnali kill-t)
                if self.rect.colliderect(tile["imageRect"]) and not self.rect.colliderect(self.starting_tile_rect):
                    self.kill()

        # 3. Ütközésvizsgálat a játékossal (halál)
        if self.rect.colliderect(player.rect):
            player.died = 1