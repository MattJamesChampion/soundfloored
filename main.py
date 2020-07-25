import configparser
from soundfloored.music_logic import MusicLogic
from soundfloored.interfaces.keyboard_interface import KeyboardInterface
from soundfloored.interfaces.gui_interface import GuiInterface

class Settings:
    def __init__(self, config_parser):
        try:
            self.root_audio_directory = config_parser["DEFAULT"]["RootAudioDirectory"]
        except KeyError:
            print("Could not find the root audio directory setting")
            raise

        try:
            self.interface = config_parser["DEFAULT"]["Interface"]
        except KeyError:
            print("Could not find the interface setting")
            raise

def get_settings(path):
    config_parser = configparser.ConfigParser()
    config_parser.read(path)

    return Settings(config_parser)

def main():
    settings = get_settings("settings.ini")

    music_logic = MusicLogic(settings.root_audio_directory)

    interface = None

    if settings.interface == "keyboard":
        interface = KeyboardInterface(music_logic)
    elif settings.interface == "gui":
        interface = GuiInterface(music_logic)

    interface.start()

if __name__ == "__main__":
    main()
