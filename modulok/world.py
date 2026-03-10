import pygame
import os
from .disappearingBlock import DisappearingBlock
from .enemy import Enemy
from .fireball import Fireball
from .styles import Color
from .stalactite import Stalactite
from .player import Player
from .entities import Entities

class World():
	tile_width = 0
	tile_height = 0
	in_game_menu_rects = []
	worlds_list = []


	def __init__(self, data : list, level : int, level_name : str, screen):
		self.level = level - 1
		self.level_name = level_name
		self.points = 0
		self.tile_list = []
		self.enemy_places = []
		self.world_enemy_group = pygame.sprite.Group()
		self.fireballs_group = pygame.sprite.Group()
		self.stalactite_places = []
		self.stalactite_group = pygame.sprite.Group()
		self.player_place = None
		self.dissaperaingBlocks = []

		

		dirt_img = pygame.image.load(os.path.join("kepek", "dirt.png"))
		grass_img = pygame.image.load(os.path.join("kepek","grass.png"))
		goal_img = pygame.image.load(os.path.join("kepek", "goal.png"))
		water_img = pygame.image.load(os.path.join("kepek", "water.png"))
		water2_img = pygame.image.load(os.path.join("kepek", "water2.png"))
		goal2_img = pygame.image.load(os.path.join("kepek", "goal2.png"))
		rock_img = pygame.image.load(os.path.join("kepek", "rock.png"))
		lava_img = pygame.image.load(os.path.join("kepek", "lava.png"))
		snow_img = pygame.image.load(os.path.join("kepek", "snow.png"))
		snow2_img = pygame.image.load(os.path.join("kepek", "snow2.png"))
		ice_img = pygame.image.load(os.path.join("kepek", "ice.png"))


		def make_just_disappearing_block(image, col_count, row_count, seconds):
			img = pygame.transform.scale(image, (World.tile_width, World.tile_height))
			img_rect = img.get_rect()
			img_rect.x = col_count * World.tile_width
			img_rect.y = row_count * World.tile_width
			block = DisappearingBlock(img_rect.x, img_rect.y, img, seconds)
			self.dissaperaingBlocks.append(block)


		def make_just_tile(image, tile_size, col_count, row_count, typeofnumber):
			img = pygame.transform.scale(image, (World.tile_width, World.tile_height))
			img_rect = img.get_rect()
			img_rect.x = col_count * World.tile_width
			img_rect.y = row_count * World.tile_height
			tile = {
				"image" : img,
				"imageRect" : img_rect, 
				"number" : typeofnumber
			}
			self.tile_list.append(tile)


		def make_tile(image, col_count, row_count, typeofnumber):
			img = pygame.transform.scale(image, (World.tile_width, World.tile_height))
			img_rect = img.get_rect()
			img_rect.x = col_count * World.tile_width
			img_rect.y = row_count * World.tile_height
			tile = {
				"image" : img,
				"imageRect" : img_rect, 
				"number" : typeofnumber
			}
			return tile
		

		DEADLY = 4
		row_count = 0
		for row in data:
			col_count = 0
			for tile in row:
				if tile == 1:
					make_just_tile(dirt_img, World.tile_width, col_count, row_count, 1)
					
				if tile == 2:
					make_just_tile(grass_img, World.tile_width, col_count, row_count, 2)
					
				if tile == 3:
					make_just_tile(goal_img, World.tile_width, col_count, row_count, 3)

				if tile == DEADLY:
					make_just_tile(water_img, World.tile_width, col_count, row_count, DEADLY)

				if tile == 5:
					make_just_tile(goal2_img, World.tile_width, col_count, row_count, 5)

				if tile == 6:
					enemy = Enemy(col_count * World.tile_width, row_count * World.tile_height, self.level, screen)
					self.world_enemy_group.add(enemy)
					self.enemy_places.append(enemy)
				
				if tile == 7:
					make_just_tile(rock_img, World.tile_width, col_count, row_count, 7)
				
				if tile == 8:
					make_just_tile(lava_img, World.tile_width, col_count, row_count, DEADLY)

				if tile == 9:
					make_just_tile(snow2_img, World.tile_width, col_count, row_count, 9)
				
				if tile == 10:
					make_just_tile(snow_img, World.tile_width, col_count, row_count, 10)

				if tile == 11:
					make_just_tile(water2_img, World.tile_width, col_count, row_count, DEADLY)

				if tile == 12:
					make_just_tile(ice_img, World.tile_width, col_count, row_count, 12)

				if tile == "b1":
					make_just_disappearing_block(rock_img, col_count, row_count, 2)

				if tile == "b2":
					make_just_disappearing_block(grass_img, col_count, row_count, 3)

				if tile == "b3":
					make_just_disappearing_block(snow_img, col_count, row_count, 2)

				if tile == "b4":
					make_just_disappearing_block(snow_img, col_count, row_count, 2)

				if tile == "p":
					self.player_place = Player(level, 0, col_count * World.tile_width, row_count * World.tile_height, screen)

				if tile == "fb":
					fireball = Fireball(col_count * World.tile_width, row_count * World.tile_height)
					tile = make_tile(lava_img, col_count, row_count, DEADLY)
					self.fireballs_group.add(fireball)
					self.tile_list.append(tile)
				
				if tile == "st":
					tile = make_tile(rock_img, col_count, row_count, 7)
					stalactite = Stalactite(col_count * World.tile_width, row_count * World.tile_height, tile)
					self.stalactite_group.add(stalactite)
					self.stalactite_places.append(stalactite)
					self.tile_list.append(tile)

				col_count += 1
			row_count += 1

			self.entities = Entities(
				enemy_group=self.world_enemy_group, 
				disappearing_blocks=self.dissaperaingBlocks, 
				fireball_group=self.fireballs_group, 
				stalactite_group=self.stalactite_group
			)




	def draw(self, pause, run, lang, ch_lang, fonts, screen, points, mouse = None):

		def draw_left_top_texts(points):
			if self.level < 5:
				chosen_color = Color().BLACK
			else:
				chosen_color = Color().WHITE

			level_text = fonts.font_size50.render(self.level_name, 0, chosen_color)
			points_number = fonts.font_size50.render(str(points), 0, chosen_color)
			level_text_place = level_text.get_rect()
			points_number_place = (level_text_place[0] + 255, level_text_place[1])
			screen.blit(level_text, level_text_place)
			screen.blit(points_number, points_number_place)


		for tile in self.tile_list:
			if pause and not run:

				if ch_lang == "en":
					quit_game_text_place = ((World.in_game_menu_rects[0].center[0])-(World.in_game_menu_rects[0].center[0]*0.30), World.in_game_menu_rects[0].center[1]-15)
				else:
					quit_game_text_place = ((World.in_game_menu_rects[0].center[0])-(World.in_game_menu_rects[0].center[0]*0.45), World.in_game_menu_rects[0].center[1]-15)

				for rect in World.in_game_menu_rects:
					square = pygame.draw.rect(screen, Color().BLACK, rect)
					if square.collidepoint(float(mouse[0]), float(mouse[1])) and mouse is not None:
						square = pygame.draw.rect(screen, Color().BLUE, rect)
				quit_game_text = fonts.font_size50.render(lang[ch_lang][5], 0, Color().RED)
				screen.blit(quit_game_text, quit_game_text_place)
				draw_left_top_texts(points)
				pygame.display.update()

			draw_left_top_texts(points)
			screen.blit(tile["image"], tile["imageRect"])
			
	def draw_broken_blocks(self, screen):
		for bloc in self.dissaperaingBlocks:
			bloc.update()
			bloc.draw(screen)


	def get_player(self):
		return self.player_place
	

	def not_player_objects(self, screen, player):
		self.draw_broken_blocks(screen)
		self.world_enemy_group.update(self.tile_list)
		self.world_enemy_group.draw(screen)
		self.fireballs_group.update()
		self.fireballs_group.draw(screen)
		self.stalactite_group.draw(screen)
		self.stalactite_group.update(player, self.tile_list)


	async def reload_when_player_died(self, points : int):
		remainedEnemy = len(self.world_enemy_group)
		originalEnemyNumer = len(self.enemy_places)
		szorzo = originalEnemyNumer - remainedEnemy
		pontCsokkentes = szorzo * 100
		points -= pontCsokkentes
		for enemy in self.enemy_places:
			self.world_enemy_group.remove(enemy)

		for enemy in self.enemy_places:
			self.world_enemy_group.add(enemy)

		for stal in self.stalactite_places:
			self.stalactite_group.remove(stal)

		for stal in self.stalactite_places:
			stal.set_to_default()
			self.stalactite_group.add(stal)

		if points >= 0:
			return points

		return 0