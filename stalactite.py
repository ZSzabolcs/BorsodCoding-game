import pygame
import os

class Stalactite(pygame.sprite.Sprite):
	def __init__(self, x, y, tile):
		pygame.sprite.Sprite.__init__(self)
		image = pygame.image.load(os.path.join("kepek", "tuzgolyo.png"))
		self.image = pygame.transform.scale(image, (25, 25))
		self.rect = self.image.get_rect()
		self.rect.x = x + 15
		self.rect.y = y + 30
		self.start_x = x
		self.start_y = y
		self.initial_y = y
		self.starting_tile = tile["imageRect"]
		self.fall = 0
		self.vertical_velocity = 7

	def update(self, player, tile_list : list):
		if player.rect.y - 250 <= self.rect.y and player.rect.x + 15 >= self.rect.x:
			self.fall = 1

		if self.fall:
			self.rect.y += self.vertical_velocity
			for tile in tile_list:
				if self.rect.colliderect(tile["imageRect"]) and not self.rect.colliderect(self.starting_tile):
					self.kill()

		if self.rect.colliderect(player):
			player.died = 1