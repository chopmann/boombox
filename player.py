#First things first:
#RPi.GPIO:
# wget http://raspberry-gpio-python.googlecode.com/files/python-rpi.gpio_0.3.1a-1_armhf.deb
# sudo dpkg -i python-rpi.gpio_0.3.1a-1_armhf.deb
#eyeD3:
#  first get setuptools:
# wget https://pypi.python.org/packages/source/s/setuptools/setuptools-1.1.1.tar.gz
# tar -zxvf setuptools-1.1.1.tar.gz
# cd setuptools-1.1.1
# sudo python setup.py install
#  then get eyeD3:
# wget http://eyed3.nicfit.net/releases/eyeD3-0.7.3.tgz
# tar -zxvf eyeD3-0.7.3.tgz
# cd eyeD3-0.7.3
# sudo python setup.py install
#import
import RPi.GPIO as GPIO
import time
import pygame.mixer
from os import walk
import glob
from mutagen.id3 import ID3
GPIO.cleanup()
GPIO.setwarnings(False)
# Define GPIO to LCD mapping
LCD_RS   = 26
LCD_E    = 24
LCD_D4   = 22 
LCD_D5   = 18
LCD_D6   = 12
LCD_D7   = 10
# Buttons
PLAY     = 3
STOP     = 7
REW      = 13
FWD      = 15
MENU     = 19
Vol_up   = 5
Vol_down = 11
# Define some device constants
LCD_WIDTH = 16    # Maximum characters per line
LCD_CHR = True
LCD_CMD = False

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line 

# Timing constants
E_PULSE = 0.00005
E_DELAY = 0.00005
# Menu variables
MUSIC_DIR='/home/pi/Music/'
####################################Main#########################################
def main():
  # Main program block
  # Initialising GPIO pins
  GPIO.setmode(GPIO.BOARD)     # Use BOARD numbers
  GPIO.setup(LCD_E, GPIO.OUT)  # E
  GPIO.setup(LCD_RS, GPIO.OUT) # RS
  GPIO.setup(LCD_D4, GPIO.OUT) # DB4
  GPIO.setup(LCD_D5, GPIO.OUT) # DB5
  GPIO.setup(LCD_D6, GPIO.OUT) # DB6
  GPIO.setup(LCD_D7, GPIO.OUT) # DB7
  GPIO.setup(PLAY, GPIO.IN)    # ---Buttons---
  GPIO.setup(STOP, GPIO.IN)    #
  GPIO.setup(REW, GPIO.IN)     #
  GPIO.setup(FWD, GPIO.IN)     #
  GPIO.setup(Vol_up, GPIO.IN)  #
  GPIO.setup(Vol_down, GPIO.IN)#
  GPIO.setup(MENU, GPIO.IN)    # -------------
  # Initialise display
  lcd_init()
  # Initialise pygame.mixer
  pygame.mixer.init()
  # get all files from the directory Music
  # and more
  path=MUSIC_DIR
  ############################################### menu arrays initializing
  menu_items=[]
  menu_items=glob.glob(path+'*')
  change=[]
  if menu_items!=[]:
    for i in range(len(menu_items)):
      menu_items[i]=menu_items[i][len(path):]
      if '.' in menu_items[i]:
        if menu_items[i].rsplit('.',1)[1]!='mp3':
          change.append(i)
        else:
	  audio=ID3(path+menu_items[i])
	  if (audio.getall('TIT2')!=[] and audio.getall('TPE1')!=[]):
	    menu_items[i]=audio.getall('TIT2')[0][0]+' by '+audio.getall('TPE1')[0][0]
	  elif (audio.getall('TIT2')!=[]):
	    menu_items[i]=audio.getall('TIT2')[0][0]
	  else:
	    menu_items[i]=menu_items[i].rsplit('.',1)[0]
      else:
        menu_items[i]='>'+menu_items[i]
  for i in range(len(change)):
    menu_items.remove(menu_items[change[i]-i])
  print menu_items
 # dirs
  dirs=[]
  for (dirpath, dirnames, filenames) in walk(path):
    dirs.extend(dirnames)
    break
  if (dirs==[]):
    dirs.extend('.')
  print dirs
  # files
  files=[]
  for (dirpath, dirnames, filenames) in walk(path):
    files.extend(filenames)
    break
  filesnames=[]
  for (dirpath, dirnames, filenames) in walk(path):
    filesnames.extend(filenames)
    break
  change=[]
  for i in range(len(files)):
    if '.' in files[i]:
      if files[i].rsplit('.',1)[1]!='mp3':
        change.append(i)
      else:
	audio=ID3(path+files[i])
	if (audio.getall('TIT2')!=[] and audio.getall('TPE1')!=[]):
	  files[i]=audio.getall('TIT2')[0][0]+' by '+audio.getall('TPE1')[0][0]
	elif (audio.getall('TIT2')!=[]):
	  files[i]=audio.getall('TIT2')[0][0]
	else:
	  files[i]=files[i].rsplit('.',1)[0]
    else:
      change.append(i)
  for i in range(len(change)):
    files.remove(files[change[i]-i])
    filesnames.remove(filesnames[change[i]-i])
  if (files==[]):
    files.extend('.')
    filesnames.extend('.')
  print files
  print filesnames
