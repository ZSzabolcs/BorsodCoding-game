import pygame
import os

class Stalactite(pygame.sprite.Sprite):
	def __init__(self, x, y, tile):
		pygame.sprite.Sprite.__init__(self)
		image = pygame.image.load(os.path.join("kepek", "cseppko.png")).convert()
		self.image = pygame.transform.scale(image, (15, 15))
		self.rect = self.image.get_rect()
		self.rect.x = x + 15
		self.rect.y = y + 30
		self.start_x = self.rect.x
		self.start_y = self.rect.y
		self.starting_tile = tile["imageRect"]
		self.is_falling = False
		self.vertical_velocity = 7

	def update(self, player, tile_list : list):
		if player.rect.y - 250 <= self.rect.y and player.rect.x + 15 >= self.rect.x:
			self.is_falling = True

		if self.is_falling:
			self.rect.y += self.vertical_velocity
			for tile in tile_list:
				if self.rect.colliderect(tile["imageRect"]) and not self.rect.colliderect(self.starting_tile):
					self.kill()

		if self.rect.colliderect(player):
			player.died = True

	def set_to_default(self):
		self.rect.x = self.start_x
		self.rect.y = self.start_y
		self.is_falling = False