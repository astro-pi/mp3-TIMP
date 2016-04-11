"""
Tim's Interstellar Music Player (TIM.P)

!!!!!!!!!!!!!!!!!!!!!!!!!IMPORTANT!!!!!!!!!!!!!!!!!!!!!!!!!!!
Before you run please make sure that:
>The variable RESOURCES_PATH corresponds to the folder which holds the resources (This should be a folder called "TIMP data").
>The variable SONG_PATH corresponds to a folder with some MP3 files in it.
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

Note:
TIMP was entirely developed by me (NAME REDACTED) hidden away typing at my computer.
Over many afternoons (and some of the Easter holidays) I developed this program with the hope that Tim Peake will be able to use on the ISS!
You do not have to read the instructions to use the program as prompts are given through the console. The instructions just explain it in detail.
Because there are over 1900 lines I would recommend opening the program in Visual Studio because you can collapse blocks which makes it easier to navigate the file. 
Also if there is a copyright issue with the Red Dwarf theme tune I set as the alarm, it can be changed to another song. It is called Alarm.ogg in the "TIMP data" folder
Finally, when looking through the code please remember that my message() function does not block execution, but uses a separate process to display the scrolling message so it can be cancelled.

Features:
> Easy to use song picker
> Play / Pause / Skip / Replay / Stop buttons
> Main menu and Volume buttons
> Volume control
> Engaging GUI with transitions
> Shuffle setting
> Visualisations! (like screensavers)
> Stats view (this is one of the visualisations) with temperature, pressure and humidity.
> Alarm clock
> Date and time
> Timer
> Daily messages
> Quit button

The following is a detailed guide on how to use the program, it's not as complicated as it looks when you use it :)

CONTROLS:
The Joystick is used to navigate the GUI.
The top button is play/pause
The right button is skip
The left button is replay / rewind
The bottom button is stop
The lower left button activates a volume control on the screen
The lower right button brings the user back to the main menu. If user is already on the main menu it cycles through different 'visualisations' (I will explain this later)

To rewind, press the stop button and then the replay/rewind button

The buttons work at any point in the program so you can play or pause whenever you want

NAVIGATION:
>>>>Main menu
By default the program loads the Main menu which is a note icon with a border. Moving the joystick in any direction opens the settings (see Settings below)
IMPORTANT: If no buttons are pressed for the amount of seconds specified by TIMEOUT then the program will return to the main menu or visualisation.

>Visualisations
The Visualisations are like screensavers. The visualisations either show info about the song or display patterns on the screen.
To cycle through the visualisations press the Main Menu / visualisations button. Note: the button's primary function is to bring the user back to the main menu first.

If the program times out then it goes back to playing whatever visualisation was playing. 
To wake up TIMP, move the joystick in any direction.
visualisations are disabled when no song is playing.

The Visualisations:

>Song -shows the name of the song that is playing.
>Snakes -random pattern with two 'snakes' spiralling into the middle.
>Bars -random pattern that looks like an equaliser.
>Circles -randomly spawns different circles on the screen (I had to use trigonometry and Pythagoras for this)
>Stats -Displays a message showing the temperature, pressure and humidity.

>>>>Settings
The user can scroll through the settings using the joystick left/right. 
Down or Enter (middle button) selects that setting. 
Up goes back to the Main menu.

The settings:

>Pick Song (note icon):
Opens up a GUI that lets the user select a song (see the Pick Song section)

>Volume (speaker with soundwaves icon):
Displays a GUI to let the user change the volume (see the Volume section)

>Shuffle (infinity icon):
Either displays a red 'N' or green 'Y' depending on the current setting.
The user can toggle the setting by pressing left or fight on the joystick.
The middle button chooses the currently displaying letter.

>Date (Clock icon):
Shows the date and then the time

>Timer (321 icon):
Lets the user set a timer. It works like this with the user pressing enter after each one:
1) displays "Minutes Set"
2) The user uses up/down to change the minutes. The screen shows the number.
3) displays "Seconds Set"
4) The user uses up/down to change the seconds. The screen shows the number.
5) displays "Set: 3M 30S" replacing 3 and 30 with the correct values
6) shows a screen which slowly fills in untill the timer is up.
7) Alarm goes off

>Alarm (Bell icon):
Lets the user set an alarm. It works just like the timer but with these steps insted:
1) displays "On/Off"
2) The user uses left/right to toggle between Y/N
3) If the user selected N then it displays "Alarm Off" and goes back to the settings
4) Otherwise it displays "Hours Set"
5) The user uses up/down to change the hours. The screen shows the number.
6) displays "Minutes Set"
7) The user uses up/down to change the minutes. The screen shows the number.
8) displays the set time for the alarm and then goes back to settings

When the time is reached an alarm is set off, this is detected by the Update() function

>Message(? icon):
Displays a daily message, these messages are stored in Messages.txt in the TIMP data folder

>Info (i icon):
Displays a small message

>Quit (X icon):
Ends the program

>>>>Pick Song
This is opened by selecting Pick song from the settings.
Pick song displays a GUI that allows the user to pick a song to play:

    > When it loads the letter 'A' is displayed. Using the joystick up/down the user can scroll through the alphabet. 
    > If the middle key or right is pressed on the joystick then the function will display the name of the song with the matching first letter. 
    > Then using up/down the user can scroll through the songs in alphabetical order.
    > If left is pressed then it will go back to the alphabet.
    > If left is pressed on the alphabet the program returns to the main menu. 
    > When the user finds the song that he/she wants to play they can press right or the middle key to play that song. It will show a play icon and return to the main menu
    > Songs beginning with a non-alphabetic character are under '*' which is above A in the scroll.

>>>>Volume
This is opened by either selecting Volume from the settings or pressing the volume button.
It displays a bar on the screen. left / right on the joystick increases or decreases the length of the bar which represents the volume.
If the bar fills up the whole screen then it is at max volume.
Pressing up or pressing the volume button will close the volume control.

That's it!
"""

###################################### Imports ######################################

from sense_hat import SenseHat
import time
import random
import glob
import datetime
import os
import math
from multiprocessing import Process
import pygame
import threading
from pygame.locals import *

######################################  Variables ######################################

######## SenseHat ########
SENSE = SenseHat()# (static)

