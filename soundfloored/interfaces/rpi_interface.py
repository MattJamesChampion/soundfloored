import pygame
import RPi.GPIO as GPIO
from functools import partial
import time
import os
import signal
from RPLCD.gpio import CharLCD

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

# If the button is connected to a GPIO pin and ground, the corresponding value when the
# button is pressed is False. If the button is connected to 3.3v, the value will be True.
BUTTONS_CONNECTED_TO_GROUND = True
INPUT_VALUE_WHEN_BUTTON_PRESSED = not BUTTONS_CONNECTED_TO_GROUND
SCREEN_COLUMNS = 16
SCREEN_ROWS = 2

class RpiInterface:
    def __init__(self, music_logic):
        self.music_logic = music_logic

    def write_to_screen(self, text, line=None):
        written_characters = 0
        total_available_characters = 0
        
        if line in range(SCREEN_ROWS):
            total_available_characters = SCREEN_COLUMNS
            self._lcd.cursor_pos = (line, 0)
        elif line is None:
            total_available_characters = SCREEN_COLUMNS * SCREEN_ROWS
            self._lcd.home()
        else:
            raise AttributeError(f"line must be between 0 and {SCREEN_COLUMNS}")

        trimmed_text = text[:total_available_characters]
        self._lcd.write_string(trimmed_text)
        
    def clear_screen(self):
        self._lcd.clear()

    def start(self):
        os.putenv('SDL_VIDEODRIVER', 'fbcon')
        pygame.display.init()

        GPIO.setmode(GPIO.BCM)
        self._lcd = CharLCD(pin_rs=7,
                      pin_e=8,
                      pins_data=[25, 24, 23, 18],
                      numbering_mode=GPIO.BCM,
                      cols=SCREEN_COLUMNS,
                      rows=SCREEN_ROWS)
        self._lcd.clear()
        self._lcd.write_string('Welcome to\r\nSoundFloored')

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
            for index, audio_clip_button_pin in enumerate(audio_clip_button_pins):
                if GPIO.input(audio_clip_button_pin) == INPUT_VALUE_WHEN_BUTTON_PRESSED:
                    # Sleep for just long enough to give the event detector a chance to
                    # execute the callback, rather than stacking multiple calls
                    # to play_clip at the same time
                    time.sleep(0.01)
                    self.music_logic.play_clip(index, is_distinct_trigger=False)
                    
