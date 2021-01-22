import os
try:
    os.system("pip3 uninstall pygame")
except:
    pass
os.system("pip3 install mutagen")
os.system("pip3 install db-sqlite3")
os.system("pip3 install tk")
os.system("sudo apt-get install python3-tk")
os.system("sudo apt-get install python-dev libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev libsdl1.2-dev libsmpeg-dev python-numpy subversion libportmidi-dev ffmpeg libswscale-dev libavformat-dev libavcodec-dev libfreetype6-dev")
os.system("pip3 install pygame==1.9.6")