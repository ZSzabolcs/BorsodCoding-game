import pygame
import os


class Fireball(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		image = pygame.image.load(os.path.join("kepek", "tuzgolyo.png"))
		self.image = pygame.transform.scale(image, (25, 25))
		self.rect = self.image.get_rect()
		self.rect.x = x + 15
		self.rect.y = y
		self.start_x = x
		self.start_y = y
		self.initial_y = y
		self.vertical_velocity = -4

	def update(self):
		self.rect.y += self.vertical_velocity
		distance_revealed = abs(self.initial_y - self.rect.y)

		if self.vertical_velocity < 0:
			if distance_revealed >= 200:
				self.vertical_velocity *= -1
		elif self.vertical_velocity > 0:
			if self.rect.y >= self.initial_y:
				self.vertical_velocity = -4
				self.rect.y = self.initial_y