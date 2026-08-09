import pygame
from base import Base, resource_path
import base
from sound_manager import SoundManager

class Player():
    def __init__(self, rect):
        self.rect = rect
        self.frames = {
    'idle_right': base.load_sprite_sheet(
        pygame.image.load(resource_path("assets", "girl", "Idle.png")).convert_alpha(),
        rows=1, cols=5, frame_width=128, frame_height=128
    ),
    'idle_left': [
        pygame.transform.flip(sprite, True, False)
        for sprite in base.load_sprite_sheet(
            pygame.image.load(resource_path("assets", "girl", "Idle.png")).convert_alpha(),
            rows=1, cols=6, frame_width=128, frame_height=128
        )
    ],
    'running_right': base.load_sprite_sheet(
        pygame.image.load(resource_path("assets", "girl", "Run.png")).convert_alpha(),
        rows=1, cols=6, frame_width=128, frame_height=128
    ),
    'running_left': [
        pygame.transform.flip(sprite, True, False)
        for sprite in base.load_sprite_sheet(
            pygame.image.load(resource_path("assets", "girl", "Run.png")).convert_alpha(),
            rows=1, cols=6, frame_width=128, frame_height=128
        )
    ],
    'hurt_right': base.load_sprite_sheet(
        pygame.image.load(resource_path("assets", "girl", "Hurt.png")).convert_alpha(),
        rows=1, cols=2, frame_width=128, frame_height=128
    ) * 2,
    'hurt_left': [
        pygame.transform.flip(sprite, True, False)
        for sprite in base.load_sprite_sheet(
            pygame.image.load(resource_path("assets", "girl", "Hurt.png")).convert_alpha(),
            rows=1, cols=2, frame_width=128, frame_height=128
        )
    ] * 2,
    'dead_right': base.load_sprite_sheet(
        pygame.image.load(resource_path("assets", "girl", "Dead.png")).convert_alpha(),
        rows=1, cols=10, frame_width=128, frame_height=128
    ),
    'dead_left': [
        pygame.transform.flip(sprite, True, False)
        for sprite in base.load_sprite_sheet(
            pygame.image.load(resource_path("assets", "girl", "Dead.png")).convert_alpha(),
            rows=1, cols=10, frame_width=128, frame_height=128
        )
    ]
}
        self.dead = False
        self.score = 0
        self.hearts = 3
        self.hurt_delay = 0
        self.hurt_delay_ticks = 20
        self.state = 'idle_right'
        self.speed = 5
        self.current_animation = self.frames['idle_right']
        self.current_frame = 0
        self.frame_counter = 0
        self.animation_speed = 5
        self.direction = 'right'
        

    def draw(self, screen):
        sprite_offset = (-75, -85)
        sprite_pos = (self.rect.x + sprite_offset[0], self.rect.y + sprite_offset[1])
        screen.blit(self.current_animation[self.current_frame], sprite_pos)
        
    def move(self, direction):
        self.direction = direction
        if direction == 'left':
            if self.rect.x - self.speed > 0:
                self.rect.x -= self.speed
                Player.change_state(self, f'running_{direction}')
        elif direction == 'right':
            if self.rect.x + self.speed < Base.WIDTH-(Base.PLAYER_SIZE[0]/2):
                self.rect.x += self.speed
                Player.change_state(self, f'running_{direction}')
            
    def hurt(self):
        if self.hurt_delay <= 0 & self.dead:
            self.hearts -= 1
            self.hurt_delay = self.hurt_delay_ticks
            Base.sound_manager.play('hurt', 0.9)
            if self.hearts > 0:
                Player.change_state(self, f'hurt_{self.direction}')
            else:
                Player.change_state(self, f'dead_{self.direction}')
                
        
            
    def change_state(self, state):
        if 'hurt' in self.state:
            if self.current_frame != 3:
                return
        if 'dead' in self.state:
            if self.current_frame != 9:
                return
            else:
                self.dead = True
                self.rect.y += 400
        self.state = state
        if self.current_animation != self.frames[state]:
            self.current_animation = self.frames[state]
            self.current_frame = 0
            
    def update_animation(self):
        self.frame_counter += 1
        if self.frame_counter >= self.animation_speed:
            if 'hurt dead' in self.state:
                if self.current_frame == 3:
                    Player.change_state(self, f'running_{self.direction}')
            self.frame_counter = 0
            self.current_frame = (self.current_frame + 1) % len(self.current_animation)
    
    def update(self, screen):
        if self.dead == True:
            base.draw_text(screen, f'You died :(', 400, 250, Base.death_font, 'red')
            return
        Player.update_animation(self)
        self.draw(screen)
        self.draw_hearts(screen)
        
        self.score += 0.025
        
        if 'idle' not in self.state:
            if self.pos == (self.rect.x, self.rect.y):
                Player.change_state(self, f'idle_{self.direction}')

        if self.hurt_delay > 0:
            self.hurt_delay -= 1
            
        if 'hurt' in self.current_animation:
            pass
        
        self.pos = (self.rect.x, self.rect.y)
        
    def draw_hearts(self, screen):
        x, y = 925, 15
        for _ in range(self.hearts):
            screen.blit(Base.heart_img.convert_alpha(), (x, y))
            x -= 50