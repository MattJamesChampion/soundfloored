import configparser
import logging
import sys
import os
from enum import Enum
from soundfloored.music_logic import MusicLogic, MusicLogicSettings, RepeatStyle
from soundfloored.interfaces.keyboard_interface import KeyboardInterface
from soundfloored.interfaces.gui_interface import GuiInterface
from soundfloored.interfaces.rpi_interface import RpiInterface

class Settings:
    def __init__(self, config_parser):
        self._logger = logging.getLogger(__name__)
        try:
            self.root_audio_directory = config_parser["DEFAULT"]["RootAudioDirectory"]
        except KeyError:
            self._logger.error("Could not find the root audio directory setting")
            raise
        
        try:
            self.backup_root_audio_directory = config_parser["DEFAULT"]["BackupRootAudioDirectory"]
        except KeyError:
            self._logger.debug("Could not find the backup root audio directory setting, setting value to None")
            self.backup_root_audio_directory = None

        try:
            self.interface = config_parser["DEFAULT"]["Interface"]
        except KeyError:
            self._logger.error("Could not find the interface setting")
            raise

        try:
            initial_repeat_style = config_parser["DEFAULT"]["InitialRepeatStyle"]
            self.initial_repeat_style = RepeatStyle[initial_repeat_style.upper()]
        except KeyError:
            self._logger.error("Could not find/load the initial repeat style setting, setting value to None")
            self.initial_repeat_style = None

def get_settings(path):
    config_parser = configparser.ConfigParser()
    config_parser.read(path)

    return Settings(config_parser)

class Interfaces(Enum):
    KEYBOARD = 0,
    GUI = 1,
    RPI = 2

def main():
    settings = get_settings(os.path.join(os.path.dirname(__file__), "settings.ini"))

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    music_logic_settings = MusicLogicSettings(settings.root_audio_directory, backup_root_audio_directory=settings.backup_root_audio_directory, initial_repeat_style=settings.initial_repeat_style)
    music_logic = MusicLogic(music_logic_settings)

    interface = None

    interface_dict = {
        Interfaces.KEYBOARD: KeyboardInterface,
        Interfaces.GUI: GuiInterface,
        Interfaces.RPI: RpiInterface
    }

    try:
        interface_enum_instance = Interfaces[settings.interface.upper()]
        interface_class = interface_dict[interface_enum_instance]
        logging.debug(f"Creating instance of {interface_class.__name__}")
        interface = interface_class(music_logic)
    except:
        logging.error(f"Could not load interface {settings.interface}")
        raise

    interface.start()

if __name__ == "__main__":
    main()
