import os
import pygame

class Bank:
    def __init__(self, name, clips):
        self.name = name
        self.clips = clips
    
    def play_clip(self, position):
        #TODO: Increase number of channels if position is greater than the default of 10
        clip = self.clips[position - 1]
        pygame.mixer.Channel(position).play(clip)
        

class MusicLogic:
    def __init__(self, root_audio_directory):
        self.root_audio_directory = root_audio_directory
        self.banks = []

        self.load_banks()

        self.current_bank = None
        if len(self.banks) > 0:
            self.current_bank = 0

        pygame.init()
        pygame.mixer.init()

    def load_banks(self):
        banks = []
        for bank in os.listdir(self.root_audio_directory):
            bank_path = os.path.join(self.root_audio_directory, bank)
            clips = []
            for clip in os.listdir(bank_path):
                clip_path = os.path.join(bank_path, clip)
                clip_sound = pygame.mixer.Sound(clip_path)
                clips.append(clip_sound)

            banks.append(Bank(bank_path, clips))

        self.banks = banks
