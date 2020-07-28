import pygame
import RPi.GPIO as GPIO
from functools import partial
import os
import signal

# Used to resolve an issue when starting the RpiInterface from systemd where the service would
# receive a SIGHUP upon pygame.init() (or in this case pygame.display.init())
# https://stackoverflow.com/q/39198961
def handler(signum, frame):
    pass

try:
    signal.signal(signal.SIGHUP, handler)
except AttributeError:
    # Windows compatibility
    pass

class RpiInterface:
    def __init__(self, music_logic):
        self.music_logic = music_logic

    def start(self):
        os.putenv('SDL_VIDEODRIVER', 'fbcon')
        pygame.display.init()

        GPIO.setmode(GPIO.BCM)

        control_button_1_pin = 21
        control_button_2_pin = 20

        GPIO.setup(control_button_1_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(control_button_1_pin, GPIO.FALLING, callback=lambda channel: self.music_logic.decrement_bank(), bouncetime=200)
        GPIO.setup(control_button_2_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(control_button_2_pin, GPIO.FALLING, callback=lambda channel: self.music_logic.increment_bank(), bouncetime=200)

        audio_clip_button_pins = [19, 13, 6, 5]

        # Used to discard the channel value that is automatically provided by
        # add_event_detect to the callback function
        callback_wrapper = lambda index, channel: self.music_logic.play_clip(index)

        for index, audio_clip_button_pin in enumerate(audio_clip_button_pins):
            GPIO.setup(audio_clip_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.add_event_detect(audio_clip_button_pin, GPIO.FALLING, callback=partial(callback_wrapper, index), bouncetime=200)
        
        while True:
            pass
