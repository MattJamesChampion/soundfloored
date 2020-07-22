import os
import pygame

class Bank:
    def __init__(self, name, clips):
        self.name = name
        self.clips = clips
    
    def play_clip(self, position):
        #TODO: Increase number of channels if position is greater than the default of 10
        clip = self.clips[position]
        pygame.mixer.Channel(position).play(clip)
        

class MusicLogic:
    def __init__(self, root_audio_directory):
        self.root_audio_directory = root_audio_directory
        self.banks = []

        self.current_bank_position = None

        pygame.init()

        self.load_banks()

        if len(self.banks) > 0:
            self.current_bank_position = 0

    def get_current_bank(self):
        return self.banks[self.current_bank_position]

    @property
    def current_bank_position(self):
        return self._current_bank

    @current_bank_position.setter
    def current_bank_position(self, value):
        self._current_bank = value

    def load_banks(self):
        pygame.mixer.init()
        
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

        try:
            if self.current_bank_position > len(self.banks) - 1:
                # We may have loaded fewer banks than before. If that's the case,
                # we need to reset the current bank to avoid an IndexError
                self.current_bank_position = 0
        except TypeError:
            pass
