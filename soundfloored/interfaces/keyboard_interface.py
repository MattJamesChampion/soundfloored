import pygame

class KeyboardInterface:
    def __init__(self, music_logic):
        self.music_logic = music_logic

    def start(self):
        pygame.display.init()
        screen = pygame.display.set_mode((1,1))
        current_bank = self.music_logic.get_current_bank()

        available_clip_keys = [
            pygame.K_a,
            pygame.K_s,
            pygame.K_d,
            pygame.K_f
        ]

        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        current_bank = self.music_logic.decrement_bank()
                    if event.key == pygame.K_r:
                        current_bank = self.music_logic.increment_bank()
                    try:
                        clip_position = available_clip_keys.index(event.key)
                        current_bank.play_clip(clip_position)
                    except:
                        pass
