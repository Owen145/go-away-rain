 #* 3/5/25
#todo - Some kind of objective (other than staying alive)
#todo - Statistics & Scoring
#todo - Make different kinds of raindrops (ie. drop hearts or speed boost, big splash(AOE))
#todo - Events (ie. Blood rain(bullet hell), )
#todo - Music & Sounds (ie. hurt, death, ambient)
#todo - Main Menu
#todo - Multiplayer?


import pygame
import random
from player import Player
from raindrop import Raindrop
from base import Base
import base

#* Initialize everything
pygame.init()
pygame.font.init()
pygame.mixer.init()


#* Set up display
screen = pygame.display.set_mode((Base.WIDTH, Base.HEIGHT))
pygame.display.set_caption("Go Away Rain")

background = Base.background.convert()

DROP_SOMETHING = pygame.USEREVENT+1
pygame.time.set_timer(DROP_SOMETHING, 1000)

MUSIC_END = pygame.USEREVENT+2
pygame.mixer.music.set_endevent(MUSIC_END)
Base.sound_manager.play_next_track()


def main():
    running = True
    raindrops = []
    player = Player(pygame.Rect(500, 655-Base.PLAYER_SIZE[1], Base.PLAYER_SIZE[0], Base.PLAYER_SIZE[1]))
    clock = pygame.time.Clock()
    while running:
        clock.tick(60) #* The maximum amount of FPS (refreshes/second)

        #* Event handler
        for event in pygame.event.get():
            #* Game ending logic
            if player.dead:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    main()
            
            #* Play soundtrack
            if event.type == MUSIC_END:
                Base.sound_manager.play_next_track()
            
            #* Drop an item event
            if event.type == DROP_SOMETHING:
                if random.random() < 0.01:
                    pass #! Do stuff
            
            #* Quit
            if event.type == pygame.QUIT:
                running = False
            

        #* Movement & Keybinds
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]: player.move('left')
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]: player.move('right')
    
    
        #* Draw background
        screen.blit(background, (0, 0))
        
        #* Spawn raindrops
        if pygame.time.get_ticks() % 30 == 0:
            for i in range(random.randint(1,3)):
                raindrops = Raindrop.spawn_raindrop(raindrops)
        
        #* Collisions
        for i, raindrop in enumerate(raindrops):
            raindrop.update(screen)
            if not raindrop.dead: 
                if raindrop.rect.colliderect(player):
                    player.hurt()
                    raindrop.die()
            else: 
                if raindrop.death_count_ticks >= raindrop.death_count_ticks_max:
                    del raindrops[i]
        
        #* Update the player
        player.update(screen)
        
        #* Hitboxes (configure in Base class)
        if Base.DRAW_HITBOX:
            pygame.draw.rect(screen, (255, 0, 0), player.rect, 2)
            for raindrop in raindrops: 
                pygame.draw.rect(screen, (250, 0, 0), raindrop.rect, 2)

        #* Draw the score & refresh the screen
        base.draw_score(screen, int(player.score))
        pygame.display.flip()
    
    #* Exit the game
    pygame.quit()
    
    
    
if __name__ == '__main__':
    main()