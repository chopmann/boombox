#First things first:
#RPi.GPIO:
# wget http://raspberry-gpio-python.googlecode.com/files/python-rpi.gpio_0.3.1a-1_armhf.deb
# sudo dpkg -i python-rpi.gpio_0.3.1a-1_armhf.deb
#mutagen:
# wget https://pypi.python.org/packages/source/s/setuptools/setuptools-1.1.1.tar.gz
# tar -zxvf setuptools-1.1.1.tar.gz
# cd ~/setuptools-1.1.1
# sudo python setup.py install
# sudo apt-get install mercurial
# hg clone https://code.google.com/p/mutagen
# cd ~/mutagen
# sudo python setup.py install
#import
import RPi.GPIO as GPIO
import time
import pygame
from os import walk
from os import system
import glob
from mutagen.id3 import ID3
GPIO.cleanup()
GPIO.setwarnings(False)
# Define GPIO to LCD mapping
LCD_RS   = 12
LCD_E    = 16
LCD_D4   = 18 
LCD_D5   = 22
LCD_D6   = 24
LCD_D7   = 26
# Buttons
PLAY     = 11
STOP     = 7
REW      = 15
FWD      = 3 
MENU     = 13
VOL_UP   = 19
VOL_DOWN = 21
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
  GPIO_init()
  # Initialise display
  lcd_init()
  # Initialise path
  path=MUSIC_DIR
  ############################################### menu arrays initializing
  menu_items=get_menu_items(path) #what will be shown on the LCD screen when in menu
  # dirs
  dirs=get_dirs(path)
  # files
  files=get_files(path)
  # filesnames
  filesnames=get_filesnames(path)
