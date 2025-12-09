import pygame
import os
from entities import Entities

class Player():
	def __init__(self, level, completed, x, y, tile_width, tile_height, screen):
		img = pygame.image.load(os.path.join("kepek", "trollface.jpg"))
		self.image = pygame.transform.scale(img, (tile_width - tile_width * 0.2, tile_height - tile_height * 0.2))
		self.rect = self.image.get_rect()
		self.level = level - 1
		self.rect.x = x
		self.rect.y = y
		self.jumpvalue = 0
		if screen.get_width() == 750 and screen.get_height() == 750:
			self.vel_y = -13
		else:
			self.vel_y = -15
		self.jumped = 0
		self.width = self.image.get_width()
		self.height = self.image.get_height()
		self.checkpoint_x = self.rect.x
		self.checkpoint_y = self.rect.y
		self.died = 0
		self.completed = completed
		self.player_place = None

	def update(self, tile_list, entities : Entities, screen : pygame.display):
		dx = 0
		dy = 0
		key = pygame.key.get_pressed()
		if key[pygame.K_LEFT]:
			dx -= 5
		if key[pygame.K_RIGHT]:
			dx += 5
		if key[pygame.K_UP] and self.jumped == 0:
			self.jumpvalue += self.vel_y
			self.jumped = 1

		self.jumpvalue += 1
		if self.jumpvalue > 10:
			self.jumpvalue = 10
		dy += self.jumpvalue

		for tile in tile_list:
			if tile["imageRect"].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
				if key[pygame.K_UP] == 0:
					self.jumped = 0
				if self.jumpvalue < 0:
					dy = tile["imageRect"].bottom - self.rect.top
					self.jumpvalue = 0
				elif self.jumpvalue >= 0:
					dy = tile["imageRect"].top - self.rect.bottom
					self.jumpvalue = 0
				if tile["number"] == 4:
					self.died = 1
				if tile["number"] == 3:
					self.checkpoint_x = tile["imageRect"].x
					self.checkpoint_y = tile["imageRect"].y
				if tile["number"] == 5:
					return 1
		
			if tile["imageRect"].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
				dx = 0

		for enemy in entities.enemy_group:
			if self.rect.colliderect(enemy.rect):
				if self.rect.bottom <= enemy.rect.top + 10:
					enemy.kill()  
					self.jumpvalue = -10 
				else: 
					self.died = 1

		for block in entities.disappearing_blocks:
			if block.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
				if key[pygame.K_UP] == 0:
					self.jumped = 0
				if self.jumpvalue < 0 and block.visible:
					dy = block.rect.bottom - self.rect.top
					self.jumpvalue = 0					
				elif self.jumpvalue >= 0 and block.visible:
					dy = block.rect.top - self.rect.bottom
					self.jumpvalue = 0


		for fireball in entities.fireball_group:
			if self.rect.colliderect(fireball.rect):
				self.died = 1

		if self.rect.bottom > screen.get_height():
			self.rect.bottom = screen.get_height()
			dy = 0
			
		if self.died == 0:
			self.rect.x += dx
			self.rect.y += dy
		
		else:
			self.rect.x = self.checkpoint_x
			self.rect.y = self.checkpoint_y
			self.died = 0

		screen.blit(self.image, self.rect)