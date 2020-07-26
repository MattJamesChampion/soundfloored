import configparser
import logging
import sys
from soundfloored.music_logic import MusicLogic, MusicLogicSettings, RepeatStyle
from soundfloored.interfaces.keyboard_interface import KeyboardInterface
from soundfloored.interfaces.gui_interface import GuiInterface

class Settings:
    def __init__(self, config_parser):
        self._logger = logging.getLogger(__name__)
        try:
            self.root_audio_directory = config_parser["DEFAULT"]["RootAudioDirectory"]
        except KeyError:
            self._logger.error("Could not find the root audio directory setting")
            raise

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

def main():
    settings = get_settings("settings.ini")

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    music_logic_settings = MusicLogicSettings(settings.root_audio_directory, settings.initial_repeat_style)
    music_logic = MusicLogic(music_logic_settings)

    interface = None

    if settings.interface == "keyboard":
        logging.debug("Creating instance of KeyboardInterface")
        interface = KeyboardInterface(music_logic)
    elif settings.interface == "gui":
        logging.debug("Creating instance of GuiInterface")
        interface = GuiInterface(music_logic)

    interface.start()

if __name__ == "__main__":
    main()