################################################## End Menu Arrays
# First Screen
  lcd_byte(LCD_LINE_1, LCD_CMD)
  lcd_string("")
  lcd_byte(LCD_LINE_1, LCD_CMD)
  lcd_string("Welcome")
  lcd_byte(LCD_LINE_2, LCD_CMD)
  lcd_string("")
  # Initialise pygame.mixer and pygame
  pygame.mixer.init()
  pygame.init()
  # Sets the event that is outputted if a song naturally ends. 
  # In this case it doesnt matter which event is outputted, 
  # because the program just looks if there is any event at all
  pygame.mixer.music.set_endevent(1)
  time.sleep(0.5)
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
  Vol_up_pressed  =False
  Vol_down_pressed=False
  Play_input=False 
  Stop_input=False
  Rew_input =False
  Fwd_input =False
  Menu_input=False
  Vol_up_input  =False
  Vol_down_input=False
  # Control varabels for correct displaying of strings
  New_string=True
  String_showtime=time.time()
  Char_counter=0
  songs_playing=[]
  song_display=[]
  New_playing=False
  # Array counters
  menu_counter=0
  dir_counter =0
  file_counter=0
  song_counter=0
  # setting Volume
  pygame.mixer.music.set_volume(0.3)
  #####################################While Start
  while True:
    # gets the input of every button (True or False)
    Play_input = button_input(PLAY)
    Stop_input = button_input(STOP)
    Rew_input  = button_input(REW)
    Fwd_input  = button_input(FWD)
    Menu_input = button_input(MENU)
    Vol_up_input   = button_input(VOL_UP)
    Vol_down_input = button_input(VOL_DOWN)
    # End Program button:
    if (Fwd_input and Play_input and Rew_input and not Rew_pressed):
      lcd_byte(LCD_LINE_1,LCD_CMD)
      lcd_string('')
      lcd_byte(LCD_LINE_2,LCD_CMD)
      lcd_string('')
      break
    if (Play_input and Stop_input and Menu_input and not Play_pressed):
      system("init 0")
      break
    if (menu):
      lcd_byte(LCD_LINE_2,LCD_CMD)
      lcd_string('Menu')
      # Play
      if (not Play_pressed and Play_input):
	print ('Play')
	# if a file is selected the file will be played
	if (menu_items[menu_counter]==files[file_counter]):
	  playing=True
          paused=False
	  menu=False
	  lcd_byte(LCD_LINE_2, LCD_CMD)
	  lcd_string('')
	  songs_playing=[]
	  song_display=[]
	  for i in range(len(files)):
	    songs_playing.append(path+filesnames[i])
            song_display.append(files[i])
	  song_counter=file_counter
	  pygame.mixer.music.load(songs_playing[song_counter])
	  pygame.mixer.music.play()
	# Dir selected#############
        elif (menu_items[menu_counter][1:]==dirs[dir_counter] or (menu_items[menu_counter]=='..' and path != MUSIC_DIR)):
	  # Change path
	  if menu_items[menu_counter]=='..' and path!=MUSIC_DIR:
	    path=path.rsplit('/',2)[0]+'/'
	  else:
	    path=path+dirs[dir_counter]+'/'
	  print path
	  # same as the initial filling of menu_items, dirs, files and filesnames in line 77 to 145
          menu_items=get_menu_items(path)
	  # dirs
	  dirs=get_dirs(path)
	  # files
	  files=get_files(path)
	  # filesnames
	  filesnames=get_filesnames(path)
	  New_string=True
	  menu_counter=0
	  dir_counter =0
	  file_counter=0
      # Stop aka Back button
      if (not Stop_pressed and Stop_input):
	print('Stop')
	if path!=MUSIC_DIR:
	# Change path
	  path=path.rsplit('/',2)[0]+'/'
	  print path
	  # menu_items
	  menu_items=get_menu_items(path)
          # dirs
	  dirs=get_dirs(path)
	  # files
	  files=get_files(path)
	  # filesnames
	  filesnames=get_filesnames(path)
	  New_string=True
	  menu_counter=0
	  dir_counter =0
	  file_counter=0
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
	  paused=False
	  pygame.mixer.music.unpause()
	elif (not playing and not paused and filesnames[file_counter]!='.'):
	  playing=True
	  songs_playing=[]
	  song_display=[]
	  for i in range(len(files)):
	    songs_playing.append(path+filesnames[i])
            song_display.append(files[i])
	  song_counter=file_counter
	  pygame.mixer.music.load(songs_playing[song_counter])
	  pygame.mixer.music.play()
      # Stop
      if (not Stop_pressed and Stop_input):
	print ('Stop')
        playing=False
	paused=False
	menu=True
	New_string=True
	songs_playing=[]
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
      if (not menu and playing):
	if (song_counter == 0):
	  song_counter=len(songs_playing) -1
	else:
	  song_counter=song_counter-1
	pygame.mixer.music.load(songs_playing[song_counter])
	pygame.mixer.music.play()
	New_playing=True
      else:
	if (menu_counter==0):
          menu_counter=len(menu_items)-1
          dir_counter =len(dirs)-1
          file_counter=len(files)-1
        else:
          menu_counter=menu_counter-1
	  if (dir_counter!=0 and menu_items[menu_counter][1:]==dirs[dir_counter-1]):
            dir_counter=dir_counter-1
          elif (file_counter!=0 and menu_items[menu_counter]==files[file_counter-1]):
            file_counter=file_counter-1
        New_string=True
    # Next
    if (not Fwd_pressed and Fwd_input):
      print('Fwd')
      if (not menu and playing):
	if (song_counter == len(songs_playing)-1):
	  song_counter=0
	else:
	  song_counter=song_counter+1
	pygame.mixer.music.load(songs_playing[song_counter])
	pygame.mixer.music.play()
	New_playing=True
      else:
        if (menu_counter==len(menu_items)-1):
	  menu_counter=0
	  dir_counter =0
	  file_counter=0
        else:
	  menu_counter=menu_counter+1
	  if (dir_counter!=len(dirs)-1 and menu_items[menu_counter][1:]==dirs[dir_counter+1]):
	    dir_counter=dir_counter+1
	  elif (file_counter!=len(files)-1 and menu_items[menu_counter]==files[file_counter+1]):
	    file_counter=file_counter+1
        New_string=True
    # Volume up
    if (not Vol_up_pressed and Vol_up_input):
      print 'Vol up'
      if pygame.mixer.music.get_volume()+0.05<=1:
        pygame.mixer.music.set_volume(pygame.mixer.music.get_volume()+0.05)
      else: pygame.mixer.music.set_volume(1)
    # Volume down
    if (not Vol_down_pressed and Vol_down_input):
      print 'Vol down'
      if pygame.mixer.music.get_volume()-0.05>=0:
	pygame.mixer.music.set_volume(pygame.mixer.music.get_volume()-0.05)
      else: pygame.mixer.music.set_volume(0)
    # Displaying of all Strings:    
    if (New_string):
      lcd_byte(LCD_LINE_1,LCD_CMD)
      lcd_string(menu_items[menu_counter])
      String_showtime =time.time()+1
      Char_counter=0
      New_string=False
    elif(menu or (not menu and not playing)):
      if (time.time()-String_showtime>0.3 and Char_counter<=len(menu_items[menu_counter])-16):
        String_showtime=time.time()
        lcd_byte(LCD_LINE_1,LCD_CMD)
        lcd_string(menu_items[menu_counter][Char_counter:])
        Char_counter=Char_counter+1
        if (Char_counter==1):
          String_showtime=time.time()+1
        if (Char_counter>len(menu_items[menu_counter])-16):
 	  Char_counter=0
	  String_showtime=time.time()+0.5
    if (playing and New_playing and not menu):
      lcd_byte(LCD_LINE_1,LCD_CMD)
      lcd_string(song_display[song_counter])
      String_showtime =time.time()+1
      Char_counter=0
      New_playing=False
      print song_display[song_counter]
    elif(not menu and playing):
      if (time.time()-String_showtime>0.3 and Char_counter<=len(song_display[song_counter])-16):
        String_showtime=time.time()
        lcd_byte(LCD_LINE_1,LCD_CMD)
        lcd_string(song_display[song_counter][Char_counter:])
        Char_counter=Char_counter+1
        if (Char_counter==1):
          String_showtime=time.time()+1
        if (Char_counter>len(song_display[song_counter])-16):
          Char_counter=0
          String_showtime=time.time()+0.5
    if len(pygame.event.get())!=0:
      if song_counter==len(songs_playing)-1:
        song_counter=0
      else:
        song_counter=song_counter + 1
      print song_counter
      pygame.mixer.music.load(songs_playing[song_counter])
      pygame.mixer.music.play()
      New_playing=True

    Play_pressed=Play_input
    Stop_pressed=Stop_input
    Rew_pressed =Rew_input
    Fwd_pressed =Fwd_input
    Menu_pressed=Menu_input
    Vol_up_pressed=Vol_up_input
    Vol_down_pressed=Vol_down_input
    time.sleep(0.05)
 ############################While End
