import os
import pygame
from enum import Enum
import logging
import re

class MusicLogicHelpers:
    @staticmethod
    def clean_name(name):
        matching_pattern = r"(\d+-)?(.*)"
        replacement_pattern = r"\2"

        try:
            cleaned_name = re.sub(matching_pattern, replacement_pattern, name)

            if cleaned_name != "":
                return cleaned_name
            else:
                return name
        except:
            return name


class RepeatStyle(Enum):
    #Values must be sequential starting from 0
    RESTART = 0
    STOP = 1

class Clip:
    def __init__(self, path):
        self._logger = logging.getLogger(__name__)

        self._logger.debug(f"Loading clip {path}")

        try:
            self.name = MusicLogicHelpers.clean_name(os.path.basename(os.path.normpath(path)))
            self.sound = pygame.mixer.Sound(path)

            self._logger.debug(f"Clip {self.name} loaded")
        except:
            self._logger.error(f"Error loading clip with path {path}")
            raise

class Bank:
    def __init__(self, path):
        self._logger = logging.getLogger(__name__)

        self._logger.debug(f"Loading bank {path}")

        try:
            clips = []
            for relative_clip_path in os.listdir(path):
                full_clip_path = os.path.join(path, relative_clip_path)
                try:
                    clip = Clip(full_clip_path)
                    clips.append(clip)
                except:
                    self._logger.error(f"Clip could not be loaded with path {full_clip_path}, skipping")

            self.name = MusicLogicHelpers.clean_name(os.path.basename(os.path.normpath(path)))
            self.clips = clips

            self._logger.debug(f"Bank {self.name} loaded with {len(self.clips)} elements")
        except:
            self._logger.error(f"Error loading bank with path {path}")
            raise

class MusicLogic:
    def __init__(self, root_audio_directory):
        self._logger = logging.getLogger(__name__)
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

        self._logger.debug(f"play_clip executing with position {position}, bank {bank.name} and repeat_style {repeat_style.name}")
        try:
            #TODO: Increase number of channels if position is greater than the default of 10
        
            clip = bank.clips[position]
            if repeat_style == RepeatStyle.RESTART:
                pygame.mixer.Channel(position).play(clip.sound)

            elif repeat_style == RepeatStyle.STOP:
                if pygame.mixer.Channel(position).get_busy():
                    pygame.mixer.Channel(position).stop()
                else:
                    pygame.mixer.Channel(position).play(clip.sound)
        except IndexError:
            self._logger.debug(f"play_clip referenced an invalid index (requested position {position} of a bank with only {len(bank.clips)} elements)")


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
        self._logger.debug(f"Bank position set to {self._current_bank}")

    def move_next_repeat_style(self):
        maximum_repeat_style = len(RepeatStyle) - 1
        if self.repeat_style.value == maximum_repeat_style:
            self.repeat_style = RepeatStyle(0)
        else:
            self.repeat_style = RepeatStyle(self.repeat_style.value + 1)

        self._logger.debug(f"Repeat style set to {self.repeat_style.name}")

        return self.repeat_style
    
    def move_previous_repeat_style(self):
        maximum_repeat_style = len(RepeatStyle) - 1
        if self.repeat_style.value == 0:
            self.repeat_style = RepeatStyle(maximum_repeat_style)
        else:
            self.repeat_style = RepeatStyle(self.repeat_style.value - 1)

        self._logger.debug(f"Repeat style set to {self.repeat_style.name}")

        return self.repeat_style

    def load_banks(self):
        pygame.mixer.init()
        
        banks = []
        self._logger.debug(f"Loading banks (with root directory {self.root_audio_directory})")
        
        for relative_bank_path in os.listdir(self.root_audio_directory):
            full_bank_path = os.path.join(self.root_audio_directory, relative_bank_path)
            try:
                bank = Bank(full_bank_path)
                banks.append(bank)
            except:
                self._logger.error(f"Bank could not be loaded with path {full_bank_path}, skipping")

        self.banks = banks

        try:
            if self.current_bank_position > len(self.banks) - 1:
                # We may have loaded fewer banks than before. If that's the case,
                # we need to reset the current bank to avoid an IndexError
                self.current_bank_position = 0
        except TypeError:
            pass