######## letters for song selection ########
LETTERS=["*","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]# (static)

######## Audio ########
Songs=[]#holds song names
PlayedSongs=[]#holds played Songs, used for shuffle
Shuffle=False #if true the song order is randomised
PlayingI=-1#the index of 'Songs' that refers to the currently playing song. -1 if no song is playing
Paused=False#is media paused?

######## Volume ########
VolumeIcon=[11,12,10,23,34,43,51,52,50,06,16,26,65,56,66,76,67]#hold the xy co-ordinates of the pixels to overlay on the volume control.

######## Alarm ########
class Alarm:
    Hour=12#24 hour time
    Minute=30
    Set=False#alarm on or off
    Active=False#Used to stop the alarm being constantly set off at the set time

######## Navigation ########
TimeoutDisabled=False#used to disable the timeout (still times out after a minute)
RequestPickSong=False #used to request to the main thread to launch the PickSong GUI
ReturnToMain=False# When true the program returns to the main menu or settings depending on what is currently displaying
Menu="Main" #either Main or Settings, used in main menu loop
SICONS=["Pick","Volume","Shuffle","Date","Timer","Alarm","Message","Info","Quit"]#The settings in the order they will appear (static)
IsVolumeDisplaying=False#True when the volume control is being displayed
Beep=0#will hold the beep sound

######## TimeOut ########
CurrentTimeOut=0#used to count up to TIMEOUT (TIMEOUT is an adjustable variable)
LastTime=datetime.datetime.now()#used to work out the time elapsed

######## current background colour ########
CR=0
CG=0
CB=0

######## song visuals ########
VISUAL_MODES=["Main","Song","Snakes","Bars","Circles","Stats"]# (static)
VMode=0#default mode is Main
RequestUpdateVisuals=False#request to show / update the visuals

#the following are variables needed for each visual
#### visual snakes ####
class VSnakes:
    #positions of two snakes
    x1=0
    x2=7
    y1=0
    y2=7
    #direction of snakes
    d1=0
    d2=2
    #length of a side od a snake
    L1=4
    L2=4
    #colour change amount
    RP=5
    GP=-3
    BP=-2
    #snake colours
    r=30
    g=0
    b=200
    r2=100
    g2=50
    b2=0
    
#### visual bars ####
class VBars:
    #Bar colour (static)
    BR=50
    BG=200
    BB=40
    #Peak colour (the top of the bar) (static)
    PR=250
    PG=40
    PB=40
    #the last position of the bars
    Position=[0,3,5,7,0,2,1,3]

#### visual circles ####
class VCircles:
    Screen=0#holds a screen image (will become an array)
    class C1:#holds the settings for a circle
        #middle of the circle
        x=4
        y=4
        #radius
        ra=2.5
        #colour
        r=30
        g=50
        b=70

######## Message Thread ########
PassMessage="A"#variable to pass message name to threading slave
MPid=0 #message process pid thread (for terminating)

###################################### Adjustible variables ######################################

#time in seconds until the GUI resets to the visuals (static)
TIMEOUT=15
#location of songs (static)
SONG_PATH="/home/pi/Music/"
#location of reasources (static)
RESOURCES_PATH="/home/pi/TIMP data/"
#Shuffle default state
Shuffle=False
#Intro enabled (static)
INTRO_ENABLED=True

###################################### Images ######################################

class Images:

    #### Settings Icons ####

    g=(0,50,0)
    r=(237,28,36)
    b=(136,0,21)

    ImgAlarm=[g,g,g,g,g,g,g,g,
              g,g,g,r,r,g,g,g,
              g,g,r,r,r,r,g,g,
              g,g,r,r,r,r,g,g,
              g,g,r,r,r,r,g,g,
              g,r,r,r,r,r,r,g,
              g,g,g,b,b,g,g,g,
              g,g,g,g,g,g,g,g]

    ImgDate= [g,g,g,r,r,g,g,g,
              g,r,r,g,g,r,r,g,
              g,r,g,b,g,g,r,g,
              r,g,g,b,g,g,g,r,
              r,g,g,g,b,b,g,r,
              g,r,g,g,g,g,r,g,
              g,r,r,g,g,r,r,g,
              g,g,g,r,r,g,g,g]

    ImgInfo= [g,g,g,r,r,g,g,g,
              g,g,g,r,r,g,g,g,
              g,g,g,g,g,g,g,g,
              g,g,g,r,r,g,g,g,
              g,g,g,r,r,g,g,g,
              g,g,g,r,r,g,g,g,
              g,g,g,r,r,g,g,g,
              g,g,g,r,r,g,g,g]
    
    ImgMessage=[g,g,g,r,r,r,g,g,
              g,g,r,g,g,g,r,g,
              g,g,r,g,g,g,r,g,
              g,g,g,g,g,r,g,g,
              g,g,g,g,r,g,g,g,
              g,g,g,g,r,g,g,g,
              g,g,g,g,g,g,g,g,
              g,g,g,g,r,g,g,g]

    ImgPick= [g,g,g,g,g,g,g,g,
              g,g,r,r,r,r,r,g,
              g,g,r,g,g,g,r,g,
              g,g,r,g,g,g,r,g,
              g,g,r,g,g,g,r,g,
              g,r,r,g,g,r,r,g,
              g,r,r,g,g,r,r,g,
              g,g,g,g,g,g,g,g]

    ImgQuit= [g,g,g,g,g,g,g,g,
              g,r,g,g,g,g,r,g,
              g,g,r,g,g,r,g,g,
              g,g,g,r,r,g,g,g,
              g,g,g,r,r,g,g,g,
              g,g,r,g,g,r,g,g,
              g,r,g,g,g,g,r,g,
              g,g,g,g,g,g,g,g]

    ImgShuffle= [g,g,g,g,g,g,g,g,
              g,g,g,g,g,g,g,g,
              g,r,r,g,g,b,b,g,
              r,g,g,r,b,g,g,b,
              b,g,g,b,r,g,g,r,
              g,b,b,g,g,r,r,g,
              g,g,g,g,g,g,g,g,
              g,g,g,g,g,g,g,g]

    o=(255,127,39)
    y=(255,242,0)

    ImgTimer= [g,g,g,g,g,g,g,g,
              g,g,g,g,g,g,g,g,
              r,r,r,o,o,o,g,y,
              g,g,r,g,g,o,g,y,
              r,r,r,o,o,o,g,y,
              g,g,r,o,g,g,g,y,
              r,r,r,o,o,o,g,y,
              g,g,g,g,g,g,g,g]

    ImgVolume= [g,g,g,g,g,b,g,g,
              g,g,g,b,g,g,b,g,
              g,r,g,g,b,g,g,b,
              r,r,g,g,b,g,g,b,
              r,r,g,g,b,g,g,b,
              g,r,g,g,b,g,g,b,
              g,g,g,b,g,g,b,g,
              g,g,g,g,g,b,g,g]

    #### Audio Control Images ####

    p=(50,50,70)
    g=(34,177,76)

    ImgPause= [p,p,p,p,p,p,p,p,
               p,g,g,p,p,g,g,p,
               p,g,g,p,p,g,g,p,
               p,g,g,p,p,g,g,p,
               p,g,g,p,p,g,g,p,
               p,g,g,p,p,g,g,p,
               p,g,g,p,p,g,g,p,
               p,p,p,p,p,p,p,p]

    ImgPlay=  [p,p,p,p,p,p,p,p,
               p,p,g,g,p,p,p,p,
               p,p,g,g,g,p,p,p,
               p,p,g,g,g,g,p,p,
               p,p,g,g,g,p,p,p,
               p,p,g,g,p,p,p,p,
               p,p,p,p,p,p,p,p,
               p,p,p,p,p,p,p,p]

    ImgRewind=[p,p,p,p,p,p,p,p,
               p,p,p,g,p,p,g,p,
               p,p,g,g,p,g,g,p,
               p,g,g,g,g,g,g,p,
               p,g,g,g,g,g,g,p,
               p,p,g,g,p,g,g,p,
               p,p,p,g,p,p,g,p,
               p,p,p,p,p,p,p,p]

    ImgSkip=  [p,p,p,p,p,p,p,p,
               p,g,p,p,g,p,p,p,
               p,g,g,p,g,g,p,p,
               p,g,g,g,g,g,g,p,
               p,g,g,g,g,g,g,p,
               p,g,g,p,g,g,p,p,
               p,g,p,p,g,p,p,p,
               p,p,p,p,p,p,p,p]

    ImgStop=  [p,p,p,p,p,p,p,p,
               p,p,p,p,p,p,p,p,
               p,p,g,g,g,g,p,p,
               p,p,g,g,g,g,p,p,
               p,p,g,g,g,g,p,p,
               p,p,g,g,g,g,p,p,
               p,p,p,p,p,p,p,p,
               p,p,p,p,p,p,p,p]

    #### Other ####

    w=(200,200,200)
    r=(250,0,0)
    g=(0,200,0)

    ImgNo=[r,r,r,r,r,r,r,r,
           r,w,r,r,r,r,w,r,
           r,w,w,r,r,r,w,r,
           r,w,r,w,r,r,w,r,
           r,w,r,r,w,r,w,r,
           r,w,r,r,r,w,w,r,
           r,w,r,r,r,r,w,r,
           r,r,r,r,r,r,r,r]

    ImgYes=[g,g,g,g,g,g,g,g,
            g,w,g,g,g,g,w,g,
            g,w,w,g,g,w,w,g,
            g,g,w,w,w,w,g,g,
            g,g,g,w,w,g,g,g,
            g,g,g,w,w,g,g,g,
            g,g,g,w,w,g,g,g,
            g,g,g,g,g,g,g,g]

    p=(163,73,164)
    g=(0,70,0)
    b=(0,0,100)
    o=(255,127,39)

    ImgMain=[p,g,g,g,g,g,g,p,
             g,b,o,o,o,o,o,g,
             g,b,o,b,b,b,o,g,
             g,b,o,b,b,b,o,g,
             g,b,o,b,b,b,o,g,
             g,o,o,b,b,o,o,g,
             g,o,o,b,b,o,o,g,
             p,g,g,g,g,g,g,p]

###################################### Functions ######################################

######## Update ########
def Update():#Updates and sends back key presses
    """
    The update function should always continually be called from the active GUI loop (ie: Main menu, pick song...).
    It does these things:
    >Plays the next song if the playing song has finished
    >Gets all the key presses and how many times the key has been pressed
    >Plays a beep sound if a key is pressed
    >Responds to the play, stop, skip, rewind, volume and main Menu/Visuals buttons
    >Updates the Time out
    >Times out the program when timeout occurs (Returns to Main menu)
    >Activates the alarm at the correct time

    The function also returns the key pressed, if any, and the number of presses
    """
    global CurrentTimeOut
    global ReturnToMain
    global PlayingI
    global Menu
    global RequestPickSong
    global VMode
    global LastTime
    global RequestUpdateVisuals
    eventN="None"#holds the event name
    presses=0 #holds the number of key presses
    if ((not pygame.mixer.music.get_busy()) and (not PlayingI==-1)):#if the music has ended, load the next track
        SongEnd()
        #### Updates the Song Name visualisation to the new song ####
        if(VISUAL_MODES[VMode]=="Song" and CurrentTimeOut==-1):#Shows the name of the currently playing song
            print("visualisation: Song Name   Pressing any key will wake up TIMP and return to the Main menu")
            CR=50
            CG=20
            CB=0
            message(Songs[PlayingI])
    for event in pygame.event.get():# get events
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                if(not eventN=="DOWN"):
                    presses=0
                presses=presses+1
                eventN="DOWN"
            if event.key == K_LEFT:
                if(not eventN=="UP"):
                    presses=0
                presses=presses+1
                eventN="UP"
            if event.key == K_UP:
                if(not eventN=="RIGHT"):
                    presses=0
                presses=presses+1
                eventN="RIGHT"
            if event.key == K_DOWN:
                if(not eventN=="LEFT"):
                    presses=0
                presses=presses+1
                eventN="LEFT"
            if event.key == K_RETURN:
                if(not eventN=="RETURN"):
                    presses=0
                presses=presses+1
                eventN="RETURN"
            if event.key == K_u:
                if(not eventN=="PLAY"):
                    presses=0
                presses=presses+1
                eventN="PLAY"
            if event.key == K_d:
                if(not eventN=="STOP"):
                    presses=0
                presses=presses+1
                eventN="STOP"
            if event.key == K_l:
                if(not eventN=="REWIND"):
                    presses=0
                presses=presses+1
                eventN="REWIND"
            if event.key == K_r:
                if(not eventN=="SKIP"):
                    presses=0
                presses=presses+1
                eventN="SKIP"
            if event.key == K_a:
                if(not eventN=="VOLUME"):
                    presses=0
                presses=presses+1
                eventN="VOLUME"
            if event.key == K_b:
                if(not eventN=="VISUAL"):
                    presses=0
                presses=presses+1
                eventN="VISUAL"
    #Beep
    if(eventN!="None"):
        Beep.play()
    #media control
    if(eventN=="PLAY"):
        TogglePause()
        ReturnToMain=True
    if(eventN=="STOP"):
        Stop()
        ReturnToMain=True
    if(eventN=="SKIP"):
        Skip()
        ReturnToMain=True
    if(eventN=="REWIND"):
        Rewind()
        ReturnToMain=True
    if(eventN=="VOLUME" and not (IsVolumeDisplaying or CurrentTimeOut==-1)):
        messageKill()
        VolumeChange()#launches the volume control
        ReturnToMain=True
    
    # the 'visual' button firstly goes to the main menu, if it is on the main menu then the visual will change
    if(eventN=="VISUAL"):
        if(CurrentTimeOut==-1):#if already on visulals, request to switch to next one
            VMode=VMode+1
            if (VMode==len(VISUAL_MODES)):
                VMode=0
            RequestUpdateVisuals=True
        else:
            if(Menu=="Main"):#if on main menu load visuals
                RequestUpdateVisuals=True
                if(VMode==0):
                    VMode=1
            else:#if not, just go to the main menu (VMode[0] is the main menu)
                ReturnToMain=True
                RequestUpdateVisuals=True
                VMode=0
    if(not (eventN=="None" or eventN=="VISUAL")):#any key apart from the visualisation key is pressed
        if(CurrentTimeOut==-1 and VMode>0):#awake from visuals
            print("Waking up from visualisation")
            Menu="Main"
            ReturnToMain=True
            eventN="None"#ignore the key that was pressed
        CurrentTimeOut=0#reset TIMEOUT
    if(CurrentTimeOut>TIMEOUT):#TIMEOUT!
        if(TimeoutDisabled):#if timeout is disabled
            if(CurrentTimeOut>60):#if timeout is over a minute, then timeout anyway
                CurrentTimeOut=-1#disable timer
                RequestUpdateVisuals=True#return to visuals
        else:
            CurrentTimeOut=-1#disable timer
            print("TIMEOUT")
            RequestUpdateVisuals=True#return to visuals
    if(not CurrentTimeOut==-1):
        if((datetime.datetime.now()-LastTime)>datetime.timedelta(0,1,0,0,0,0,0)):#increse CurrentTimeOut if it has elapsed 1 second
            LastTime=datetime.datetime.now()#saves the time
            CurrentTimeOut=CurrentTimeOut+1
    if(RequestUpdateVisuals==True):
        Menu="Main"#return to the main menu
        ReturnToMain=True
    #Alarm
    if(Alarm.Set):#if alarm is active
        d=datetime.datetime.now()#get the time now
        if(d.hour==Alarm.Hour and d.minute==Alarm.Minute):#if it is the correct time
            if(not Alarm.Active):#if the alarm is not already going off
                Alarm.Active=True
                AlarmSetoff()#set off alarm
                ReturnToMain=True
        else:
            Alarm.Active=False
    #Return the key presses
    return (eventN,presses)

######## Alarm ########
def AlarmSetoff():#sets off an alarm
    print("Alarm!")
    PlayingI=-1
    pygame.mixer.music.stop()#stops music
    pygame.mixer.music.load(RESOURCES_PATH+"Alarm.ogg")#plays the alarm tune
    pygame.mixer.music.play()
    while(True):#GUI loop
        (key,presses)=Update()#update
        if(key!="None"):#if any key is pressed
            break
        #does some flashing
        transition("RIGHT",250,50,50,0.99)
        transition("RIGHT",150,100,100,0.99)
        transition("RIGHT",250,50,50,0.99)
        transition("RIGHT",0,60,0,0.99)
        #shows the alarm icon
        SENSE.set_pixels(Images.ImgAlarm)
        time.sleep(0.7)
    pygame.mixer.music.stop()#stops the alarm tune
        
######## Audio Control ########
def TogglePause():#play or pause the music
    global RequestPickSong
    global Paused
    messageKill()
    transition("RIGHT",50,50,70,0.99)
    
    if(PlayingI==-1): #if no song is playing
        print("Play")
        SongEnd() #load a song
        Paused=False
        SENSE.set_pixels(Images.ImgPlay)#show play icon
        time.sleep(1)
        transition("RIGHT",0,0,50,0.99)
        return
    if(not Paused):#if a song is not paused
        print("Paused")
        Paused=True
        pygame.mixer.music.pause()#pause the song
        SENSE.set_pixels(Images.ImgPause)#show pause icon
    else:#if a song is paused
        print("Play")
        Paused=False
        pygame.mixer.music.unpause()#resume the song
        SENSE.set_pixels(Images.ImgPlay)#show play icon
    time.sleep(1)
    transition("RIGHT",0,0,50,0.99)

def Stop(): # stop playing music
    global PlayingI
    global Paused
    Paused=False
    print("Stop")
    messageKill()
    PlayingI=-1
    transition("RIGHT",50,50,70,0.99)
    SENSE.set_pixels(Images.ImgStop)#shows the stop icon
    pygame.mixer.music.fadeout(2000)#fades out the music and stops it
    time.sleep(1)
    transition("RIGHT",0,0,50,0.99)

def Skip(): # load the next track
    global Paused
    Paused=False
    messageKill()
    print("Skip")
    transition("RIGHT",50,50,70,0.99)
    SENSE.set_pixels(Images.ImgSkip)#show skip icon
    SongEnd()#this function plays another song
    time.sleep(1)
    transition("RIGHT",0,0,50,0.99)

def Rewind(): # restart the current track or skips back if it is stopped
    global Paused
    global PlayingI
    Paused=False
    messageKill()
    transition("LEFT",50,50,70,0.99)
    SENSE.set_pixels(Images.ImgRewind)#show rewind icon
    if(PlayingI>-1):#if a song is playing
        print("Replaying")
        pygame.mixer.music.play()#restart that song
    else:
        if(PlayingI==-1 and not len(PlayedSongs)<2):#if a song has been previously played
            #fiddles with the list of previously played songs
            PlayedSongs.remove(PlayedSongs[-1])
            PlayingI=PlayedSongs[-1]
            Play(SONG_PATH+Songs[PlayedSongs[-1]]+".mp3",PlayingI)#plays the previous song
            PlayedSongs.remove(PlayedSongs[-1])
            print("Skip Back")
        else:#occurs when there is not previous song to go back to
            print("Not possible to rewind")
    
    time.sleep(1)
    transition("LEFT",0,0,50,0.99)

def SongEnd():# load and play the next song in alphabetical order (random if Shuffle enabled)
    global PlayingI
    global PlayedSongs
    global Paused
    Paused=False
    i=PlayingI#i is the index of the song that has just ended
    PlayingI=-1#sets the playing index to none while choosing a song
    if(Shuffle):
        if(len(PlayedSongs)>len(Songs)-1): # if played all the songs, reset the list of played songs 
            PlayedSongs=[]
        PlayingI=random.randint(0,len(Songs)-1)#pick random song
        while(PlayingI in PlayedSongs):#keep picking random songs until it finds a song that hasn't been played yet
            PlayingI=random.randint(0,len(Songs)-1)
    else:
        PlayingI=i+1#pick the next song in alphabetical order
    if(PlayingI>len(Songs)-1):#if that was the final song, loop back to the beginning
       PlayingI=0
    Play(SONG_PATH+Songs[PlayingI]+".mp3",PlayingI)#finally play the song

def Play(filepath,index):#loads a song from the given filepath and 'Songs' index
    global PlayingI
    global PlayedSongs
    global Paused
    Paused=False
    PlayedSongs.append(index)#add the song to the list of played songs
    if(len(PlayedSongs)>len(Songs)-1): # if played all the songs, reset the list of played songs 
        PlayedSongs=[]
    pygame.mixer.music.load(filepath)#load the song
    pygame.mixer.music.play()#play the song
    print("Now Playing: "+Songs[index])
    PlayingI=index#sets the PlayingI index to the index of the new song
    
######## Tool Functions ########
def message(Message):#uses a separate process to display a looping message that can be interupted
    """
    The message function starts the new process that displays a scrolling message on the screen.
    I needed to use a whole new process so I could interrupt the scrolling message. It would
    be very annoying to have to wait for each message to finish displaying when not necessary,
    e.g. when scrolling through song names.
    MPid stores the Pid of the process so the program can kill the message process later
    """
    global PassMessage
    global MPid
    if(MPid>0):#if it is already displaying a message
        os.system("kill -9 "+str(MPid))#kill the message process
    PassMessage=Message
    p=Process(target=BeginDisplayMessage)#start the new process
    p.start()
    MPid=p.pid#get the pid of the message process

def messageKill():#kills the message display process
    global MPid
    if(MPid>0):#if there is a message displaying
        os.system("kill -9 "+str(MPid))#kill the message process
    MPid=0

def transition(direction,R2,G2,B2,speed):#swaps background colour to another in a certain direction
    """
    The transition function transitions from one background colour to another in a certain direction.
    eg if RIGHT was the chosen direction the function would start by setting all pixels to the old background colour,
    the program then draws a gradient starting on line 'Start' going RIGHT, line by line. Because 'Start' is set to 8
    the program will only display one line of the gradient on the first frame. Each frame start is decreased by
    1, meaning the gradient will slowly go left. The length of the gradient is 'TL' which is set to ten lines.
    Start will eventually become negative meaning the gradient will start part way through on the display. 
    When the end of the gradient is reached while drawing a frame, it will set the other lines to the new background 
    colour. The transition ends when 'Start<-TL'
    """
    messageKill()#kills any message that is being displayed
    #### Checking if the values are in range ####
    if(R2>255):
        R2=255
    if(R2<0):
        R2=0
    if(G2>255):
        G2=255
    if(G2<0):
        G2=0
    if(B2>255):
        B2=255
    if(B2<0):
        B2=0
    ####static variables####
    # current background colours
    global CR
    global CG
    global CB
    TL=10#the length of the gradient in lines
    #the difference between the old and new colours is R2 - CR , G2 - CG ,B2 - CB
    #these are the increse amounts for each colour per line in the gradient
    Rin=(R2-CR)/TL
    Gin=(G2-CG)/TL
    Bin=(B2-CB)/TL
    x=0#x position for drawing pixel by pixel
    y=0#y position for drawing pixel by pixel

    #these are updated every line and are set to the desired colour for that line
    r=CR
    g=CG
    b=CB
    Line=0#the line relative to the start of the gradient
    Start=8#the line from where it starts drawing the gradient, decreases by one each time
    while(not Start<-TL):#each loop of this draws a gradient on the screen 
        while(x<8):#each loop of this draws a line
            if(Start<x):#has it reached the line where it should start drawing the gradient?
                Line=Line+1
                if(Line<TL):#if this line is part of the gradient
                    r=CR+(Rin*Line)#set the colour of the line
                    g=CG+(Gin*Line)
                    b=CB+(Bin*Line)
                else:#draw the new background colour for this line
                    r=R2
                    g=G2
                    b=B2
            else:#draw the old background colour for this line
                r=CR
                g=CG
                b=CB
            while(y<8):#each loop of this sets the colour of one pixel in the current line
                #### if the values generated are out of range, make them safe:
                if(r>255):
                    r=225
                if(r<0):
                    r=0
                if(g>255):
                    g=225
                if(g<0):
                    g=0
                if(b>255):
                    b=225
                if(b<0):
                    b=0
                ####
                #set the pixel to the desired colour
                if(direction=="UP"):
                    SENSE.set_pixel(y,7-x,r,g,b)
                elif(direction=="DOWN"):
                    SENSE.set_pixel(y,x,r,g,b)
                elif(direction=="LEFT"):
                    SENSE.set_pixel(7-x,y,r,g,b)
                else:
                    SENSE.set_pixel(x,y,r,g,b)
                y=y+1
            x=x+1
            y=0
        Start=Start-1
        x=0
        if(Line>7):
            Line=Line-7
        else:
            Line=0
        time.sleep(1-speed)
    # sets the new background colour
    CR=R2
    CG=G2
    CB=B2

###################################### GUI loops ######################################

######## Volume Control GUI ########
def VolumeChange():#displays a GUI control to change the Volume
    global IsVolumeDisplaying
    global Beep
    IsVolumeDisplaying = True
    volume = float(pygame.mixer.music.get_volume())#get the current volume
    print("Opening Volume control")
    print("Use left / right to adjust the volume. Press Enter or the lower left button to go back")
    while(True):#GUI loop
        (key,presses) = Update()
        if(key == "NONE"):
            time.sleep(0.1)
        if(key == "LEFT"):
            volume = volume - presses * 0.05#decrese volume
        if(key == "RIGHT"):
            volume = volume + presses * 0.05#increse volume
        if(key=="VOLUME" or key=="RETURN"):
            break#close the volume control GUI
        if(ReturnToMain):
            break #close the volume control GUI
        if(volume > 1):
            volume = 1
        if(volume < 0):
            volume = 0
        #draws a bar accross the screen to show the volume level
        x = 0
        y = 0
        while(x < 8):
            while(y < 8):
                if(int(str(x)+str(y)) in VolumeIcon):#draws an icon above the bar, VolumeIcon holds the collection of pixel co-ordinates that make up the image
                    SENSE.set_pixel(x,y,100,100,250)
                elif((x*8)+y-0.01<volume*64):
                    SENSE.set_pixel(x,y,100,100,0)
                else:
                    SENSE.set_pixel(x,y,0,50,0)
                y = y + 1
            x = x + 1
            y = 0
        pygame.mixer.music.set_volume(volume)#finally set the volume
        Beep.set_volume(pygame.mixer.music.get_volume()/2)#set the volume for the beep sound at half the volume
    IsVolumeDisplaying=False
    print("Closing Volume control")

######## Picking a song GUI ########
def PickSong():#displays a GUI that lets the user pick a song
    """
    Pick song displays a GUI that allows the user to pick a song to play:
    > When it loads the letter 'A' is displayed. Using the joystick up/down the user can
    scroll through the alphabet. 
    > If the middle key or right is pressed on the joystick then the function will  
    display the name of the song with the matching first letter. 
    > Then using up/down the user can scroll through the songs in alphabetical order.
    > If left is pressed then it will go back to the alphabet.
    > If left is pressed on the alphabet the program returns to the main menu. 
    > When the user find the song that he/she wants to play they can press right or the 
    middle key to play that song. It will show a play icon and return to the main menu
    >Songs beginning with a non-alphabetic character are under '*' which is above A in the scroll
    """
    global RequestPickSong
    global MPid
    global PassMessage
    global ReturnToMain
    global TimeoutDisabled
    print("Opening Song picker")
    Alpha=True#True when the user is scrolling through the alphabet
    transition("RIGHT",40,110,150,0.99)
    scroll=1#current position in the scrolling GUI
    scrollMAX=26#max elements in the scroll GUI
    print("""HELP: Use up/down to scroll through the alphabet. 
    Press enter or right to find a song beginning with that letter.
    Then use up/down to scroll through the songs in alphabetical order.
    Press enter or right to select a song.
    The symbol * is above A and lists songs that don't begin with a letter.
    Left will go back.""")
    SENSE.show_letter(LETTERS[scroll],back_colour=(CR,CG,CB),text_colour=(255,50,50))#shows the first letter in the alphabet
    while(True):#GUI loop
        eventN="None"
        presses=0
        (eventN,presses)=Update()#update
        RequestPickSong=False#cancel the request to pick a song
        if(ReturnToMain):#cancel and return back to the main menu
            messageKill()
            ReturnToMain=False
            return
        if(Alpha):
            TimeoutDisabled=False
        else:
            TimeoutDisabled=True#disables timeout when the song names are being displayed
        #events
        if (eventN=="DOWN"):
            scroll=scroll+presses#scroll down
            scroll=PickSongDisplay("DOWN",scroll,scrollMAX,Alpha)#scroll to the new item     
            time.sleep(0.5)
                    
        if (eventN=="UP"):
            scroll=scroll-presses#scroll up
            scroll=PickSongDisplay("UP",scroll,scrollMAX,Alpha)#scroll to the new item 
            time.sleep(0.5)
        if (eventN=="RIGHT" or eventN=="RETURN"):
            if(Alpha):#is the user scrolling through the alphabet?
                i=0
                #check if the current letter matches at least one song
                for song in Songs:
                    if(song[0].upper()==LETTERS[scroll]):
                        break
                    i=i+1
                        
                if(LETTERS[scroll]=='*'):#if the letter is '*' then pick a song that starts with a non alphabetical character
                    i=0
                    for song in Songs:
                        if(not song[0].upper() in LETTERS):
                            break
                        i=i+1
                #shows cross if there is no match
                if(i==len(Songs)):
                    transition("RIGHT",150,0,0,0.995)
                    SENSE.show_letter("X",back_colour=(150,0,0))
                    print("No songs begin with: "+LETTERS[scroll])
                    time.sleep(1)
                    scroll=PickSongDisplay("LEFT",scroll,scrollMAX,Alpha)#go back to the alphabet scroll
                    continue
                #shows song name
                Alpha=False#user is now on the song scroll
                scroll=i
                scrollMAX=len(Songs)-1#set the max scroll to the number of songs
                scroll=PickSongDisplay("RIGHT",scroll,scrollMAX,Alpha) #display the song
            else:#if user is on the song scroll then play the chosen song
                messageKill()
                transition("RIGHT",50,50,70,0.97)
                SENSE.set_pixels(Images.ImgPlay)#show the play icon
                Play(SONG_PATH+Songs[scroll]+".mp3",scroll)#play the chosen song
                time.sleep(1)
                transition("RIGHT",0,0,50,0.99)
                #play
                break#Close the song picker GUI
                
        if (eventN=="LEFT"):
            if(Alpha):#if user is scrolling through the alphabet then quit
                messageKill()
                transition("LEFT",0,0,50,0.99)
                break#Close the song picker GUI
            else:#if user is scrolling through the songs then go back to the alphabet
                Alpha=True
                try:
                    scroll=LETTERS.index(Songs[scroll][0].upper())#try to find the first letter of the song and go back to that letter in the alphabet
                except:
                    scroll=0#if it begins with a non alphabetical character then go back to '*'
                scrollMAX=26#the total elements in the scroll
                scroll=PickSongDisplay("LEFT",scroll,scrollMAX,Alpha)#show the letter
    TimeoutDisabled=False 
    print("Closing Song picker")  
             
#### PickSong helper function ####          
def PickSongDisplay(direction,scroll,scrollMAX,Alpha):#utility for PickSong that scrolls to a position in the GUI
    messageKill()
    if(scroll>scrollMAX):
        scroll=0#go to the top element of the scroll
    if(scroll<0):
        scroll=scrollMAX#go to the bottom element of the scroll
    #### alternates between two background colours by checking if the number is even
    if(scroll%2==0):
        transition(direction,(scroll+1)*3,120-(scroll+1)*3,0,0.99)
    else:
        transition(direction,(scroll+1)*3,120-(scroll+1)*3,100,0.99)
    ####
    if(Alpha):
        SENSE.show_letter(LETTERS[scroll],back_colour=(CR,CG,CB),text_colour=(255,50,50))#show the letter
    else:
        message(Songs[scroll])#show the song name
    return scroll

######## Main Menu GUI Loop ########
def MainMenu():
    """
    The Main menu is the master loop of the whole program.
    The main menu has two parts:
    > Home Screen / visualisations
    > Settings
    The Home screen shows a song icon. When the program is started or times out it returns here, it is the default screen for the program.
    The Home/visualisations button takes the user back to this menu from any point. If the user is already on the Home screen the button
    cycles through the visualisations. The visualisations are a bit like screensavers, to see the full list of visualisations check the top
    of the program. visualisations are updated with the function 'SongVisualsUpdate(reset)' the reset is a bool and if true shows the main menu.
    
    The Settings are accessed by pressing the down key on the joystick. Using the joystick you can then press left or right to scroll
    through elements in the list. Down or enter can be pressed to select the item and launch the setting.
    """
    global ReturnToMain
    global Shuffle
    global Menu
    global TimeoutDisabled
    global CR
    global CG
    global CB
    Menu="Main"
    transition("RIGHT",0,0,50,0.99)
    SENSE.set_pixels(Images.ImgMain)
    SIndex=0#settings menu scroll position
    SongVisualsUpdate(True)
    Update()#discards any pressed keys
    print("""Main Menu - Press in any direction on the joystick to launch the settings. From there you can pick a song.
    If a song is playing, press the lower right button to cycle through visualisations.""")
    while(True):#GUI loop
        (key,presses)=Update()#get key presses
        if(RequestPickSong):#if the user has requested to pick a song
            PickSong()#launches the GUI to pick a song
            SENSE.set_pixels(Images.ImgMain)
            Menu="Main"
            Update()#discards any pressed keys
            continue
        if(Menu=="Main"):

            SongVisualsUpdate(False)#update the visualisations
            SIndex=0#resets the settings scroll index
            if(ReturnToMain):#refresh what is displaying
                CR=0
                CG=0
                CB=50
                SongVisualsUpdate(True)
                ReturnToMain=False
            if(key=="DOWN" or key=="RETURN" or key=="LEFT" or key=="RIGHT" or key=="UP"):#if a joystick event has been detected, open settings
                Menu="Settings"
                print("Settings - use left/right to scroll through each setting. Press enter to launch that setting or up to go back to Main Menu")
                DisplayIcon(SIndex,"DOWN")
                Update()#discards any pressed keys
                continue
        if(Menu=="Settings"):
            if(ReturnToMain):#refresh what is displaying
                print("Settings")
                CR=0
                CG=60
                CB=0
                DisplayIcon(SIndex,"DOWN")#displays the setting icon
                ReturnToMain=False
            if(key=="UP"):#go back to the main menu
                Menu="Main"
                print("Returning to Main Menu")
                transition("UP",0,0,50,0.99)
                SongVisualsUpdate(True)
                Update()#discards any pressed keys
                continue
            if(key=="LEFT"):#scroll left
                SIndex=SIndex-1
                if(SIndex<0):
                    SIndex=len(SICONS)-1
                DisplayIcon(SIndex,"LEFT")#displays the setting icon
            if(key=="RIGHT"):#scroll right
                SIndex=SIndex+1
                if(SIndex==len(SICONS)):
                    SIndex=0
                DisplayIcon(SIndex,"RIGHT")#displays the setting icon
            if(key=="DOWN" or key=="RETURN"):#select the setting
                # SICONS is a list of names corresponding to settings and their icons
                print("Launching Setting: "+SICONS[SIndex])
                if(SICONS[SIndex]=="Pick"):#pick a song setting
                    transition("DOWN",100,0,100,0.99)
                    PickSong()#launches the pick song GUI
                    Menu="Main"#returns to the menu
                    SongVisualsUpdate(True)
                    Update()#discards any pressed keys
                    continue
                if(SICONS[SIndex]=="Volume"):#change volume setting
                    transition("DOWN",100,0,100,0.99)
                    VolumeChange()
                    DisplayIcon(SIndex,"UP")
                    Update()#discards any pressed keys
                    continue
                if(SICONS[SIndex]=="Shuffle"):#toggle Shuffle setting
                    if(Shuffle):
                        transition("DOWN",0,100,0,0.99)#transitions to green
                        SENSE.set_pixels(Images.ImgYes)
                    else:
                        transition("DOWN",100,0,0,0.99)#transitions to red
                        SENSE.set_pixels(Images.ImgNo)
                    while(True):#GUI loop
                        (key,presses)=Update()
                        if(ReturnToMain):
                            messageKill()
                            break
                        if(key=="None"):
                            time.sleep(0.01)
                        if(key=="UP" or key=="RETURN"):#return to settings
                            DisplayIcon(SIndex,"UP")
                            break
                        
                        if(key=="LEFT" or key=="RIGHT" ):#toggle Shuffle
                            if(Shuffle):
                                print("Shuffle Off")
                                Shuffle=False
                                SENSE.set_pixels(Images.ImgNo)
                                CR=100
                                CG=0
                                CB=0
                            else:
                                print("Shuffle On")
                                Shuffle=True
                                SENSE.set_pixels(Images.ImgYes)
                                CR=0
                                CG=100
                                CB=0
                    Update()#discards any pressed keys
                    continue
                if(SICONS[SIndex]=="Quit"):#Quit setting (this displays an animation and then shuts down the program)
                    transition("DOWN",0,70,90,0.99)
                    print("Goodbye")
                    messageKill()
                    message("Goodbye")
                    pygame.mixer.music.fadeout(6000)#fades out the music
                    time.sleep(6)
                    messageKill()
                    transition("DOWN",0,0,0,0.6)
                    return#ends the main menu GUI loop and returns execution to the end of the program wher MainMenu() was called
                if(SICONS[SIndex]=="Info"):#Displays a short message saying Hi!
                    transition("DOWN",0,80,100,0.99)
                    messageKill()
                    TimeoutDisabled=True
                    message("Hi Tim - Tim's Interstellar Music Player was made by Joe Speers   Have fun :)")#show the message
                    Update()#discard key presses
                    while(True):
                        (key,presses)=Update()
                        if(ReturnToMain):
                            messageKill()
                            break
                        if(key=="None"):
                            time.sleep(0.1)
                        else:#if any key is pressed
                            break
                    TimeoutDisabled=False
                    messageKill()
                    DisplayIcon(SIndex,"UP")
                    Update()#discards any pressed keys
                    continue
                if(SICONS[SIndex]=="Alarm"):#Lets the user set an alarm for a certain time
                    transition("DOWN",50,0,40,0.97)
                    messageKill()
                    print("Press enter to dismiss the onscreen message then toggle the alarm On/Off (left/right), press enter to select")
                    message("On/Off   Set Alarm")#ask the user to set the alarm on or off
                    Update()#update
                    TimeoutDisabled=True

                    #get current settings
                    AlarmOn=False
                    Hours=Alarm.Hour
                    Minutes=Alarm.Minute
                    Section="OnOffMessage"#Section holds the name of what is currently displaying
                    while(True):#GUI loop
                        time.sleep(0.1)
                        (key,presses)=Update()#update
                        if(ReturnToMain):
                            messageKill()
                            break
                        if(Section=="OnOffMessage"):#waits for the user to press return and then goes to OnOff
                            if(key=="RETURN"):
                                Section="OnOff"
                                messageKill()
                                transition("DOWN",0,100,0,0.97)
                                key="LEFT"#triggers loading the image (just below)
                        if(Section=="OnOff"):
                            if(key=="LEFT" or key=="RIGHT"):#toggles the alarm on/off
                                if(AlarmOn):
                                    AlarmOn=False
                                    SENSE.set_pixels(Images.ImgNo)
                                    #sets the background colour
                                    CR=100
                                    CG=0
                                    CB=0
                                else:
                                    AlarmOn=True
                                    SENSE.set_pixels(Images.ImgYes)
                                    #sets the background colour
                                    CR=0
                                    CG=100
                                    CB=0
                            if(key=="RETURN"):#go on to the next part
                                if(AlarmOn):
                                    Section="HoursMessage"
                                    messageKill()
                                    transition("DOWN",50,0,40,0.97)
                                    message("Hour Set")#ask the user to set the hour
                                    print("Set the Hours (up/down to pick)")
                                else:
                                    Section="End"
                                    messageKill()
                                    transition("DOWN",50,0,40,0.97)
                                    message("Alarm Off")
                                    print("Alarm Disabled")
                                continue#returns to the settings
                        if(Section=="HoursMessage"):#waits for the user to press return and then goes to Hours
                            if(key=="RETURN"):
                                Section="Hours"
                                key="UP"#triggers loading the image (just below)
                                messageKill()
                                transition("DOWN",0,60,30,0.97)
                        if(Section=="Hours"):#lets the user pick the hour
                            if(key=="UP"):
                                Hours+=presses
                                if(Hours>23):
                                    Hours=0
                                message(str(Hours))
                            if(key=="DOWN"):
                                Hours-=presses
                                if(Hours<0):
                                    Hours=23
                                message(str(Hours))
                            if(key=="RETURN"):
                                Section="MinutesMessage"
                                messageKill()
                                transition("DOWN",50,0,40,0.97)
                                message("Minutes Set")#asks the user to select the minutes
                                print("Set the Minutes (up/down to pick)")
                                continue
                        if(Section=="MinutesMessage"):#waits for the user to press return and then goes to Minutes
                            if(key=="RETURN"):
                                Section="Minutes"
                                key="UP"#triggers loading the image (just below)
                                messageKill()
                                transition("DOWN",0,60,30,0.97)
                        if(Section=="Minutes"):#lets the user pick the minute
                            if(key=="UP"):
                                Minutes+=presses
                                if(Minutes>59):
                                    Minutes=0
                                if(Minutes<10):
                                    message("0"+str(Minutes))
                                else:
                                    message(str(Minutes))
                            if(key=="DOWN"):
                                Minutes-=presses
                                if(Minutes<0):
                                    Minutes=59
                                if(Minutes<10):
                                    message("0"+str(Minutes))
                                else:
                                    message(str(Minutes))
                            if(key=="RETURN"):
                                Section="End"
                                messageKill()
                                transition("DOWN",50,0,40,0.97)
                                print("Alarm Set")
                                #displays the set time
                                if(Minutes<10):

                                    message("Set: "+str(Hours)+":0"+str(Minutes))
                                else:
                                    message("Set: "+str(Hours)+":"+str(Minutes))
                                
                                continue
                        if(Section=="End"):
                            if(key=="RETURN"):
                                #sets the time
                                Alarm.Set=AlarmOn
                                Alarm.Hour=Hours
                                Alarm.Minute=Minutes
                                messageKill()
                                break#end message waits for the user to press return and then exits
                    TimeoutDisabled=False
                    DisplayIcon(SIndex,"UP")#goes back to the settings menu
                if(SICONS[SIndex]=="Date"):#Shows the date and time
                    transition("DOWN",30,0,60,0.97)
                    messageKill()
                    message(str(datetime.datetime.now()))#show the date and time
                    TimeoutDisabled=True
                    while(True):#GUI loop
                        time.sleep(0.1)
                        (key,presses)=Update()
                        if(key!="None" or ReturnToMain):#if a key is pressed go back
                            messageKill()
                            break
                    TimeoutDisabled=False
                    DisplayIcon(SIndex,"UP")#goes back to settings
                if(SICONS[SIndex]=="Timer"):#Lets the user set and use a timer
                    transition("DOWN",30,0,60,0.97)
                    messageKill()
                    message("Minutes Set")#asks the user to set the minute
                    #settings for the timer
                    Minutes=0
                    Seconds=0
                    Section="MinutesMessage"#what part of the procedure the user is on
                    Update()#discards key presses
                    TimeoutDisabled=True#disables timeout
                    print("Press enter to dismiss the onscreen message then set the Minutes (up/down to pick). Press enter to select")
                    while(True):#GUI loop
                        time.sleep(0.1)
                        (key,presses)=Update()#update
                        if(ReturnToMain):
                            messageKill()
                            break
                        if(Section=="MinutesMessage"):#waits for the user to press return and then goes to Minutes
                            if(key=="RETURN"):
                                Section="Minutes"
                                key="UP"#triggers the display of the next part (just below)
                                messageKill()
                                transition("DOWN",0,40,40,0.97)
                        if(Section=="Minutes"):
                            if(key=="UP"):
                                Minutes+=presses#increse the minutes
                                if(Minutes>500):
                                    Minutes=0
                                message(str(Minutes))#show the minutes as a message
                            if(key=="DOWN"):
                                Minutes-=presses#decrese the minutes
                                if(Minutes<0):
                                    Minutes=500
                                message(str(Minutes))#show the minutes as a message
                            if(key=="RETURN"):#the user has selected the current value
                                Section="SecondsMessage"
                                messageKill()
                                transition("DOWN",30,0,60,0.97)
                                message("Seconds Set")#asks the user to select the seconds
                                print("Set the Seconds (up/down to pick)")
                                continue
                        if(Section=="SecondsMessage"):#waits for the user to press return and then goes to Seconds
                            if(key=="RETURN"):
                                Section="Seconds"
                                key="UP"#triggers the display of the next part (just below)
                                messageKill()
                                transition("DOWN",0,40,40,0.97)
                        if(Section=="Seconds"):
                            if(key=="UP"):
                                Seconds+=presses#increse the seconds
                                if(Seconds>59):
                                    Seconds=0
                                if(Seconds<10):
                                    message("0"+str(Seconds))#show the seconds as a message
                                else:
                                    message(str(Seconds))
                            if(key=="DOWN"):
                                Seconds-=presses#decrese the seconds
                                if(Seconds<0):
                                    Seconds=59
                                if(Seconds<10):
                                    message("0"+str(Seconds))#show the seconds as a message
                                else:
                                    message(str(Seconds))
                            if(key=="RETURN"):#the user has selected the current value
                                Section="Timer"
                                messageKill()
                                transition("DOWN",30,0,60,0.97)
                                print("Timer set, press enter to activate")
                                message("Set: "+str(Minutes)+"M "+str(Seconds)+"S")#tells the user the selected time
                                continue
                        if(Section=="Timer"):
                            if(key=="RETURN"):#activates the timer

                                messageKill()
                                transition("DOWN",0,50,0,0.97)
                                #draws a bar accross the screen to show the timer time
                                Seconds+=Minutes*60
                                progress=0
                                while(True):#GUI loop
                                    (key,presses)=Update()#update
                                    time.sleep(0.1)
                                    progress+=0.1
                                    if(ReturnToMain):
                                        messageKill()
                                        break
                                    if(progress>Seconds):#when the countdown has completed
                                        AlarmSetoff()#set off an alarm
                                        break#return to settings
                                    level=progress/Seconds#works out the value of the bar
                                    #Draws the bar:
                                    x = 0
                                    y = 0
                                    while(x < 8):
                                        while(y < 8):
                                            if((x*8)+y-0.01<level*64):
                                                SENSE.set_pixel(x,y,0,150,100)#coloured
                                            else:
                                                SENSE.set_pixel(x,y,0,50,0)#clear
                                            y = y + 1
                                        x = x + 1
                                        y = 0
                                    if(key=="RETURN"):#if return is pressed, canecel the timer
                                        messageKill()
                                        break#end message waits for the user to press return and then exits
                                break
                    TimeoutDisabled=False#re-enables the timeout
                    DisplayIcon(SIndex,"UP")#goes back to the settings menu
                if(SICONS[SIndex]=="Message"):#Displays a daily message to Tim
                    transition("DOWN",90,0,30,0.97)
                    messageKill()#kills any displaying message
                    TimeoutDisabled=True#disables the timeout

                    #### Reading the Messages file ####

                    try:#attempts to read all the data from the messages file
                        MessageFile = open(RESOURCES_PATH+"Messages.txt")
                        date=MessageFile.readline().strip()#first line is the date the last message was given out
                        index=int(MessageFile.readline())#index is the index of the last message
                        Messages=[]#this will hold the messages
                        dateObject=datetime.datetime.now()#gets the date
                        DateNow=str(dateObject.year)+str(dateObject.month)+str(dateObject.day)#gets the date in the same format as the one in the text file
                        for line in MessageFile:#reads all the messages into the Messages list
                            if(line==date or line==str(index)):
                                continue
                            Messages.append(line.strip())
                        MessageFile.close()#closes the file
                    except:#if the file read failed
                        print("Error reading Messages file")
                        TimeoutDisabled=False
                        DisplayIcon(SIndex,"UP")#goes back to the settings menu
                        continue

                    #### Finding the right message ####

                    if(not date==DateNow):#if the last message was given out more than a day ago, then set the new date and change to a new message
                        date=DateNow
                        print("New date: "+date)
                        index+=1

                    if(index+1>len(Messages)):#returns to the first message if all the messages have been given out
                        index=0

                    message(Messages[index])#shows the message
                    print("Message: "+str(index))

                    #### Writing to the Messages file ####

                    try:
                        MessageFile = open(RESOURCES_PATH+"Messages.txt",'w')#open the file
                        MessageFile.write(date+'\n')#write the date
                        MessageFile.write(str(index)+'\n')#write the index
                        for line in Messages:#write all of the messages
                            MessageFile.write(line+'\n')
                        MessageFile.close()#close the file

                    except:#if the file write failed
                        print("Error writing to Messages file")
                        TimeoutDisabled=False
                        DisplayIcon(SIndex,"UP")#goes back to the settings menu
                        continue

                    #### Waiting for user to dismiss the message ####

                    Update()#discards any key presses
                    while(True):#GUI loop
                        (key,presses)=Update()

                        if(ReturnToMain):
                            messageKill()
                            break
                        if(key!="None"):#if a key is pressed, return
                            messageKill()
                            break

                    #### Returning to settings ####

                    TimeoutDisabled=False#re-enables the timeout
                    DisplayIcon(SIndex,"UP")#goes back to the settings menu
                             
#### Main menu helper functions ####
def DisplayIcon(index,direction):#MainMenu settings utility to scroll through the settings
    transition(direction,100,50,100,0.995)
    transition(direction,0,60,0,0.995)
    if(SICONS[index]=="Alarm"):
        SENSE.set_pixels(Images.ImgAlarm)#shows the icon
        print("Set an alarm")
    elif(SICONS[index]=="Date"):
        SENSE.set_pixels(Images.ImgDate)
        print("Show the date and time")
    elif(SICONS[index]=="Info"):
        SENSE.set_pixels(Images.ImgInfo)
        print("Show a short message")
    elif(SICONS[index]=="Message"):
        SENSE.set_pixels(Images.ImgMessage)
        print("Tim's daily message")
    elif(SICONS[index]=="Pick"):
        SENSE.set_pixels(Images.ImgPick)
        print("Pick a song")
    elif(SICONS[index]=="Quit"):
        SENSE.set_pixels(Images.ImgQuit)
        print("Quit")
    elif(SICONS[index]=="Shuffle"):
        SENSE.set_pixels(Images.ImgShuffle)
        print("Shuffle On/Off")
    elif(SICONS[index]=="Timer"):
        SENSE.set_pixels(Images.ImgTimer)
        print("Set a timer")
    elif(SICONS[index]=="Volume"):
        SENSE.set_pixels(Images.ImgVolume)
        print("Adjust the Volume")   

def SongVisualsUpdate(reset):#when the program times out, this displays different visuals
    global CurrentTimeOut
    global VMode
    global CR
    global CG
    global CB
    global RequestUpdateVisuals
    if(reset and not CurrentTimeOut==-1):#display main menu
        messageKill()
        SENSE.set_pixels(Images.ImgMain)
    if(RequestUpdateVisuals):#Setup visualisation
        RequestUpdateVisuals=False
        CurrentTimeOut=-1
        messageKill()
        if(PlayingI==-1):#if it is not playing a song then visualisations are disabled
            VMode=0# VISUAL_MODES[0] is "Main"
        if(VISUAL_MODES[VMode]=="Main"):#Main menu
            SENSE.set_pixels(Images.ImgMain)
        if(VISUAL_MODES[VMode]=="Song"):#Shows the name of the currently playing song
            print("visualisation: Song Name   Pressing any key will wake up TIMP and return to the Main menu")
            #sets background colour
            CR=50
            CG=20
            CB=0
            message(Songs[PlayingI])#shows the name of the song
        if(VISUAL_MODES[VMode]=="Snakes"):
            print("visualisation: Snakes")
            #sets the values for snakes
            SENSE.clear()
            VSnakes.x1=0
            VSnakes.y1=0
            VSnakes.d1=0
            VSnakes.x2=7
            VSnakes.y2=7
            VSnakes.d2=2
            VSnakes.L1=4
            VSnakes.L2=4
        if(VISUAL_MODES[VMode]=="Bars"):
            print("visualisation: Bars")
            VBars.Position=[0,3,5,7,0,2,1,3]#sets the first position of the bars
            SENSE.clear()
        if(VISUAL_MODES[VMode]=="Circles"):
            print("visualisation: Circles")
            SENSE.clear()
            VCircles.Screen=[[[20 for x in range(3)] for x in range(8)] for x in range(8)]#sets up the array that holds a screen image
        if(VISUAL_MODES[VMode]=="Stats"):
            print("visualisation: Stats")
            #sets background colour
            CR=60
            CG=0
            CB=20
            #shows the stats message
            message("Temp: "+str(round(SENSE.get_temperature(),1))+" C    Humidity: "+str(round(SENSE.get_humidity(),1))+"%    Pressure: "+str(round(SENSE.get_pressure(),1))+" mb.  ")#displays stats
    if(CurrentTimeOut==-1):#if only updating visuals (ie not just timed out)
        if(VISUAL_MODES[VMode]=="Snakes"):#displays randomised colourful snakes
            time.sleep(0.02)
            ######## colour ########
            #change colour
            r=VSnakes.r+VSnakes.RP
            g=VSnakes.g+VSnakes.GP
            b=VSnakes.b+VSnakes.BP
            r2=VSnakes.r2+VSnakes.RP
            g2=VSnakes.g2+VSnakes.GP
            b2=VSnakes.b2+VSnakes.BP
            #precautions
            if(r>255): r=255
            if(g>255): g=255
            if(b>255): b=255
            if(r2>255): r2=255
            if(g2>255): g2=255
            if(b2>255): b2=255
            if(r<0): r=1
            if(g<0): g=1
            if(b<0): b=1
            if(r2<0): r2=1
            if(g2<0): g2=1
            if(b2<0): b2=1
            #update the colour variables
            VSnakes.r=r
            VSnakes.g=g
            VSnakes.b=b
            VSnakes.r2=r2
            VSnakes.g2=g2
            VSnakes.b2=b2

            ######## Draw Snakes ########
            SENSE.set_pixel(VSnakes.x1,VSnakes.y1,r,g,b)
            SENSE.set_pixel(VSnakes.x2,VSnakes.y2,r2,g2,b2)
                
            ######## Move Snakes ########
            turn=VSnakes.L1+4#works out the pixel position where the snake should turn
            if(VSnakes.d1==0):
                VSnakes.x1+=1#move the 'head' of the snake
                if(VSnakes.x1>=turn):#if it should turn
                    VSnakes.x1-=1
                    VSnakes.d1=1#change position
                    VSnakes.L1-=1#decrese the length of a 'side'
            if(VSnakes.d1==1):
                VSnakes.y1+=1
                if(VSnakes.y1>=turn):
                    VSnakes.y1-=1
                    VSnakes.d1=2
            if(VSnakes.d1==2):
                VSnakes.x1-=1
                if(VSnakes.x1<=7-turn):
                    VSnakes.x1+=1
                    VSnakes.d1=3
                    VSnakes.L1-=1
                        
            if(VSnakes.d1==3):
                VSnakes.y1-=1
                if(VSnakes.y1<=7-turn):
                    VSnakes.y1+=1
                    VSnakes.d1=0
            #2nd snake
            turn=VSnakes.L2+4
            if(VSnakes.d2==0):
                VSnakes.x2+=1
                if(VSnakes.x2>=turn):
                    VSnakes.x2-=1
                    VSnakes.d2=1
                    VSnakes.L2-=1
                        
            if(VSnakes.d2==1):
                VSnakes.y2+=1
                if(VSnakes.y2>=turn):
                    VSnakes.y2-=1
                    VSnakes.d2=2
                        
            if(VSnakes.d2==2):
                VSnakes.x2-=1
                if(VSnakes.x2<=7-turn):
                    VSnakes.x2+=1
                    VSnakes.d2=3
                    VSnakes.L2-=1
            if(VSnakes.d2==3):
                VSnakes.y2-=1
                if(VSnakes.y2<=7-turn):
                    VSnakes.y2+=1
                    VSnakes.d2=0
            #checks if snake has reached the middle
            if(VSnakes.L2==0):
                #if so, reset the snakes
                VSnakes.HasStarted=True
                VSnakes.x1=0
                VSnakes.y1=0
                VSnakes.d1=random.randrange(0,4)
                VSnakes.x2=7
                VSnakes.y2=7
                VSnakes.d2=VSnakes.d1+2
                if(VSnakes.d2==4): VSnakes.d2=0
                if(VSnakes.d2==5): VSnakes.d2=1
                VSnakes.L1=4
                VSnakes.L2=4
                VSnakes.RP=random.randrange(-10,10)
                VSnakes.GP=random.randrange(-10,10)
                VSnakes.BP=random.randrange(-10,10)
                VSnakes.r=random.randrange(10,100)
                VSnakes.g=random.randrange(10,100)
                VSnakes.b=random.randrange(10,100)
                VSnakes.r2=random.randrange(10,100)
                VSnakes.g2=random.randrange(10,100)
                VSnakes.b2=random.randrange(10,100)
        if(VISUAL_MODES[VMode]=="Bars"):#displays a randomised bars sound view
            time.sleep(0.13)
            i=0#this is the 'line' or x index
            for Height in VBars.Position:#height is the last height of each line
                NewHeight=random.randrange(0,8)
                if(NewHeight>Height and random.randrange(0,2)==0):#if the new height is higher than the old one and a random chance
                    VBars.Position[i]=NewHeight
                else:#if not then decrese the height of the line
                    if(Height<1):#checks if the line is at 0 already
                        Height=1
                    VBars.Position[i]=Height-1
                #Rendering the line
                y=0
                while(y<8):#cycles through each pixel in the line
                    if(y<Height):#if the pixel is below the height
                        SENSE.set_pixel(i,7-y,VBars.BR,VBars.BG,VBars.BB)
                    if(y==Height):#if the pixel is the same as the height
                        SENSE.set_pixel(i,7-y,VBars.PR,VBars.PG,VBars.PB)
                    if(y>Height):#if the pixel is above the height
                        SENSE.set_pixel(i,7-y,0,0,0)#clear the pixel
                    y+=1
                #next line
                i+=1
        if(VISUAL_MODES[VMode]=="Circles"):#displays random circles
            if(random.randrange(0,30)==1):
                VDrawCircle()#draw another circle
            time.sleep(0.01)
            #RENDERING
            x=0
            y=0
            for array in VCircles.Screen:#each line
                for array2 in array:#each pixel
                    SENSE.set_pixel(x,y,array2[0],array2[1],array2[2])
                    #slowly darkens old cirles untill they dissapear
                    i=0
                    while(i<3):
                        array2[i]-=1
                        if(array2[i]<0):
                            array2[i]=0
                        i+=1
                    y+=1
                y=0
                x+=1     
        if(VISUAL_MODES[VMode]=="Stats"):#displays temperature, humidity and pressure
            time.sleep(0.1)
            if(random.randrange(0,5000)==3):#randomly updates the display every few minutes
                message("Temp: "+str(round(SENSE.get_temperature(),1))+" C    Humidity: "+str(round(SENSE.get_humidity(),1))+"%    Pressure: "+str(round(SENSE.get_pressure(),1))+" mb.  ")#displays stats 
       
def VDrawCircle():#helper function for the circles visualisation that draws a circle
    C=VCircles.C1
    rot=0#current rotation (increases as the program draws the circle)
    C.ra=random.randrange(1,6)#sets the radius
    C.x=random.randrange(1,7)#sets the midpoint
    C.y=random.randrange(1,7)
    C.r=random.randrange(0,150)#sets the colour
    C.g=random.randrange(0,150)
    C.b=random.randrange(0,150)
    while(rot<359):#this works out 360 points in the circle and draws them to the nearest pixel
        rot+=1
        TempRot=rot
        #makes TempRot between 0-89 so the triginomitry will work
        if(rot>89):
            TempRot=rot-90
        if(rot>179):
            TempRot=rot-180
        if(rot>269):
            TempRot=rot-270
        #using the radius and the rotation it works out the x and y co-ordinates with triginometry and pythagorous
        Ty=math.cos(TempRot*(math.pi/180))*C.ra
        if(Ty==0):
            Tx=C.ra
        else:
            Tx=math.sqrt((C.ra*C.ra)-(Ty*Ty))
        #now it converts the co-ordinates to the position on the screen
        if(rot>269):
            Nx=C.x-Ty
            Ny=C.y+Tx
        elif(rot>179):
            Nx=C.x-Tx
            Ny=C.y-Ty
        elif(rot>89):
            Nx=C.x+Ty
            Ny=C.y-Tx    
        elif(rot<90):
            Nx=C.x+Tx
            Ny=C.y+Ty
        #checks if the pixel is on the screen before drawing
        if(not (int(round(Ny,0))>7 or round(Ny,0)<0 or int(round(Nx,0))>7 or int(round(Nx,0))<0)):
            VCircles.Screen[int(round(Nx,0))][7-int(round(Ny,0))]=[C.r,C.g,C.b]
                        
######################################  Threading slave ######################################

def BeginDisplayMessage():#run as a seperate process
    while(True):
        SENSE.show_message(PassMessage,back_colour=(CR,CG,CB),text_colour=(255,150,150),scroll_speed=0.14)  #shows the scrolling message

###################################### STARTUP CODE ######################################

######## Audio jack setup ########
os.system("sudo amixer cset numid=3 1")# Set audio output to Analogue Jack
os.system("sudo amixer cset numid=1 100%")# Set system volume to 100%

######## pygame setup ########
pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag
pygame.mixer.init()
pygame.display.set_mode((640, 480))
pygame.mixer.music.set_volume(0.7)#sets the volume

######## get music files ########
print("Loading songs")
for song in glob.glob(SONG_PATH+"*.mp3"):
    Songs.append(song[len(SONG_PATH):-4])
    print(song[len(SONG_PATH):-4])
Songs=sorted(Songs)
print("Loaded "+str(len(Songs))+" songs")

######## beep sound effect ########
Beep=pygame.mixer.Sound(RESOURCES_PATH+"Beep.ogg")
Beep.set_volume(pygame.mixer.music.get_volume()/2)

######## Sense Hat check ########
try:
    SENSE.clear()#clears screen
except:
    print("ERROR: Sense HAT is not connected! (FATAL")
    raise SystemExit#quit

######## Change to the case orientation ########
SENSE.set_rotation(270)

######## Resources check ########
if(len(Songs)==0):#checks if the program did not find and songs in the folder
    print("ERROR: No songs found in folder: "+SONG_PATH+"   (FATAL)")
    SENSE.show_message("ERROR: No songs found in folder: "+SONG_PATH+"   (FATAL)",text_colour=(255,50,50))
    raise SystemExit#quit

#checks if the required resources are in the right folder
if(not(os.path.isfile(RESOURCES_PATH+"Alarm.ogg") and os.path.isfile(RESOURCES_PATH+"Intro.ogg") and os.path.isfile(RESOURCES_PATH+"Beep.ogg"))):
   print("ERROR: One or more of the required resources are missing, check that the RESOURCES_PATH value is right: "+ RESOURCES_PATH+"   (FATAL)")
   SENSE.show_message("ERROR: One or more of the required resources are missing!  (FATAL)",text_colour=(255,50,50))
   raise SystemExit#quit

###################################### BEGIN CODE ######################################

######## Intro Animation ########
""" 
The intro animation has four parts:
> Snakes animation (Played twice)
> Wipe transition
> Welcome message
> Colour transiton to main menu
"""

if(INTRO_ENABLED):
    print("Running Intro")


    #### Snake animation ####

    #sets up the values for the snakes
    CurrentTimeOut=-1
    VMode=2

    Time=0#used to count the length in 0.02 second lengths
    while(Time<68):#68 is the length for 1 repeat of the snakes animation/visualisation
        Time+=1
        SongVisualsUpdate(False)#Update snakes

    #resets the values to their default values
    CurrentTimeOut=0
    VMode=0

    #### Wipe transition to a random colour ####
    pygame.mixer.Sound(RESOURCES_PATH+"Intro.ogg").play()#plays the intro tune
    #display index
    x = 0
    y = 0
    #picks a random colour
    r=random.randrange(0,100)
    g=random.randrange(0,80)
    b=random.randrange(0,150)
    #Draws the transition
    while(x < 8):#for each line
        while(y < 8):#for each pixel
            SENSE.set_pixel(x,y,r,g,b)#set the colour
            time.sleep(0.01)
            y = y + 1
        x = x + 1
        y = 0
    #Sets the current background colour to the new colour
    CR=r
    CG=g
    CB=b

    #### Message ####

    transition("DOWN",25,25,50,0.96)
    SENSE.show_message("Tim's Interstellar Music Player!",back_colour=(25,25,50),scroll_speed=0.05);#says hi

    #### Colour transitions ####

    transition("UP",200,100,20,0.96)
    transition("LEFT",100,200,100,0.96)
    transition("DOWN",50,100,200,0.96)

######## Load Main Menu ########
MainMenu()

######## End #########
print("Thanks for using, made by Joe Speers!")
