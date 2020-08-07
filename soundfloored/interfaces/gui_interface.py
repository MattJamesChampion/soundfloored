import pygame
import tkinter
from functools import partial
from ..music_logic import RepeatStyle

class GuiInterface:
    def __init__(self, music_logic):
        self.music_logic = music_logic

    def update_screen(self):
        line_1 = self.music_logic.get_current_bank().name
        line_2 = f"RS: {self.music_logic.repeat_style.name}"

        #Add same limiations as a 2x16 screen
        self.screen_line_1.set(line_1[:16])
        self.screen_line_2.set(line_2[:16])
        self.body.after(10, self.update_screen)

    def start(self):
        pygame.display.init()
        screen = pygame.display.set_mode((1,1))

        self.body = tkinter.Tk()
        self.body.title("SoundFloored")
        self.body.geometry("500x200")

        control_frame = tkinter.Frame()
        control_frame.pack(fill=tkinter.BOTH)

        button_load_banks = tkinter.Button(control_frame, text="Load Banks", command=self.music_logic.load_banks)
        button_load_banks.pack(side=tkinter.LEFT, expand=True, fill=tkinter.BOTH)

        screen_frame = tkinter.Frame()
        screen_frame.pack(fill=tkinter.BOTH)

        self.screen_line_1 = tkinter.StringVar()
        label_screen_line_1 = tkinter.Label(screen_frame, textvariable=self.screen_line_1)
        label_screen_line_1.pack(side=tkinter.TOP, expand=True, fill=tkinter.BOTH)
        self.screen_line_2 = tkinter.StringVar()
        label_screen_line_2 = tkinter.Label(screen_frame, textvariable=self.screen_line_2)
        label_screen_line_2.pack(side=tkinter.TOP, expand=True, fill=tkinter.BOTH)

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

        stop_frame = tkinter.Frame()
        stop_frame.pack(expand=True, fill=tkinter.BOTH)

        button_stop = tkinter.Button(stop_frame, text="Stop", command=self.music_logic.stop_all_clips)
        button_stop.pack(side=tkinter.LEFT, expand=True, fill=tkinter.BOTH)

        self.music_logic.after_state_change_functions.append(self.update_screen)
        self.update_screen()

        self.body.mainloop()
