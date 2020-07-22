import os
import pygame

class Bank:
    def __init__(self, name, clips):
        self.name = name
        self.clips = clips

class MusicLogic:
    def __init__(self, root_audio_directory):
        self.root_audio_directory = root_audio_directory
        self.banks = []

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
