import os

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
        for bank in [f for f in os.listdir(self.root_audio_directory)]:
            bank_path = os.path.join(self.root_audio_directory, bank)
            clips = []
            for clip in os.listdir(bank_path):
                clips.append(os.path.join(self.root_audio_directory, clip))

            banks.append(Bank(bank_path, clips))

        self.banks = banks
