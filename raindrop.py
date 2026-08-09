import pygame
from random import randint
from base import Base, resource_path
import base
from sound_manager import SoundManager

class Raindrop():
    def __init__(self, rect):
        self.rect = rect
        self.dead = False
        self.sprite = pygame.transform.scale(pygame.image.load(resource_path("assets","raindrop.png")), (Base.RAINDROP_SIZE[0], Base.RAINDROP_SIZE[1]))
        self.sprite_death = pygame.transform.scale(pygame.image.load(resource_path("assets","raindrop_die.png")), (Base.RAINDROP_SIZE[0], Base.RAINDROP_SIZE[1]))
        self.death_count_ticks = 0
        self.death_count_ticks_max = 4
        
    def spawn_raindrop(raindrops):
        drop = Raindrop(pygame.Rect(randint(0,1000), -Base.RAINDROP_SIZE[1], Base.RAINDROP_SIZE[0], Base.RAINDROP_SIZE[1]))
        raindrops.append(drop)
        return raindrops
    
    def fall(self):
        if self.rect.y < randint(520,790):
                self.rect.y += 8
        else:
            Raindrop.die(self)
    
    def die(self):
        self.dead = True
        
    def draw(self, screen):
        if self.dead:
            if self.death_count_ticks < self.death_count_ticks_max:
                screen.blit(self.sprite_death, (self.rect.x, self.rect.y))
                self.death_count_ticks += 1
        else:
            screen.blit(self.sprite, (self.rect.x, self.rect.y))
    
    
    def update(self, screen):
        Raindrop.fall(self)
        self.draw(screen)