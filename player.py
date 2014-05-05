#!/usr/bin/python

import time
import RPi.GPIO as GPIO
import BoomBox_Keypad
import BoomBox_LCD
import pygame
import os


class Player:
    def __init__(self):
        GPIO.setwarnings(False)
        self.menu_mode = False
        keypad = BoomBox_Keypad.Keypad(GPIO)
        self.display = BoomBox_LCD.LCD(GPIO=GPIO)
        GPIO.add_event_detect(keypad.PLAY, GPIO.FALLING, callback=self.play_callback, bouncetime=300)
        GPIO.add_event_detect(keypad.STOP, GPIO.FALLING, callback=self.stop_callback, bouncetime=300)
        GPIO.add_event_detect(keypad.MENU, GPIO.FALLING, callback=self.menu_callback, bouncetime=300)
        GPIO.add_event_detect(keypad.FWD, GPIO.FALLING, callback=self.fwd_callback, bouncetime=300)
        GPIO.add_event_detect(keypad.REW, GPIO.FALLING, callback=self.rew_callback, bouncetime=300)
        GPIO.add_event_detect(keypad.VOL_UP, GPIO.FALLING, callback=self.vol_up, bouncetime=300)
        GPIO.add_event_detect(keypad.VOL_DOWN, GPIO.FALLING, callback=self.vol_down, bouncetime=300)
        # Init Music Player
        pygame.init()
        # set up the mixer
        freq = 44100     # audio CD quality
        bitsize = -16    # unsigned 16 bit
        channels = 2     # 1 is mono, 2 is stereo
        buffer = 1024    # number of samples (experiment to get right sound)
        pygame.mixer.init(freq, bitsize, channels, buffer)
        pygame.mixer.music.set_volume(0.5)
        self.paused = False
        self.root_dir = "/home/pi/Music"
        self.playlist = self.something(self.root_dir)
        self.pl_index = 0
        try:
            self.display.message("Starting Program")
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            GPIO.cleanup()  # clean up GPIO on CTRL+C exit

    def play(self):
        song = self.playlist[self.pl_index]
        pygame.mixer.music.load(song)
        pygame.mixer.music.play()
        self.display.message(song)
        self.paused = False

    def something(self, path):
        menu_list = []
        for (dirpath, dirnames, filenames) in os.walk(path):
            #dirnames.sort()
            #menu_list.append(dirnames)
            for f in filenames:
                if f[-4:] == ".mp3":
                    menu_list.append(os.path.join(path, f))
            break
        for i in menu_list:
            self.display.message(i)
        return menu_list


    # Callbacks
    def play_callback(self, channel):
        self.display.message("play callback")
        if not self.menu_mode:
            self.display.message("Normal Mode: Play/Pause")
            if pygame.mixer.music.get_busy():
                if not self.paused:
                    self.display.message("Pause")
                    pygame.mixer.music.pause()
                    self.paused = True
                else:
                    self.display.message("Unpause")
                    pygame.mixer.music.unpause()
                    self.paused = False
            else:
                self.display.message("Playing")
                self.play()

        else:
            self.display.message("Menu Mode: Select/Enter")

    def stop_callback(self, channel):
        self.display.message("stop callback")
        if not self.menu_mode:
            self.display.message("Normal Mode: Stop")
            pygame.mixer.music.stop()
        else:
            self.display.message("Menu Mode: Queue Item")

    def menu_callback(self, channel):
        self.display.message("menu callback")
        if not self.menu_mode:
            self.display.message("Normal Mode: Enter Menu")
            self.menu_mode = True
        else:
            self.display.message("Menu Mode: Exit Menu")
            self.menu_mode = False

    def fwd_callback(self, channel):
        self.display.message("fwd callback")
        if not self.menu_mode:
            self.display.message("Normal Mode: Next Song")
            next_song = self.pl_index + 1
            if next_song >= len(self.playlist):
                self.pl_index = 0
            else:
                self.pl_index = next_song
            pygame.mixer.music.stop()
            self.play()
        else:
            self.display.message("Menu Mode: Navigation Down")

    def rew_callback(self, channel):
        self.display.message("rew callback")
        if not self.menu_mode:
            self.display.message("Normal Mode: Previous Song")
            prev_song = self.pl_index + 1
            if prev_song < 0:
                self.pl_index = len(self.playlist) - 1
            else:
                self.pl_index = prev_song
            pygame.mixer.music.stop()
            self.play()
        else:
            self.display.message("Menu Mode: Navigation Up")

    def vol_up(self, channel):
        self.display.message("vol_up callback")
        if not self.menu_mode:
            vol = pygame.mixer.music.get_volume()
            self.display.message("Normal Mode: Volume Up "+str(vol))
            pygame.mixer.music.set_volume(vol + 0.0625)
        else:
            self.display.message("Menu Mode: --")

    def vol_down(self, channel):
        self.display.message("vol_down callback")
        if not self.menu_mode:
            vol = pygame.mixer.music.get_volume()
            self.display.message("Normal Mode: Volume Down "+str(vol))
            pygame.mixer.music.set_volume(vol - 0.0625)
        else:
            self.display.message("Menu Mode: ---")

if __name__ == '__main__':
    Player()