###################################End main####################################### 
def button_input(button):
  if button==3:
    return not GPIO.input(button)
  else:
    return GPIO.input(button)

def get_menu_items(path):
  menu_items=[] #what will be shown on the LCD screen when in menu
  menu_items=sorted(glob.glob(path+'*')) #gets everything out of the directory specified by path
  change=[]#array needed for cleaning up other arrays
  if menu_items!=[]:
    for i in range(len(menu_items)):
      menu_items[i]=menu_items[i][len(path):] #delets the path from every item
      if '.' in menu_items[i]:
        if menu_items[i].rsplit('.',1)[1]!='mp3': 
          change.append(i) #puts every file which doesnt end with .mp3 in the change array to be deleted later
        else:
	  menu_items[i]=get_metadata(menu_items[i],path)
      else:
        menu_items[i]='>'+menu_items[i] # puts a > in front of every directory
  menu_items=clean_array(menu_items,change,'..') #if the directory specified by path is empty it will put the item '..' in the array, so its not empty
  print menu_items
  return menu_items

def get_dirs(path):
  dirs=[]
  # puts all directories in the directory specified by path in the array dirs
  for (dirpath, dirnames, filenames) in walk(path): 
    dirs.extend(dirnames)
    break
  change=[]
  dirs=clean_array(dirs,change,'.')
  dirs=sorted(dirs)
  print dirs
  return dirs

def get_files(path):
  files=[]
  # puts all files in the arrays files and filesnames
  for (dirpath, dirnames, filenames) in walk(path):
    files.extend(filenames)
    break
  files=sorted(files)
  change=[]
  # this for loop has the same function as with menu_items. look above
  for i in range(len(files)):
    if '.' in files[i]:
      if files[i].rsplit('.',1)[1]!='mp3':
        change.append(i)
      else:
	files[i]=get_metadata(files[i],path)
    else:
      change.append(i)
  files=clean_array(files,change,'.')
  print files
  return files

def get_filesnames(path):
  filesnames=[]
  for (dirpath, dirnames, filenames) in walk(path):
    filesnames.extend(filenames)
    break
  filesnames=sorted(filesnames)
  change=[]
  for i in range(len(filesnames)):
    if '.' in filesnames[i]:
      if filesnames[i].rsplit('.',1)[1]!='mp3':
	change.append(i)
    else: 
      change.append(i)
  filesnames=clean_array(filesnames,change,'.')
  print filesnames
  return filesnames

def clean_array(array,change,replace_string):
  for i in range(len(change)):
    array.remove(array[change[i]-i])
  if (array==[]):
    array.append(replace_string)
  return array

def get_metadata(song,path):
  audio=ID3(path+song) #needed to get metadata
  # making the Items look nice
  if (audio.getall('TIT2')!=[] and audio.getall('TPE1')!=[]):
    song=audio.getall('TIT2')[0][0]+' by '+audio.getall('TPE1')[0][0] # if there is a interpret and title it prints both
  elif (audio.getall('TIT2')!=[]):
    song=audio.getall('TIT2')[0][0] # if there is just a title it just print that
  else:
    song=song.rsplit('.',1)[0] # if there is nothing it will print the filename without .mp3
  return song
def GPIO_init():
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
  GPIO.setup(VOL_UP, GPIO.IN)  #
  GPIO.setup(VOL_DOWN, GPIO.IN)#
  GPIO.setup(MENU, GPIO.IN)    # -------------

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
