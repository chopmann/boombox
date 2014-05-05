from time import sleep


class LCD:
    def __init__(self, pin_rs=18, pin_e=23, pins_db=[24, 25, 8, 7], GPIO = None):
    # Emulate the old behavior of using RPi.GPIO if we haven't been given
    # an explicit GPIO interface to use
        if not GPIO:
            import RPi.GPIO as GPIO
        self.GPIO = GPIO
        self.pin_rs = pin_rs
        self.pin_e = pin_e
        self.pins_db = pins_db

        self.GPIO.setmode(GPIO.BCM)
        self.GPIO.setup(self.pin_e, GPIO.OUT)
        self.GPIO.setup(self.pin_rs, GPIO.OUT)

        for pin in self.pins_db:
            self.GPIO.setup(pin, GPIO.OUT)

    def clear(self):
        """ Blank / Reset LCD """
        self.cmd(0x33) # initialization
        self.cmd(0x32) # initialization
        self.cmd(0x28)
        self.cmd(0x0C)
        self.cmd(0x06)
        self.cmd(0x01)

    def cmd(self, bits, char_mode=False):
        """ Send command to LCD """
        sleep(0.001)
        bits = bin(bits)[2:].zfill(8)
        self.GPIO.output(self.pin_rs, char_mode)
        for pin in self.pins_db:
            self.GPIO.output(pin, False)

        for i in range(4):
            if bits[i] == "1":
                self.GPIO.output(self.pins_db[::-1][i], True)
                self.GPIO.output(self.pin_e, True)
                self.GPIO.output(self.pin_e, False)
        for pin in self.pins_db:
            self.GPIO.output(pin, False)
            for i in range(4, 8):
                if bits[i] == "1":
                    self.GPIO.output(self.pins_db[::-1][i-4], True)
                    self.GPIO.output(self.pin_e, True)
                    self.GPIO.output(self.pin_e, False)

    def message(self, text):
        """ Send string to LCD. Newline wraps to second line"""
        print text # for debug
        for char in text:
            if char == '\n':
                self.cmd(0xC0) # next line
            else:
                self.cmd(ord(char), True)
