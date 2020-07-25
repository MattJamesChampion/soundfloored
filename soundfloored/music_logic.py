import os
import pygame
from enum import Enum

class RepeatStyle(Enum):
    #Values must be sequential starting from 0
    RESTART = 0
    STOP = 1

class Bank:
    def __init__(self, name, clips):
        self.name = name
        self.clips = clips

class MusicLogic:
    def __init__(self, root_audio_directory):
        self.root_audio_directory = root_audio_directory
        self.repeat_style = RepeatStyle.RESTART
        self.banks = []

        self.current_bank_position = None

        pygame.init()

        self.load_banks()

        if len(self.banks) > 0:
            self.current_bank_position = 0

    def play_clip(self, position, bank=None, repeat_style=None):
        if bank == None:
            bank = self.get_current_bank()
        
        if repeat_style == None:
            repeat_style = self.repeat_style

        try:
            #TODO: Increase number of channels if position is greater than the default of 10
        
            clip = bank.clips[position]
            if repeat_style == RepeatStyle.RESTART:
                pygame.mixer.Channel(position).play(clip)

            elif repeat_style == RepeatStyle.STOP:
                if pygame.mixer.Channel(position).get_busy():
                    pygame.mixer.Channel(position).stop()
                else:
                    pygame.mixer.Channel(position).play(clip)
        except IndexError:
            pass


    def increment_bank(self):
        maximum_bank_position = len(self.banks) - 1
        if self.current_bank_position >= maximum_bank_position:
            self.current_bank_position = 0
        else:
            self.current_bank_position += 1
        return self.get_current_bank()
        
    def decrement_bank(self):
        maximum_bank_position = len(self.banks) - 1
        if self.current_bank_position == 0:
            self.current_bank_position = maximum_bank_position
        else:
            self.current_bank_position -= 1
        return self.get_current_bank()

    def get_current_bank(self):
        return self.banks[self.current_bank_position]

    @property
    def current_bank_position(self):
        return self._current_bank

    @current_bank_position.setter
    def current_bank_position(self, value):
        self._current_bank = value

    def move_next_repeat_style(self):
        maximum_repeat_style = len(RepeatStyle) - 1
        if self.repeat_style.value == maximum_repeat_style:
            self.repeat_style = RepeatStyle(0)
        else:
            self.repeat_style = RepeatStyle(self.repeat_style.value + 1)

        return self.repeat_style
    
    def move_previous_repeat_style(self):
        maximum_repeat_style = len(RepeatStyle) - 1
        if self.repeat_style.value == 0:
            self.repeat_style = RepeatStyle(maximum_repeat_style)
        else:
            self.repeat_style = RepeatStyle(self.repeat_style.value - 1)

        return self.repeat_style

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
