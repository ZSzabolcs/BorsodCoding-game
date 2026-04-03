import pygame

def set_language():
	try:
		with open("saves.csv", "r") as file:
			sor = file.readline().split(" ")
			language = str(sor[2])
			if language == "en" or language == "hu":
				return language
			return "hu"

	except IndexError:
		pygame.display.message_box("Hiba", "Nem található a nyelv!")
		return "hu"
	
	except FileNotFoundError:
		pygame.display.message_box("Hiba", "Nem létezik a fájl!", "error")
		return "hu"

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
		7: "Quit game",
		"in game":{
			0: "Level",
			1: "Paused",
			2: "Point"
		},
		8: "Error occured connecting to server to save your data!",
		9: "Sucessfully saved locally!"
	},

	"hu" :{
		0: "A burgonyáért!",
		1: "Új játék",
		2: "Játék folytatása",
		3: "Játék nyelve: Magyar",
		4: [
			"Zene: Van",
	  		"Zene: Nincs"
		],
		5: "Mentés és kilépés a játékból",
		6: "Nincsenek mentések!",
		7: "Kilépés a játékból",
		"in game":{
			0: "Szint",
			1: "Megállítva",
			2: "Pont"
		},
		8: "Hiba történt a szerverhez való kapcsolódáskor az adatok mentéséhez!",
		9: "Sikeresen mentve lokálisan!"
	}
}

class Selected_fonts:
	def __init__(self):
		self.font_size30 = pygame.font.Font(None, 30)
		self.font_size40 = pygame.font.Font(None, 40)
		self.font_size50 = pygame.font.Font(None, 50)
		self.font_size80 = pygame.font.Font(None, 80)
		
class Color:
	def __init__(self):
		self.BLACK = (0, 0, 0)
		self.RED = (255, 0, 0)
		self.GREEN = (0, 255, 0)
		self.BLUE = (0, 0, 255)
		self.WHITE = (255, 255, 255)