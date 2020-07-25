import pygame
import tkinter
from functools import partial
from ..music_logic import RepeatStyle

class GuiInterface:
    def __init__(self, music_logic):
        self.music_logic = music_logic

    def get_and_play_clip(self, position):
        current_bank = self.music_logic.get_current_bank()
        current_bank.play_clip(position, self.music_logic.repeat_style)

    def start(self):
        pygame.display.init()
        screen = pygame.display.set_mode((1,1))

        body = tkinter.Tk()
        body.title("SoundFloored")

        bank_frame = tkinter.Frame()
        bank_frame.pack(fill=tkinter.BOTH)

        button_dec_bank = tkinter.Button(bank_frame, text="<- Bank", command=self.music_logic.decrement_bank)
        button_dec_bank.pack(side=tkinter.LEFT, expand=True, fill=tkinter.BOTH)

        button_inc_bank = tkinter.Button(bank_frame, text="Bank ->", command=self.music_logic.increment_bank)
        button_inc_bank.pack(side=tkinter.LEFT, expand=True, fill=tkinter.BOTH)

        bank_frame.pack(expand=True, fill=tkinter.BOTH)

        repeat_style_frame = tkinter.Frame()
        repeat_style_frame.pack(expand=True, fill=tkinter.BOTH)

        button_move_previous_repeat_style = tkinter.Button(repeat_style_frame, text="<- Repeat Style", command=self.music_logic.move_previous_repeat_style)
        button_move_previous_repeat_style.pack(side=tkinter.LEFT, expand=True, fill=tkinter.BOTH)
        button_move_next_repeat_style = tkinter.Button(repeat_style_frame, text="Repeat Style ->", command=self.music_logic.move_next_repeat_style)
        button_move_next_repeat_style.pack(side=tkinter.LEFT, expand=True, fill=tkinter.BOTH)
        

        audio_clip_button_frame = tkinter.Frame()
        audio_clip_button_frame.pack(expand=True, fill=tkinter.BOTH)
        
        audio_clip_buttons = []

        for position in range(len(self.music_logic.get_current_bank().clips)):
            button = tkinter.Button(audio_clip_button_frame, text=str(position), command=partial(self.get_and_play_clip, position))
            button.pack(side=tkinter.LEFT, expand=True, fill=tkinter.BOTH)
            audio_clip_buttons.append(button)

        body.mainloop()
