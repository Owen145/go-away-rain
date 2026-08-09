import pygame
from pathlib import Path
import sys
from sound_manager import SoundManager
pygame.font.init()

def resource_path(*parts) -> str:
    """
    Join parts to the app's runtime directory.
    Works in dev and when frozen by PyInstaller.
    """
    base = Path(getattr(sys, "_MEIPASS", Path(__file__).parent))  # _MEIPASS when frozen
    return str(base.joinpath(*parts))

#* ---------------
#* Base class
#* ---------------

class Base:
    WIDTH, HEIGHT = 1000, 800
    PLAYER_SIZE = (40, 105)
    RAINDROP_SIZE = (64, 80)
    DRAW_HITBOX = False
    death_font = pygame.font.SysFont('comicsansms', 50)
    score_font = pygame.font.SysFont('comicsansms', 30)
    background = pygame.transform.scale(pygame.image.load(resource_path("assets", "background.png")), (WIDTH, HEIGHT))
    heart_img  = pygame.image.load(resource_path("assets", "heart.png"))
    sound_manager = SoundManager()



#* ---------------
#* Global functions
#* ---------------

def load_sprite_sheet(sheet, rows, cols, frame_width, frame_height, scale=1.5):
    frames = []
    sheet_width, sheet_height = sheet.get_width(), sheet.get_height()
    
    for row in range(rows):
        for col in range(cols):
            x, y = col * frame_width, row * frame_height
            if x + frame_width <= sheet_width and y + frame_height <= sheet_height:
                frame = sheet.subsurface((x, y, frame_width, frame_height))
                scaled_frame = pygame.transform.scale(frame, (frame_width * scale, frame_height * scale))
                frames.append(scaled_frame)
    return frames


def draw_text(surface, text, x, y, font, color='black'):
    text_surface = font.render(text, False, color)
    surface.blit(text_surface, (x,y))
    
    
def draw_score(screen, score): #! Use draw text for this
    draw_text(screen, f'Score: {score}', 450, 15, Base.score_font, 'lightblue')

def ticks_to_mins(ticks): #! Use draw text for this
    pass