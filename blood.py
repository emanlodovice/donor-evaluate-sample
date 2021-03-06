import os
import sys
import pygame

from asset import resource_path


class Blood:
    def __init__(self, x, speed, image, from_right_donor):
        self.x = x
        self.y = 140
        self.speed = speed
        self.image = pygame.image.load(resource_path(f"assets/{image}.png"))
        self.image = pygame.transform.scale(self.image, (90, 90))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.from_right_donor = from_right_donor
        self.is_clicked = False

    
    def move(self):
        self.y += self.speed
        self.rect.center = (self.x, self.y)
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        
    def has_left_screen(self, screen_height):
        return self.y > screen_height
    
    def check_hit(self, x, y):
        self.is_clicked = self.rect.collidepoint(x, y)
        return self.is_clicked
            
