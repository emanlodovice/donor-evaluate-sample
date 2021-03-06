import os
import sys
import pygame

from asset import resource_path


class Avatar:

    def __init__(self, image, size):
        self.image_name = image
        # self.image = pygame.image.load(os.path.join(f"assets/{image}"))
        self.image = pygame.image.load(resource_path(f"assets/{image}"))
        self.image = pygame.transform.scale(self.image, (size, size))
    
    def draw(self, screen, x, y):
        screen.blit(self.image, (x, y))
