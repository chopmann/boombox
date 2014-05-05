class Keypad:
    PLAY = 9  # MID
    STOP = 22  # BOT
    REW = 17  # LEFT
    FWD = 10  # RIGHT
    MENU = 27  # TOP
    VOL_UP = 4  # UP
    VOL_DOWN = 2  # DOWN

    def __init__(self, GPIO = None):
        # Emulate the old behavior of using RPi.GPIO if we haven't been given
        # an explicit GPIO interface to use
        if not GPIO:
            import RPi.GPIO as GPIO

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.PLAY, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.STOP, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.REW, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.FWD, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.VOL_UP, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.VOL_DOWN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.MENU, GPIO.IN, pull_up_down=GPIO.PUD_UP)