# BCM Layout
LCD_RS   = 18
LCD_E    = 23
LCD_D4   = 24 
LCD_D5   = 25
LCD_D6   = 08
LCD_D7   = 07
# Define some device constants
LCD_WIDTH = 16    # Maximum characters per line
LCD_CHR = True
LCD_CMD = False

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line 

# Timing constants
E_PULSE = 0.00005
E_DELAY = 0.00005