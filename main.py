import configparser
import logging
import sys
from soundfloored.music_logic import MusicLogic
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

def get_settings(path):
    config_parser = configparser.ConfigParser()
    config_parser.read(path)

    return Settings(config_parser)

def main():
    settings = get_settings("settings.ini")

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    music_logic = MusicLogic(settings.root_audio_directory)

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
