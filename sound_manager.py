import pygame
from random import randint
import base
import os

class SoundManager():
    def __init__(self):
        pygame.mixer.init()
        track_path = base.resource_path("assets", "track")
        self.music_tracks = []
        self.sounds = {'hurt': [pygame.mixer.Sound(base.resource_path("assets", "girl", "hurt", f"hurt{i+1}.wav")) for i in range(5)]}
        self.music_tracks = [os.path.join(track_path, filename) for filename in os.listdir(track_path) if filename.endswith('.mp3')]
        self.current_track = randint(0, len(self.music_tracks) - 1)
        
        
    def play_next_track(self): #* For the background audio
        pygame.mixer.music.load(self.music_tracks[self.current_track])
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play()
        self.current_track = (self.current_track + 1) % len(self.music_tracks)
    
    
    def play(self, sound_type, volume): #* Play sound effects
        sound = self.sounds.get(sound_type)[randint(0, len(self.sounds[sound_type])-1)]
        sound.set_volume(sound.get_volume() + volume)
        sound.play()


