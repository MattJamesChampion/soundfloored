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
    
DEFAULT_REPEAT_STYLE = RepeatStyle.STOP

class MusicLogicSettings:
    def __init__(self, root_audio_directory, initial_repeat_style=DEFAULT_REPEAT_STYLE):
        self._logger = logging.getLogger(__name__)

        self.root_audio_directory = root_audio_directory

        if initial_repeat_style != None:
            self.initial_repeat_style = initial_repeat_style
        else:
            self._logger.debug(f"MusicLogicSettings created with an initial_repeat_style of None, modifying value to {DEFAULT_REPEAT_STYLE.name}")
            self.initial_repeat_style = DEFAULT_REPEAT_STYLE

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
            for relative_clip_path in sorted(os.listdir(path)):
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
    def __init__(self, music_logic_settings):
        self._logger = logging.getLogger(__name__)
        self.root_audio_directory = music_logic_settings.root_audio_directory
        self.repeat_style = music_logic_settings.initial_repeat_style
        self.banks = []
        self._manually_stopped_channels = set()
        self.current_bank_position = None

        pygame.init()

        self.load_banks()

        if len(self.banks) > 0:
            self.current_bank_position = 0

    def _play_channel(self, channel, clip):
        self._logger.debug(f"Playing clip {clip.name} on channel {channel}")
        pygame.mixer.Channel(channel).play(clip.sound)

    def _stop_channel(self, channel):
        self._logger.debug(f"Stopping clip on channel {channel}")
        self._manually_stopped_channels.add(channel)
        pygame.mixer.Channel(channel).stop()

    def play_clip(self, position, bank=None, repeat_style=None, is_distinct_trigger=True):
        if bank == None:
            bank = self.get_current_bank()
        
        if repeat_style == None:
            repeat_style = self.repeat_style

        is_busy_channel = pygame.mixer.Channel(position).get_busy()

        if is_distinct_trigger:
            # Used to avoid thousands of identical log entries
            self._logger.debug(f"play_clip executing with position {position}, bank {bank.name} and repeat_style {repeat_style.name}")

        try:
            clip = bank.clips[position]

            if repeat_style == RepeatStyle.STOP:
                if is_distinct_trigger:
                    try:
                        self._manually_stopped_channels.remove(position)
                    except:
                        pass

                    if is_busy_channel:
                        self._stop_channel(position)
                    else:
                        self._play_channel(position, clip)
                else:
                    if is_busy_channel:
                        return
                    else:
                        # Drop any requests that come in after manually stopping a channel
                        # until it has been manually started again (to prevent a channel from
                        # starting a split second after being stopped from the same button press)
                        if position in self._manually_stopped_channels:
                            return
                        else:
                            self._play_channel(position, clip)
            elif repeat_style == RepeatStyle.RESTART:
                if is_distinct_trigger:
                    self._play_channel(position, clip)
                else:
                    if is_busy_channel:
                        return
                    else:
                        self._play_channel(position, clip)
        except IndexError:
            if is_distinct_trigger:
                # Used to avoid thousands of identical log entries
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
    
    @property
    def repeat_style(self):
        return self._repeat_style

    @repeat_style.setter
    def repeat_style(self, value):
        self._repeat_style = value

    def load_banks(self):
        # The below is done to resolve issues with playback slow to start
        # on certain devices (such as on Raspberry Pis)
        # https://stackoverflow.com/a/55125080
        pygame.mixer.pre_init(22050, -16, 2, 1024)
        pygame.init()
        pygame.mixer.quit()
        pygame.mixer.init(22050, -16, 2, 1024)
        
        banks = []
        self._logger.debug(f"Loading banks (with root directory {self.root_audio_directory})")
        
        for relative_bank_path in sorted(os.listdir(self.root_audio_directory)):
            full_bank_path = os.path.join(self.root_audio_directory, relative_bank_path)
            try:
                bank = Bank(full_bank_path)
                if len(bank.clips) > 0:
                    banks.append(bank)
                else:
                    self._logger.debug(f"Bank {bank.name} has 0 clips, skipping")
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

    def stop_all_clips(self):
        pygame.mixer.stop()
