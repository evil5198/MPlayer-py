from tkinter import *
from tkinter import filedialog
from pygame import mixer
from mutagen.mp3 import MP3
import os
import sqlite3

#Tkinter is used for making this GUI Application(MPlayer)
#PyGame is used to play mp3 files
#Mutagen is used to get information about selected music file
#os library is used to access file location
#sqlite3 is used to help controlling media's position

#This Music Player Supports only .mp3 files
#In order to play music Browse the location of folder where your media is stored
#all your media will be shown in this application
#select the song and play the media using 'play' button

root = Tk()
#root is the main window of this application
direc = ""
#direc variable will store the directory of your media
itemLen = 0
#itemLen will store no. of media present on your selected folder
songName = ""
#songName will store the name of the song which is playing currently
conn = sqlite3.connect('seconds.db')
#conn is used to establish connection with database-seconds
playing = True
#playing is the global variable to check whether the media is playing or not
songNum = 0
#songNum is used to store the index of song playing currently
firstTime = True
#firstTime is used to check whether the function is running for the first time or not


def BrowseFiles():
    #BrowseFiles function is used by user to browse the folder where media is present
    #this function is attached to browse button in the application
    global direc
    global items
    #items variable is used to store all fetched media files from browsed folder
    try:
        direc = filedialog.askdirectory()
        items = os.listdir(direc)
        songsList.delete(0, itemLen)
        ListFiles()
        selectSong()
    except Exception as ex:
        print(ex)

def ListFiles():
    #ListFiles function is used to list all fetched media files in this application
    global itemLen
    try:
        itemLen = len(items)
        num = 1
        while num <= itemLen:
            if items[num-1].endswith(".mp3"):
                songsList.insert(num, items[num-1])
            num += 1
    except Exception as ex:
        print(ex)

def play(playButt = True):
    #play function is used to play the selected media file
    #this function is attached to play button in this application
    #playButt variable is used to check whether this function is called by pressing a button
    global firstTime
    global playing
    if playButt == True:
        selectSong()
    #if this function is called by pressing play button then this function plays the selected song
    playing = True
    mixer.init()
    try:
        mixer.music.load(f"{direc}/{songName}")
        PlayButton.config(text = "Stop")
        PlayButton.config(command = stop)
        songTitle.config(text = songName)
        mixer.music.play()
    except Exception as ex:
        print(ex)
    conn.execute("UPDATE Seconds set second = 0")
    conn.commit()
    if firstTime == True:
        MPOS_LOOP()
        firstTime = False

def stop():
    #stop function is used to stop playing the current song
    #this function is attached to stop button in the application
    global playing
    PlayButton.config(text = "Play")
    PlayButton.config(command = play)
    mixer.music.stop()
    playing = False

#play and stop buttons are the same buttons ,they switch their function once clicked

def pause():
    #pause function is used to pause the media
    #this function is attached to pause button in the application
    global playing
    PauseButton.config(text = "Unpause")
    PauseButton.config(command = unpause)
    mixer.music.pause()
    playing = False

def unpause():
    #unpause function is used to unpause/pay the paused media
    #this function is attached to unpause button in the application
    global playing
    playing = True
    PauseButton.config(text = "Pause")
    PauseButton.config(command = pause)
    mixer.music.unpause()

#pause and unpause buttons are the same buttons ,they switch their function once clicked

def MusicPos(num = 1000):
    #MusicPos function is used to adjust the position of the media
    #this function is attached to music time bar
    num = int(num)
    #num variable is used to check if user wants to change the position of media by sliding the bar which shows how much the song is completed

    cursor = conn.execute("SELECT second from Seconds")
    #curser is used to get data from database

    for row in cursor:
        mPos = row[0]
    #variable mPos will be used to set location of music time bar
    #if num is less than 100 then user is changing the music time bar
    if num < 100:
        num = int(num)
        song = MP3(f"{direc}/{songName}")
        songLen = round(song.info.length)
        mPos = round((num/100)*songLen)
        mixer.music.set_pos(mPos)
        conn.execute(f"UPDATE Seconds set second = {mPos}")
        conn.commit()

        try:
            PercentComplete = round((mPos/songLen)*100)
            Mtime.set(PercentComplete)
            timeLabelString = f"{mPos}/{songLen}"
            timeLabel.config(text = timeLabelString)
        except Exception as ex:
            print(ex)
    else:
        song = MP3(f"{direc}/{songName}")
        songLen = round(song.info.length)
        try:
            PercentComplete = round((mPos/songLen)*100)
            Mtime.set(PercentComplete)
            timeLabelString = f"{mPos}/{songLen}"
            timeLabel.config(text = timeLabelString)
        except Exception as ex:
            print(ex)

