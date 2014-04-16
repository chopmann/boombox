#!/usr/bin/python

import time
import glob
import RPi.GPIO as GPIO
import BoomBox_Buttons as BTNS
import BoomBox_LCD as LCD
from pygame import mixer
from os import walk
from os import system

GPIO.setwarnings(False)

MUSIC_DIR='/home/pi/Music/'


def main():
  GPIO_init()
  GPIO.add_event_detect(BTNS.PLAY, GPIO.FALLING, callback=play, bouncetime=300)
  GPIO.add_event_detect(BTNS.STOP, GPIO.FALLING, callback=stop, bouncetime=300)
  try:
    print "Starting Program"
    while True:
      time.sleep(1)
  except KeyboardInterrupt:  
    GPIO.cleanup()       # clean up GPIO on CTRL+C exit 

# Callbacks
def play(channel):
  print "play callback"
def stop(channel):
  print "stop callback"
def menu(channel):
  print "menu callback"
def fwd(channel):
  print "fwd callback"
def rew(channel):
  print "rew callback"
def vol_up(channel):
  print "vol_up callback"
def vol_down(channel):
  print "vol_down callback"

# TODO: Put All of this on it's own Class!
def GPIO_init():
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(LCD.E, GPIO.OUT)
  GPIO.setup(LCD.RS, GPIO.OUT)
  GPIO.setup(LCD.D4, GPIO.OUT)
  GPIO.setup(LCD.D5, GPIO.OUT)
  GPIO.setup(LCD.D6, GPIO.OUT)
  GPIO.setup(LCD.D7, GPIO.OUT)
  GPIO.setup(BTNS.PLAY    , GPIO.IN, pull_up_down=GPIO.PUD_UP)
  GPIO.setup(BTNS.STOP    , GPIO.IN, pull_up_down=GPIO.PUD_UP)
  GPIO.setup(BTNS.REW     , GPIO.IN, pull_up_down=GPIO.PUD_UP)
  GPIO.setup(BTNS.FWD     , GPIO.IN, pull_up_down=GPIO.PUD_UP)
  GPIO.setup(BTNS.VOL_UP  , GPIO.IN, pull_up_down=GPIO.PUD_UP)
  GPIO.setup(BTNS.VOL_DOWN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  GPIO.setup(BTNS.MENU    , GPIO.IN, pull_up_down=GPIO.PUD_UP)

def lcd_init():
  # Initialise display
  lcd_byte(0x33,LCD_CMD)
  lcd_byte(0x32,LCD_CMD)
  lcd_byte(0x28,LCD_CMD)
  lcd_byte(0x0C,LCD_CMD)
  lcd_byte(0x06,LCD_CMD)
  lcd_byte(0x01,LCD_CMD)

def lcd_string(message):
  # Send string to display
  message = message.ljust(LCD_WIDTH," ")
  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)

def lcd_byte(bits, mode):

  # Send byte to data pins
  # bits = data
  # mode = True  for character
  #        False for command
          
  GPIO.output(LCD_RS, mode) # RS

  # High bits

  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x10==0x10:
    GPIO.output(LCD_D4, True)
  if bits&0x20==0x20:
    GPIO.output(LCD_D5, True)
  if bits&0x40==0x40:
    GPIO.output(LCD_D6, True)
  if bits&0x80==0x80:
    GPIO.output(LCD_D7, True)

  # Toggle 'Enable' pin
  time.sleep(E_DELAY)
  GPIO.output(LCD_E, True)
  time.sleep(E_PULSE)
  GPIO.output(LCD_E, False)
  time.sleep(E_DELAY)

  # Low bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x01==0x01:
    GPIO.output(LCD_D4, True)
  if bits&0x02==0x02:
    GPIO.output(LCD_D5, True)
  if bits&0x04==0x04:
    GPIO.output(LCD_D6, True)
  if bits&0x08==0x08:
    GPIO.output(LCD_D7, True)

  # Toggle 'Enable' pin
  time.sleep(E_DELAY)
  GPIO.output(LCD_E, True)
  time.sleep(E_PULSE)
  GPIO.output(LCD_E, False)
  time.sleep(E_DELAY)
# END TODO
if __name__ == '__main__':
  main()
GPIO.cleanup()