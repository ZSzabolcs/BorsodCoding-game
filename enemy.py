import os
import pygame

class Enemy(pygame.sprite.Sprite):
	def __init__(self, x, y, level):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load(os.path.join("kepek", "enemy.png")).convert()
		self.image = pygame.transform.scale(img, (40, 40))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.move_direction = 1
		self.speed = 1
		self.level = level

	def update(self, tile_list):
		next_x = self.rect.x + self.move_direction * self.speed
		next_bottom = self.rect.bottom + 1
		ground_beneath_next = 0
		self.rect.x += self.move_direction * self.speed

		for tile in tile_list:
				if tile["imageRect"].collidepoint(self.rect.right, self.rect.midright[1]) and tile["number"] > 0:
					self.move_direction *= -1
				if tile["imageRect"].collidepoint(self.rect.left, self.rect.midleft[1]) and tile["number"] > 0:
					self.move_direction *= -1
				if tile["imageRect"].colliderect(next_x + self.rect.width // 2, next_bottom, 1, 1):
					ground_beneath_next = 1

		if not ground_beneath_next:
			self.move_direction *= -1