def MPOS_LOOP():
    #MPOS_LOOP function is used to loop the musicPos function in order to update music time bar
    #this function also updates the time elapsed while playing the media 
    song = MP3(f"{direc}/{songName}")
    songLen = round(song.info.length)
    cursor = conn.execute("SELECT second from Seconds")

    for row in cursor:
        currentTime = row[0]
    if playing == True and currentTime != songLen:
        currentTime += 1
        conn.execute(f"UPDATE Seconds set second = {currentTime}")
        conn.commit()
    MusicPos()
    root.after(1000, MPOS_LOOP)

def selectSong():
    #this function is used to select the song user wants to play
    global songName
    TotalSongNum = songsList.curselection()
    try:
        songName = songsList.get(TotalSongNum[0])
    except Exception as ex:
        print(ex)

def setVolume(num):
    #setVolume function is used adjust the volume of the song
    #this function is attached to volume bar in the application
    volume = volumeScale.get()
    volume = volume/100
    try:
        mixer.music.set_volume(volume)
    except Exception as ex:
        print(ex)

def Next():
    #Next function is used to update the current playing media to the next midia if available
    #this function is attached to >>> buttton in the application
    try:
        global songName
        print(songName)
        songs = songsList.get(0, itemLen)
        print(songs)
        index = 0
        for song in songs:
            index += 1
            print(song)
            if song == songName:
                break
        print(index)
        songName = songs[index]
        stop()
        play(False)
    except Exception as ex:
        print(ex)

def Prev():
    #Prev function is used to update the current playing tmedia to its previous media if available
    #this function is attached to <<< button in the application
    try:
        global songName
        songs = songsList.get(0, itemLen)
        index = 0
        for song in songs:
            index += 1
            if song == songName:
                break
        songName = songs[index-2]
        stop()
        play(False)
    except Exception as ex:
        print(ex)

if __name__ == "__main__":
    #The main function contains declaration and initialization of all GUI widgets in this application
    root.title("MPlayer")
    #Title of this application is given
    root.geometry("500x500")
    #geometry of this application is declared
    root.resizable(0, 0)
    #application is restricted to be resizable
    global Mtime
    #Mtime variable is used to store elapsed time while music is playing

    icon = PhotoImage(file = "icon/MPlayer.png")
    root.iconphoto(False, icon)
    #application has been assigned a icon

    SongsWindow = LabelFrame(root)
    SongsWindow.place(x = 10, y = 10, height = 340, width = 480)
    #song window is created which will contain browse button and will list all media in the browsed folder
    BrowseButton = Button(SongsWindow, text = "Browse")
    BrowseButton.place(x = 200, y = 10, height = 25, width = 80)
    BrowseButton.config(command = BrowseFiles)
    #browse button is created to browse file explorer and select the folder containing your media
    songsList = Listbox(SongsWindow, selectmode = SINGLE)
    songsList.place(x= 10, y = 45, height = 285, width = 455)
    #songlist is used to list all fetched media and is also used by user to select the media he/she wants to play

    controlWindow = Frame(root, bg = "grey")
    controlWindow.place(x = 0, y = 350, width = 500, height = 150)
    #controlWindow contains all controls such as play ,pause,etc
    songTitle = Label(controlWindow, text = "TITLE", bg = "grey")
    songTitle.place(x = 10, y = 20)
    #songTitle displays title of the currently playing media
    Mtime = DoubleVar()
    Mbar = Scale(controlWindow, variable = Mtime, orient = HORIZONTAL, showvalue = 0, bg = "black", highlightbackground = "grey", troughcolor = "blue", command = MusicPos)
    Mbar.place(x = 10, y = 65, height = 20, width = 350)
    #Mbar shows the elapsed time while playing the song witht a scsle
    timeLabel = Label(controlWindow,text = "--/--", bg = "grey")
    timeLabel.place(x = 370, y = 65)
    #time label shows the elapsed time while playing the song in text form
    PrevButton = Button(controlWindow, text = "<<<", command = Prev)
    PrevButton.place(x = 20, y = 110, height = 25, width = 80)
    #prev button is created to play previous media
    PlayButton = Button(controlWindow, text = "Play", command = play)
    PlayButton.place(x = 120, y = 110, height = 25, width = 55)
    #play button is created to play the selected media
    PauseButton = Button(controlWindow, text = "Pause", command = pause)
    PauseButton.place(x = 185, y = 110, height = 25, width = 55)
    #pause button is created to pause the currently playing media
    NextButton = Button(controlWindow, text = ">>>", command = Next)
    NextButton.place(x = 260, y = 110, height = 25, width = 80)
    #next button is created to play next media
    vol = DoubleVar()
    volumeScale = Scale(controlWindow, variable = vol, bg = "grey", from_ = 100, to = 0, highlightbackground = "grey", command = setVolume)
    vol.set(100)
    volumeScale.place(x = 430, y = 15)
    #volume scale is used to adjust the volume of the media
    VOLable = Label(controlWindow, text = "Volume", bg = "grey")
    VOLable.place(x = 440, y = 120)
    #VOlable is the label showing current volume in text form

    root.mainloop()
    #mainloop starts