import pygame
import tkinter
from functools import partial
from ..music_logic import RepeatStyle

class GuiInterface:
    def __init__(self, music_logic):
        self.music_logic = music_logic

    def start(self):
        pygame.display.init()
        screen = pygame.display.set_mode((1,1))

        body = tkinter.Tk()
        body.title("SoundFloored")
        body.geometry("500x200")

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

        number_of_audio_clip_buttons = 4

        for position in range(number_of_audio_clip_buttons):
            button = tkinter.Button(audio_clip_button_frame, text=str(position), command=partial(self.music_logic.play_clip, position))
            button.pack(side=tkinter.LEFT, expand=True, fill=tkinter.BOTH)
            audio_clip_buttons.append(button)

        body.mainloop()
