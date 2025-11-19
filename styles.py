import pygame

def set_language():
    """Beolvassa a mentési fájlból a választott nyelvet."""
    try:
        with open("saves.csv", "r") as file:
            sor = file.readline().split(" ")
            # Ellenőrzés, hogy a 3. elem létezik-e (nyelv)
            if len(sor) > 2:
                text = str(sor[2]).strip()
                language = text
                if language == "en" or language == "hu":
                    return language
            return "hu"

    except IndexError:
        return "hu"
    
    except FileNotFoundError:
        print("Nem létezik a fájl!")
        # 💡 Megjegyzés: Ha a fájl nem létezik, valószínűleg egy új játék kezdődik.
        return "hu"

# --- NYELVI KONSTANS ---
languages = {
    "en" : {
        0: "For The Potato!",
        1: "New game",
        2: "Continue game",
        3: "Game language: English",
        4: [ 
            "Music: On",
            "Music: Off"
        ],
        5: "Save and quit game",
        6: "There is no saves!",
        "in game":{
            0: "Level",
            1: "Paused"
        }
    },

    "hu" :{
        0: "A burgonyáért!",
        1: "Új játék",
        2: "Játék folytatása",
        3: "Játék nyelve: Magyar",
        4: [
            "Zene: Be",
            "Zene: Ki"
        ],
        5: "Mentés és kilépés a játékból",
        6: "Nincsenek mentések!",
        "in game":{
            0: "Szint",
            1: "Megállítva"
        }
    }
}

# 📏 Konstansok a fontok skálázásához
class FontConstants:
    ORIGINAL_SIZE30 = 30
    ORIGINAL_SIZE50 = 50
    ORIGINAL_SIZE80 = 80
    ORIGINAL_SIZE100 = 100

# 🖋️ Selected_fonts osztály (RESZPONZÍV JAVÍTÁS)
class Selected_fonts:
    def __init__(self):
        # Kezdeti inicializálás az eredeti méretekkel
        self.font_size30 = pygame.font.Font(None, FontConstants.ORIGINAL_SIZE30)
        self.font_size50 = pygame.font.Font(None, FontConstants.ORIGINAL_SIZE50)
        self.font_size80 = pygame.font.Font(None, FontConstants.ORIGINAL_SIZE80)
        self.font_size100 = pygame.font.Font(None, FontConstants.ORIGINAL_SIZE100)

    # 🔄 RESZPONZIVITÁS KEZELŐ METÓDUS
    def handle_resize(self, scale_ratio):
        """Újraszámolja a fontméreteket a megadott skálázási arány alapján."""
        
        # Fontos: A fontméretet kerekíteni kell (int), hogy elkerüljük a hibákat
        
        # 30-as méret frissítése
        new_size30 = int(FontConstants.ORIGINAL_SIZE30 * scale_ratio)
        self.font_size30 = pygame.font.Font(None, new_size30)
        
        # 50-es méret frissítése
        new_size50 = int(FontConstants.ORIGINAL_SIZE50 * scale_ratio)
        self.font_size50 = pygame.font.Font(None, new_size50)
        
        # 80-as méret frissítése
        new_size80 = int(FontConstants.ORIGINAL_SIZE80 * scale_ratio)
        self.font_size80 = pygame.font.Font(None, new_size80)
        
        # 100-as méret frissítése
        new_size100 = int(FontConstants.ORIGINAL_SIZE100 * scale_ratio)
        self.font_size100 = pygame.font.Font(None, new_size100)

# Color osztály (Nem igényel módosítást)
class Color:
    def __init__(self):
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.WHITE = (255, 255, 255)