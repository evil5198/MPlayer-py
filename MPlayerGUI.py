from tkinter import *
from tkinter import filedialog
from pygame import mixer
from mutagen.mp3 import MP3
import os
import sqlite3

root = Tk()
direc = ""
itemLen = 0
songName = ""
conn = sqlite3.connect('seconds.db')
global playing
playing = True
songNum = 0
firtTime = True


def BrowseFiles():
    global direc
    global items
    try:
        direc = filedialog.askdirectory()
        items = os.listdir(direc)
        songsList.delete(0, itemLen)
        ListFiles()
        selectSong()
    except:
        pass

def ListFiles():
    global itemLen
    try:
        itemLen = len(items)
        num = 1
        while num <= itemLen:
            if items[num-1].endswith(".mp3"):
                songsList.insert(num, items[num-1])
            num += 1
    except:
        pass

def play(playButt = True):
    global firtTime
    global playing
    if playButt == True:
        selectSong()
    playing = True
    mixer.init()
    try:
        mixer.music.load(f"{direc}/{songName}")
        PlayButton.config(text = "Stop")
        PlayButton.config(command = stop)
        songTitle.config(text = songName)
        mixer.music.play()
    except:
        pass
    conn.execute("UPDATE Seconds set second = 0")
    conn.commit()
    if firtTime == True:
        MPOS_LOOP()
        firtTime = False

def stop():
    global playing
    PlayButton.config(text = "Play")
    PlayButton.config(command = play)
    mixer.music.stop()
    playing = False

def pause():
    global playing
    PauseButton.config(text = "Unpause")
    PauseButton.config(command = unpause)
    mixer.music.pause()
    playing = False

def unpause():
    global playing
    playing = True
    PauseButton.config(text = "Pause")
    PauseButton.config(command = pause)
    mixer.music.unpause()

def MusicPos(num = 1000):
    num = int(num)
    

    cursor = conn.execute("SELECT second from Seconds")

    for row in cursor:
        mPos = row[0]
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
        except:
            pass
    else:
        song = MP3(f"{direc}/{songName}")
        songLen = round(song.info.length)
        try:
            PercentComplete = round((mPos/songLen)*100)
            Mtime.set(PercentComplete)
            timeLabelString = f"{mPos}/{songLen}"
            timeLabel.config(text = timeLabelString)
        except:
            pass

def MPOS_LOOP():
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
    global songName
    TotalSongNum = songsList.curselection()
    try:
        songName = songsList.get(TotalSongNum[0])
    except:
        pass

def setVolume(num):
    volume = volumeScale.get()
    volume = volume/100
    try:
        mixer.music.set_volume(volume)
    except:
        pass

def Next():
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
    except:
        pass

def Prev():
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
        print(index-2)
        songName = songs[index-2]
        stop()
        play(False)
    except:
        pass

if __name__ == "__main__":
    root.title("MPlayer")
    root.geometry("500x500")
    root.resizable(0, 0)
    global Mtime

    icon = PhotoImage(file = "icon/MPlayer.png")
    root.iconphoto(False, icon)

    SongsWindow = LabelFrame(root)
    SongsWindow.place(x = 10, y = 10, height = 340, width = 480)
    BrowseButton = Button(SongsWindow, text = "Browse")
    BrowseButton.place(x = 200, y = 10, height = 25, width = 80)
    BrowseButton.config(command = BrowseFiles)
    songsList = Listbox(SongsWindow, selectmode = SINGLE)
    songsList.place(x= 10, y = 45, height = 285, width = 455)

    controlWindow = Frame(root, bg = "grey")
    controlWindow.place(x = 0, y = 350, width = 500, height = 150)
    songTitle = Label(controlWindow, text = "TITLE", bg = "grey")
    songTitle.place(x = 10, y = 20)
    Mtime = DoubleVar()
    Mbar = Scale(controlWindow, variable = Mtime, orient = HORIZONTAL, showvalue = 0, bg = "black", highlightbackground = "grey", troughcolor = "blue", command = MusicPos)
    Mbar.place(x = 10, y = 65, height = 20, width = 350)
    timeLabel = Label(controlWindow,text = "--/--", bg = "grey")
    timeLabel.place(x = 370, y = 65)
    PrevButton = Button(controlWindow, text = "<<<", command = Prev)
    PrevButton.place(x = 20, y = 110, height = 25, width = 80)
    PlayButton = Button(controlWindow, text = "Play", command = play)
    PlayButton.place(x = 120, y = 110, height = 25, width = 55)
    PauseButton = Button(controlWindow, text = "Pause", command = pause)
    PauseButton.place(x = 185, y = 110, height = 25, width = 55)
    NextButton = Button(controlWindow, text = ">>>", command = Next)
    NextButton.place(x = 260, y = 110, height = 25, width = 80)
    vol = DoubleVar()
    volumeScale = Scale(controlWindow, variable = vol, bg = "grey", from_ = 100, to = 0, highlightbackground = "grey", command = setVolume)
    vol.set(100)
    volumeScale.place(x = 430, y = 15)
    VOLable = Label(controlWindow, text = "Volume", bg = "grey")
    VOLable.place(x = 440, y = 120)

    root.mainloop()