################################################## End Menu Arrays
# First Screen
  lcd_byte(LCD_LINE_1, LCD_CMD)
  lcd_string("")
  lcd_byte(LCD_LINE_2, LCD_CMD)
  lcd_byte(LCD_LINE_1, LCD_CMD)
  lcd_string("Welcome")
  lcd_byte(LCD_LINE_2, LCD_CMD)
  lcd_string("")
  time.sleep(1)
  lcd_byte(LCD_LINE_2, LCD_CMD)
  lcd_string('Menu')
  # Menu variables
  menu=True
  playing=False
  paused=False
  # Button variables
  Play_pressed=False
  Stop_pressed=False
  Rew_pressed =False
  Fwd_pressed =False
  Menu_pressed=False
  Play_input=False 
  Stop_input=False
  Rew_input =False
  Fwd_input =False
  Menu_input=False
  # Control varabels for correct displaying of strings
  New_string=True
  String_showtime =time.time()
  Char_counter=0
  song_playing=''
  New_playing=False
  # Array counters
  menu_counter=0
  dir_counter =0
  file_counter=0
  # Debug variables
  time1=time.time()
  #####################################While Start
  while True:
    #get_IO()
    Play_input = not GPIO.input(PLAY)
    Stop_input = GPIO.input(STOP)
    Rew_input  = GPIO.input(REW)
    Fwd_input  = GPIO.input(FWD)
    Menu_input = GPIO.input(MENU)    
    # End Program button:
    if (Menu_input and Play_input):
      lcd_byte(LCD_LINE_1,LCD_CMD)
      lcd_string('')
      lcd_byte(LCD_LINE_2,LCD_CMD)
      lcd_string('')
      break

    if (menu):
      lcd_byte(LCD_LINE_2,LCD_CMD)
      lcd_string('Menu')
      # Play
      if (not Play_pressed and Play_input):
	print ('Play')
	if (menu_items[menu_counter]==files[file_counter]):
	  playing=True
          paused=False
	  menu=False
	  lcd_byte(LCD_LINE_2, LCD_CMD)
	  lcd_string('')
	  song_playing=files[file_counter]
	  pygame.mixer.music.load(path + filesnames[file_counter])
	  pygame.mixer.music.play()
	# Dir selected#############
        elif (menu_items[menu_counter][1:]==dirs[dir_counter] or menu_items[menu_counter]=='..'):
	  # Change path
	  if menu_items[menu_counter]=='..':
	    path=path.rsplit('/',2)[0]+'/'
	  else:
	    path=path+dirs[dir_counter]+'/'
	  print path
          menu_items=['..']+glob.glob(path+'*')
	  if path==MUSIC_DIR:
	    menu_items=glob.glob(path+'*')
	  change=[]
          for i in range(len(menu_items)):            
	    if menu_items[i]!='..':
	      menu_items[i]=menu_items[i][len(path):]
	      if '.' in menu_items[i]:
		if menu_items[i].rsplit('.',1)[1]!='mp3':
		  change.append(i)
	        else:
	          audio=ID3(path+menu_items[i])
	          if (audio.getall('TIT2')!=[] and audio.getall('TPE1')!=[]):
	            menu_items[i]=audio.getall('TIT2')[0][0]+' by '+audio.getall('TPE1')[0][0]
	          elif (audio.getall('TIT2')!=[]):
	            menu_items[i]=audio.getall('TIT2')[0][0]
	          else:
	            menu_items[i]=menu_items[i].rsplit('.',1)[0]
	      else:
		menu_items[i]='>'+menu_items[i]
          for i in range(len(change)):
	    menu_items.remove(menu_items[change[i]-i])
          # dirs
	  print menu_items
	  dirs=[]
          for (dirpath, dirnames, filenames) in walk(path):
            dirs.extend(dirnames)
            break
	  if (dirs==[]):
	    dirs.extend('.')
	  print dirs
          # files
	  files=[]
          for (dirpath, dirnames, filenames) in walk(path):
	    files.extend(filenames)
            break
	  filesnames=[]
          for (dirpath, dirnames, filenames) in walk(path):
            filesnames.extend(filenames)
            break
          change=[]
	  for i in range(len(files)):
	    if '.' in files[i]:
	      if files[i].rsplit('.',1)[1]!='mp3':
                change.append(i)
	      else:
	        audio=ID3(path+files[i])
                if (audio.getall('TIT2')!=[] and audio.getall('TPE1')!=[]):
	          files[i]=audio.getall('TIT2')[0][0]+' by '+audio.getall('TPE1')[0][0]
	        elif (audio.getall('TIT2')!=[]):
	          files[i]=audio.getall('TIT2')[0][0]
	        else:
	          files[i]=files[i].rsplit('.',1)[0]
            else:
	      change.append(i)
	  for i in range(len(change)):
	    files.remove(files[change[i]-i])
	    filesnames.remove(filesnames[change[i]-i])
          if (files==[]):
	    files.extend('.')
	    filesnames.extend('.')
	  print files
	  print filesnames
	  New_string=True
	  menu_counter=0
	  dir_counter =0
	  file_counter=0
      # Stop
      if (not Stop_pressed and Stop_input):
        print ('Stop')
	playing=False
	paused=False
        pygame.mixer.music.stop()
      # Menu
      if (not Menu_pressed and Menu_input):
	print ('Menu')
        menu=False
	New_playing=True
	lcd_byte(LCD_LINE_2, LCD_CMD)
	lcd_string('')
    else: #if (menu)
      if (playing and not paused):
        lcd_byte(LCD_LINE_2, LCD_CMD)
	lcd_string('Playing...')
      elif (playing and paused):
        lcd_byte(LCD_LINE_2, LCD_CMD)
	lcd_string('Paused')
      # Play
      if (not Play_pressed and Play_input):
	print('Play')
	if (playing and not paused):
	  paused=True
	  pygame.mixer.music.pause()
	elif (playing and paused):
	  playing=True
	  paused=False
	  pygame.mixer.music.unpause()
	elif (not playing and not paused):
	  playing=True
	  song_playing=files[file_counter]
	  pygame.mixer.music.load(path + filesnames[file_counter])
	  pygame.mixer.music.play()
      # Stop
      if (not Stop_pressed and Stop_input):
	print ('Stop')
        playing=False
	paused=False
	menu=True
	New_string=True
	song_playing=''
	pygame.mixer.music.stop()
      # Menu
      if (not Menu_pressed and Menu_input):
	print('Menu back')
	menu=True
	New_string=True
	lcd_byte(LCD_LINE_2,LCD_CMD)
	lcd_string('Menu')
    # End if (menu)
    # Prev
    if (not Rew_pressed and Rew_input):
      print('Rew')
      print menu
      if (menu_counter==0):
        menu_counter=len(menu_items)-1
        dir_counter =len(dirs)-1
        file_counter=len(files)-1
      else:
        menu_counter=menu_counter-1
        if (dir_counter!=0 and menu_items[menu_counter]==dirs[dir_counter-1]):
          dir_counter=dir_counter-1
        elif (file_counter!=0 and menu_items[menu_counter]==files[file_counter-1]):
          file_counter=file_counter-1
      New_string=True
    # Next
    if (not Fwd_pressed and Fwd_input):
      print('Fwd')
      print menu
      if (menu_counter==len(menu_items)-1):
	menu_counter=0
	dir_counter =0
	file_counter=0
      else:
	menu_counter=menu_counter+1
	if (dir_counter!=len(dirs)-1 and menu_items[menu_counter]==dirs[dir_counter+1]):
	  dir_counter=dir_counter+1
	elif (file_counter!=len(files)-1 and menu_items[menu_counter]==files[file_counter+1]):
	  file_counter=file_counter+1
      New_string=True
     
    if (not menu and ((not Rew_pressed and Rew_input) or (not Fwd_pressed and Fwd_input)) and menu_items[menu_counter]==files[file_counter]):
      song_playing=files[file_counter]
      New_playing=True
      print menu
      pygame.mixer.music.load(path + filesnames[file_counter])
      if(playing):
        pygame.mixer.music.play()
    # Displaying of all Strings:    
    if (New_string):
      lcd_byte(LCD_LINE_1,LCD_CMD)
      lcd_string(menu_items[menu_counter])
      String_showtime =time.time()+1
      Char_counter=0
      New_string=False
    elif(menu or (not menu and not playing)):
      if (time.time()-String_showtime>0.5 and Char_counter<=len(menu_items[menu_counter])-16):
        String_showtime=time.time()
        lcd_byte(LCD_LINE_1,LCD_CMD)
        lcd_string(menu_items[menu_counter][Char_counter:])
        Char_counter=Char_counter+1
        if (Char_counter==1):
          String_showtime=time.time()+1
        if (Char_counter>len(menu_items[menu_counter])-16):
 	  Char_counter=0
	  String_showtime=time.time()+0.5
    if (playing and New_playing):
      lcd_byte(LCD_LINE_1,LCD_CMD)
      lcd_string(song_playing)
      String_showtime =time.time()+1
      char_counter=0
      New_playing=False
      print song_playing
    elif(not menu and playing):
      if (time.time()-String_showtime>0.5 and Char_counter<=len(song_playing)-16):
        String_showtime=time.time()
        lcd_byte(LCD_LINE_1,LCD_CMD)
        lcd_string(song_playing[Char_counter:])
        Char_counter=Char_counter+1
        if (Char_counter==1):
          String_showtime=time.time()+1
        if (Char_counter>len(song_playing)-16):
          Char_counter=0
          String_showtime=time.time()+0.5

    # for Debugging
