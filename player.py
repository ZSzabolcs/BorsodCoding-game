import pygame
import os

class Player():
    # 📐 Konstansok (ezek nem változnak az átméretezéssel)
    ORIGINAL_WIDTH = 40
    ORIGINAL_HEIGHT = 40
    ORIGINAL_JUMP_VELOCITY = -15
    ORIGINAL_GRAVITY = 1
    ORIGINAL_MAX_FALL_VELOCITY = 10
    ORIGINAL_HORIZONTAL_SPEED = 5
    ORIGINAL_SCREEN_WIDTH = 1000 
    ORIGINAL_TILE_SIZE = 50 


    def __init__(self, level, completed, x, y):
        self.img_orig = pygame.image.load(os.path.join("kepek", "trollface.jpg"))
        self.image = pygame.transform.scale(self.img_orig, (Player.ORIGINAL_WIDTH, Player.ORIGINAL_HEIGHT))
        self.rect = self.image.get_rect()
        self.level = level - 1
        
        # EREDETI (ARÁNYOSÍTATLAN) POZÍCIÓK TÁROLÁSA
        self.original_x = x
        self.original_y = y

        self.rect.x = x
        self.rect.y = y
        
        self.vel_y = 0
        self.jump_velocity = Player.ORIGINAL_JUMP_VELOCITY
        self.gravity = Player.ORIGINAL_GRAVITY
        self.max_fall_velocity = Player.ORIGINAL_MAX_FALL_VELOCITY
        self.horizontal_speed = Player.ORIGINAL_HORIZONTAL_SPEED
        
        self.jumped = 0
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        
        # EREDETI CHECKPOINT POZÍCIÓK TÁROLÁSA
        self.original_checkpoint_x = x
        self.original_checkpoint_y = y
        self.checkpoint_x = self.rect.x
        self.checkpoint_y = self.rect.y
        
        self.died = 0
        self.completed = completed
        self.player_place = None


    # 🔄 RESZPONZIVITÁS KEZELŐ METÓDUS
    def handle_resize(self, new_width, new_height, new_tile_size):
        scale_ratio = new_width / Player.ORIGINAL_SCREEN_WIDTH
        
        new_width_scaled = int(Player.ORIGINAL_WIDTH * scale_ratio)
        new_height_scaled = int(Player.ORIGINAL_HEIGHT * scale_ratio)

        self.image = pygame.transform.scale(self.img_orig, (new_width_scaled, new_height_scaled))
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        
        self.jump_velocity = int(Player.ORIGINAL_JUMP_VELOCITY * scale_ratio)
        self.gravity = Player.ORIGINAL_GRAVITY * scale_ratio 
        self.max_fall_velocity = int(Player.ORIGINAL_MAX_FALL_VELOCITY * scale_ratio)
        self.horizontal_speed = int(Player.ORIGINAL_HORIZONTAL_SPEED * scale_ratio)

        tile_scale_ratio = new_tile_size / Player.ORIGINAL_TILE_SIZE
        
        self.rect.x = int(self.original_x * tile_scale_ratio)
        self.rect.y = int(self.original_y * tile_scale_ratio)
        
        self.checkpoint_x = int(self.original_checkpoint_x * tile_scale_ratio)
        self.checkpoint_y = int(self.original_checkpoint_y * tile_scale_ratio)
        
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        
        self.vel_y = int(self.vel_y * scale_ratio)


    def update(self, tile_list, entities, screen : pygame.display):
        dx = 0
        dy = 0
        key = pygame.key.get_pressed()
        
        # --- Mozgás ---
        if key[pygame.K_LEFT]:
            dx -= self.horizontal_speed
        if key[pygame.K_RIGHT]:
            dx += self.horizontal_speed
            
        if key[pygame.K_UP] and self.jumped == 0:
            self.vel_y = self.jump_velocity
            self.jumped = 1

        # --- Gravitáció ---
        self.vel_y += self.gravity
        if self.vel_y > self.max_fall_velocity:
            self.vel_y = self.max_fall_velocity
        dy += self.vel_y

        # --- Ütközésvizsgálat a csempékkel ---
        for tile in tile_list:
            if tile["imageRect"].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                
                if self.vel_y >= 0:
                    if tile["number"] != 4:
                        self.jumped = 0
                
                if self.vel_y < 0:
                    dy = tile["imageRect"].bottom - self.rect.top
                    self.vel_y = 0
                
                elif self.vel_y >= 0:
                    dy = tile["imageRect"].top - self.rect.bottom
                    self.vel_y = 0
                
                if tile["number"] == 4 or tile["number"] == 8:
                    self.died = 1
                if tile["number"] == 3:
                    self.checkpoint_x = tile["imageRect"].x
                    self.checkpoint_y = tile["imageRect"].y
                if tile["number"] == 5:
                    return 1
        
            if tile["imageRect"].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0

        # --- Ütközésvizsgálat az Ellenségekkel (enemies) ---
        for enemy in entities.enemy_group:
            if self.rect.colliderect(enemy.rect):
                if self.rect.bottom <= enemy.rect.top + (self.height * 0.25): # Fejre ugrás
                    # ✅ Ellenőrizze, hogy az enemy a pygame.sprite.Sprite leszármazottja-e!
                    enemy.kill() 
                    self.vel_y = self.jump_velocity * 0.66 
                else: 
                    self.died = 1

        # --- Ütközésvizsgálat Eltűnő Blokkokkal ---
        for block in entities.disappearing_blocks:
            if block.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if block.visible:
                    if self.vel_y >= 0:
                         self.jumped = 0
                         
                    if self.vel_y < 0:
                        dy = block.rect.bottom - self.rect.top
                        self.vel_y = 0
                    
                    elif self.vel_y >= 0:
                        dy = block.rect.top - self.rect.bottom
                        self.vel_y = 0


        # --- Ütközésvizsgálat Tűzgolyókkal ---
        for fireball in entities.fireball_group:
            if self.rect.colliderect(fireball.rect):
                self.died = 1
                
        # --- Képernyő aljának ellenőrzése ---
        if self.rect.top > screen.get_height():
            self.died = 1

        # --- Pozíciófrissítés és respawn ---
        if self.died == 0:
            self.rect.x += dx
            self.rect.y += dy
        
        else:
            self.rect.x = self.checkpoint_x
            self.rect.y = self.checkpoint_y
            self.died = 0
            self.vel_y = 0 

        screen.blit(self.image, self.rect)
        
        return 0