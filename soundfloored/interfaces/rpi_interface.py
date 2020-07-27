import pygame
import RPi.GPIO as GPIO
from functools import partial

class RpiInterface:
    def __init__(self, music_logic):
        self.music_logic = music_logic

    def start(self):
        pygame.display.init()
        screen = pygame.display.set_mode((1,1))
        
        GPIO.setmode(GPIO.BCM)

        audio_clip_button_pins = [19, 13, 6, 5]

        for index, audio_clip_button_pin in enumerate(audio_clip_button_pins):
            GPIO.setup(audio_clip_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.add_event_detect(audio_clip_button_pin, GPIO.FALLING, callback=partial(self.music_logic.play_clip, index))    
        
        while True:
            pass
