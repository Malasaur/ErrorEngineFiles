from datetime import datetime
from random import randint
from time import sleep
import pygame, os

os.chdir("C:\\Users\\Public\\ERRENG")

def play_audio(file):
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

start, end = "30/05/24 08:00:00", "30/05/24 08:50:00"
minTime, maxTime = 120, 300

start = datetime.strptime(start, "%d/%m/%y %H:%M:%S")
end = datetime.strptime(end, "%d/%m/%y %H:%M:%S")
now = datetime.now()
if now < end and not os.path.isfile("marconi164_done.sig"):
    while now < start:
        now = datetime.now()
    while now < end:
        now = datetime.now()
        sleep(randint(minTime, maxTime))
        play_audio("marconi164_sound.wav")
        open("marconi164_done.sig", "w").write("...")
