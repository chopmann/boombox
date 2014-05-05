#!/usr/bin/python

import time
import RPi.GPIO as GPIO
import BoomBox_Keypad
import BoomBox_LCD
import pygame


class Player:
    def __init__(self):
        GPIO.setwarnings(False)
        self.menu_mode = False
        keypad = BoomBox_Keypad.Keypad(GPIO)
        self.display = BoomBox_LCD.LCD(GPIO=GPIO)
        GPIO.add_event_detect(keypad.PLAY, GPIO.FALLING, callback=self.play, bouncetime=300)
        GPIO.add_event_detect(keypad.STOP, GPIO.FALLING, callback=self.stop, bouncetime=300)
        GPIO.add_event_detect(keypad.MENU, GPIO.FALLING, callback=self.menu, bouncetime=300)
        GPIO.add_event_detect(keypad.FWD, GPIO.FALLING, callback=self.fwd, bouncetime=300)
        GPIO.add_event_detect(keypad.REW, GPIO.FALLING, callback=self.rew, bouncetime=300)
        GPIO.add_event_detect(keypad.VOL_UP, GPIO.FALLING, callback=self.vol_up, bouncetime=300)
        GPIO.add_event_detect(keypad.VOL_DOWN, GPIO.FALLING, callback=self.vol_down, bouncetime=300)
        try:
            self.display.message("Starting Program")
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            GPIO.cleanup()  # clean up GPIO on CTRL+C exit

    # Callbacks
    def play(self, channel):
        self.display.message("play callback")
        if not self.menu_mode:
            self.display.message("Normal Mode: Play/Pause")
        else:
            self.display.message("Menu Mode: Select/Enter")

    def stop(self, channel):
        self.display.message("stop callback")
        if not self.menu_mode:
            self.display.message("Normal Mode: Stop")
        else:
            self.display.message("Menu Mode: ?")

    def menu(self, channel):
        self.display.message("menu callback")
        if not self.menu_mode:
            self.display.message("Normal Mode: Enter Menu")
            self.menu_mode = True
        else:
            self.display.message("Menu Mode: Exit Menu")
            self.menu_mode = False

    def fwd(self, channel):
        self.display.message("fwd callback")
        if not self.menu_mode:
            self.display.message("Normal Mode: Next Song")
        else:
            self.display.message("Menu Mode: Navigation Down")

    def rew(self, channel):
        self.display.message("rew callback")
        if not self.menu_mode:
            self.display.message("Normal Mode: Previous Song")
        else:
            self.display.message("Menu Mode: Navigation Up")

    def vol_up(self, channel):
        self.display.message("vol_up callback")
        if not self.menu_mode:
            self.display.message("Normal Mode: Volume Up")
        else:
            self.display.message("Menu Mode: --")

    def vol_down(self, channel):
        self.display.message("vol_down callback")
        if not self.menu_mode:
            self.display.message("Normal Mode: Volume Up")
        else:
            self.display.message("Menu Mode: ?")

if __name__ == '__main__':
    Player()
