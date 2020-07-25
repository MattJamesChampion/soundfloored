import pygame

class KeyboardInterface:
    def __init__(self, music_logic):
        self.music_logic = music_logic

    def start(self):
        pygame.display.init()
        screen = pygame.display.set_mode((1,1))

        available_control_keys = {
            pygame.K_1: self.music_logic.move_previous_repeat_style,
            pygame.K_4: self.music_logic.move_next_repeat_style,
            pygame.K_q: self.music_logic.decrement_bank,
            pygame.K_r: self.music_logic.increment_bank,
            pygame.K_SPACE: self.music_logic.stop_all_clips,
        }

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
                    try:
                        available_control_keys[event.key]()
                    except:
                        pass

                    try:
                        clip_position = available_clip_keys.index(event.key)
                        self.music_logic.play_clip(clip_position)
                    except (IndexError, ValueError):
                        pass
