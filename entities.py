class Entities():
    
    def __init__(self, enemy_group, disappearing_blocks, fireball_group, stalactite_group):
        self.enemy_group = enemy_group
        self.disappearing_blocks = disappearing_blocks
        self.fireball_group = fireball_group
        self.stalactite_group = stalactite_group

    # 🔄 RESZPONZIVITÁS KEZELŐ METÓDUS (A FŐ JAVÍTÁS)
    def handle_resize(self, scale_ratio, new_tile_size):
        """
        Átadja az átméretezési információkat az összes tárolt entitás csoportnak.
        Feltételezi, hogy az entitások rendelkeznek 'handle_resize' metódussal.
        """
        
        # Ellenségek átméretezése
        for enemy in self.enemy_group:
            enemy.handle_resize(scale_ratio, new_tile_size)
            
        # Eltűnő blokkok átméretezése
        for block in self.disappearing_blocks:
            block.handle_resize(scale_ratio, new_tile_size)
            
        # Tűzgolyók átméretezése
        for fireball in self.fireball_group:
            # Feltételezzük, hogy a Fireball osztálynak is van handle_resize metódusa.
            fireball.handle_resize(scale_ratio, new_tile_size)
            
        # Jeges cseppkövek (Stalactite) átméretezése
        for stalactite in self.stalactite_group:
            # Feltételezzük, hogy a Stalactite osztálynak is van handle_resize metódusa.
            stalactite.handle_resize(scale_ratio, new_tile_size)

# Megjegyzés:
# A fenti kód feltételezi, hogy a 'disappearing_blocks', 'fireball_group', és 'stalactite_group' 
# is tartalmaz Pygame Sprite-okat vagy olyan objektumokat, amelyek rendelkeznek 
# 'handle_resize(scale_ratio, new_tile_size)' metódussal.