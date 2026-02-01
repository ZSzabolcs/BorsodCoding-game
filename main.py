import pygame
from pygame.locals import *
import os
import sys
import worlds
import asyncio
import json
import requests
from login import loginWindow
from menu import menu_page
from menu import Data
from styles import set_language
from styles import languages
from styles import Selected_fonts
from world import World
from setting_window_screen_size import setting_size
from menu import Option

def lokalis_mentes():
	with open("saves.csv", "w") as file:
		file.write(f"{str(data.points)} {str(data.level)} {data.language}")
		file.close()

async def saving_game(data : Data, name, token):
	try:
		if name == "teszt":
			lokalis_mentes()
		else:
			url = "https://localhost:7036/api/Save"

			payload = json.dumps({
				"name": name,
				"points": data.points,
				"level": data.level,
				"language": data.language
			})

			headers = {
			'Content-Type': 'application/json',
			"Authorization" : f"Bearer {token}"
			}

			response = requests.request("POST", url, headers=headers, data=payload, verify=False)

			print(response.status_code)
			body = response.json()
			print(body["message"])

			
			if(response.status_code == 200):
				response = requests.request("PUT", url, headers=headers, data=payload, verify=False)
				print(response.status_code)
				body = response.json()
				print(body["message"])

			pygame.display.message_box(languages[data.language][0], body["message"])
		

	except requests.exceptions.ConnectionError as e:
		pygame.display.message_box(languages[data.language][0], f"Nem sikerült kapcsolatba lépni a szerverrel adatai mentéséhez!", "error")
	finally:
		lokalis_mentes()
		pygame.display.message_box(languages[data.language][0], "Sikeres mentés lokálisan!", "info")

username = ""
username = "teszt"
if username != "teszt":
	login = loginWindow()
	if login.successfull:
		NAME = login.name
		TOKEN = login.token
		pygame.init()
else:
	NAME = "teszt"
	pygame.init()

screen = None
screen_index = setting_size()

if screen_index == "1":
	screen = pygame.display.set_mode((760, 760))
	World.tile_height = 38
	World.tile_width = 38
elif screen_index == "2":
	screen = pygame.display.set_mode((1000, 1000))
	World.tile_height = 50
	World.tile_width = 50


fonts = Selected_fonts()

screen_width = screen.get_width()
screen_height = screen.get_height()

choosen_language = set_language()

option = Option(screen, choosen_language, languages, fonts)

data = menu_page(option)


if data.musicIsOn:
	background_music = pygame.mixer.Sound("Jazz In Paris  Media Right Productions (No Copyright Music).mp3")
	background_music.set_volume(0.6)
	background_music.play(-1)


pygame.display.set_caption(languages[choosen_language][0])
bg_img = pygame.image.load(os.path.join("kepek", "hatter.png")).convert()
bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height))
bg2_img = pygame.image.load(os.path.join("kepek", "hatter2.png")).convert()
bg2_img = pygame.transform.scale(bg2_img, (screen_width, screen_height))
bg3_img = pygame.image.load(os.path.join("kepek", "hatter3.png")).convert()
bg3_img = pygame.transform.scale(bg3_img, (screen_width, screen_height))
bg4_img = pygame.image.load(os.path.join("kepek", "hatter4.png")).convert()
bg4_img = pygame.transform.scale(bg4_img, (screen_width, screen_height))

level_text = languages[choosen_language]["in game"][0]
point_text = languages[choosen_language]["in game"][2]

world = World(worlds.world_data, 1, f"{level_text}: 1 {point_text}: ", screen)
world2 = World(worlds.world2_data, 2, f"{level_text}: 2 {point_text}: ", screen)
world3 = World(worlds.world3_data, 3, f"{level_text}: 3 {point_text}: ", screen)
world4 = World(worlds.world4_data, 4, f"{level_text}: 4 {point_text}: ", screen)
world5 = World(worlds.world5_data, 5, f"{level_text}: 5 {point_text}: ", screen)
world6 = World(worlds.world6_data, 6, f"{level_text}: 6 {point_text}: ", screen)
world7 = World(worlds.world7_data, 7, f"{level_text}: 7 {point_text}: ", screen)
world8 = World(worlds.world8_data, 8, f"{level_text}: 8 {point_text}: ", screen)
world9 = World(worlds.world9_data, 9, f"{level_text}: 9 {point_text}: ", screen)
world10 = World(worlds.world10_data, 10, f"{level_text}: 10 {point_text}: ", screen)
World.worlds_list = [world, world2, world3, world4, world5, world6, world7, world8, world9, world10]

World.in_game_menu_rects = [
	pygame.rect.Rect(screen_width*0.27, screen_height/2-50, screen_width*0.5, screen_width*0.1)
]



async def main(data : Data):
	run = 1
	clock = pygame.time.Clock()
	FPS = 60
	pause = 0
	sum_points = 0
	while run and not pause:
		current_world = World.worlds_list[data.level - 1]
		clock.tick(FPS)
		if data.level < 4:
			screen.blit(bg_img, (0, 0))
		elif data.level >= 4 and data.level <= 5:
			screen.blit(bg2_img, (0, 0))
		elif data.level >= 6 and data.level <= 8:
			screen.blit(bg3_img, (0, 0))
		elif data.level >= 9:
			screen.blit(bg4_img, (0, 0))

		current_world.draw(
				pause,
				run,
				languages,
				choosen_language,
				fonts,
				screen,
				sum_points,
			    mouse=None
		)
		current_world.draw_broken_blocks(screen)
		player = current_world.get_player()
		current_world.not_player_objects(screen, player)
		player_state = player.update(current_world.tile_list, current_world.entities, screen)

		if player_state.died:
			sum_points = await current_world.reload_when_player_died(sum_points)

		if player_state.completed:
			data.level += 1
			player_state.completed = 0
			player = World.set_player_next_level(data.level, player_state.completed, player.checkpoint_x, player.checkpoint_y, screen)
			data.points = sum_points

		if player_state.killed:
			sum_points += 100
			

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = 0

			elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				pause = 1
				run = 0



		while not run and pause:
			mouse = pygame.mouse.get_pos()
			current_world.draw(pause, run, languages, fonts=fonts, ch_lang=choosen_language, screen=screen, points = sum_points, mouse=mouse)

			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
					pause = 0
					run = 1
				elif event.type == pygame.QUIT:
					pause = 0
					run = 0
				elif event.type == pygame.MOUSEBUTTONDOWN:
					for rect in World.in_game_menu_rects:
						if rect.collidepoint(float(mouse[0]), float(mouse[1])):
							if World.in_game_menu_rects.index(rect) == 0:
								pause, run = 0, 0



		pygame.display.flip()
		await asyncio.sleep(0)

	if not run and not pause:
		await saving_game(data, NAME, TOKEN)
		pygame.quit()
		sys.exit()

asyncio.run(main(data))