#    time2=time.time()
#    if (time2-time1>4):
#      print ('--------------')
#      print ('menu ')
#      print (menu)
#      print ('Playing ')
#      print (playing)
#      print ('Paused ')
#      print (paused)
#      print ('--------------')
#      time1=time.time()
    Play_pressed=Play_input
    Stop_pressed=Stop_input
    Rew_pressed =Rew_input
    Fwd_pressed =Fwd_input
    Menu_pressed=Menu_input
    time.sleep(0.05)
 ############################While End
###################################End main####################################### 
def get_IO():
  Play_input = not GPIO.input(PLAY)
  Stop_input = GPIO.input(STOP)
  Rew_input  = GPIO.input(REW)
  Fwd_input  = GPIO.input(FWD)
  Menu_input = GPIO.input(MENU)

def lcd_init():
  # Initialise display
  lcd_byte(0x33,LCD_CMD)
  lcd_byte(0x32,LCD_CMD)
  lcd_byte(0x28,LCD_CMD)
  lcd_byte(0x0C,LCD_CMD)  
  lcd_byte(0x06,LCD_CMD)
  lcd_byte(0x01,LCD_CMD)  
#End lcd_init
def lcd_string(message):
  # Send string to display

  message = message.ljust(LCD_WIDTH," ")  

  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)
#End lcd_string
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
# End lcd_byte
if __name__ == '__main__':
  main()
GPIO.cleanup()
