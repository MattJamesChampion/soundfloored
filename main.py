import configparser
from soundfloored.music_logic import MusicLogic

class Settings:
    def __init__(self, config_parser):
        try:
            self.root_audio_directory = config_parser["DEFAULT"]["RootAudioDirectory"]
        except KeyError:
            print("Could not find the root audio directory")
            raise

def get_settings(path):
    config_parser = configparser.ConfigParser()
    config_parser.read(path)

    return Settings(config_parser)

def main():
    settings = get_settings("settings.ini")

    MusicLogic(settings.root_audio_directory)

if __name__ == "__main__":
    main()
