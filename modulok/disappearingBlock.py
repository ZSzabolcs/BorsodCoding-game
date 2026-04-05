import pygame
import time


class DisappearingBlock(pygame.sprite.Sprite):
	def __init__(self, x, y, image, second):
		pygame.sprite.Sprite.__init__(self)
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.visible = True
		self.last_toggle_time = time.time()
		self.sec = second

	def update(self):
		current_time = time.time()
		if current_time - self.last_toggle_time > self.sec:
			self.visible = not self.visible
			self.last_toggle_time = current_time

	def draw(self, surface):
		if self.visible:
			surface.blit(self.image, self.rect)