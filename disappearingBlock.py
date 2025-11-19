import pygame
import time
# Nem kell az 'os', ha a kép már be van töltve

class DisappearingBlock(pygame.sprite.Sprite):
    # 📐 Konstansok
    ORIGINAL_TILE_SIZE = 50 # Feltételezett eredeti csempe méret

    # Az init most is 4 pozicionális argumentumot vár (self-en kívül), hogy illeszkedjen a hívó kódhoz
    def __init__(self, x, y, image, second):
        pygame.sprite.Sprite.__init__(self)
        
        # 🟢 JAVÍTÁS 1: Eredeti kép (másolata) tárolása
        # Az image paraméter egy pygame.Surface objektum kell legyen.
        # Tároljuk el az eredeti állapotot, hogy átméretezéskor ebből induljunk ki.
        self.img_orig = image.copy() 
        
        self.image = image
        self.rect = self.image.get_rect()
        
        # 🟢 JAVÍTÁS 2: Eredeti (arányosítatlan) pozíciók tárolása
        self.original_x = x
        self.original_y = y
        
        self.rect.x = x
        self.rect.y = y
        
        self.visible = 1
        self.last_toggle_time = time.time()
        self.sec = second

    # 🔄 RESZPONZIVITÁS KEZELŐ METÓDUS
    def handle_resize(self, scale_ratio, new_tile_size):
        """
        Frissíti a blokk méretét és pozícióját az átméretezéskor.
        """
        
        # 1. Pozíciók frissítése az eredeti adatok alapján
        tile_scale_ratio = new_tile_size / DisappearingBlock.ORIGINAL_TILE_SIZE

        self.rect.x = int(self.original_x * tile_scale_ratio)
        self.rect.y = int(self.original_y * tile_scale_ratio)
        
        # 2. Sprite átméretezése az új csempe méretre
        new_width_scaled = new_tile_size
        new_height_scaled = new_tile_size

        self.image = pygame.transform.scale(self.img_orig, (new_width_scaled, new_height_scaled))
        
        # A Rect objektumot újra kell szinkronizálni az új mérettel/pozícióval
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))


    def update(self):
        # Az időzítés másodperceken alapul, így nem igényel skálázást
        current_time = time.time()
        if current_time - self.last_toggle_time > self.sec:
            self.visible = not self.visible
            self.last_toggle_time = current_time

    def draw(self, surface):
        if self.visible:
            surface.blit(self.image, self.rect)