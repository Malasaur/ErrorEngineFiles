from datetime import datetime
from random import randint
from time import sleep
import pygame, os

os.chdir("C:\\Users\\Public\\ERRENG\\Files")

def play_audio(file):
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

start, end = "03/06/24 08:50:00", "03/06/24 09:40:00"
minTime, maxTime = 60, 300

start = datetime.strptime(start, "%d/%m/%y %H:%M:%S")
end = datetime.strptime(end, "%d/%m/%y %H:%M:%S")
now = datetime.now()
if now < end and not os.path.isfile("marconi164_done2.sig"):
    while now < start:
        now = datetime.now()
    while now < end:
        now = datetime.now()
        sleep(randint(minTime, maxTime))
        play_audio("marconi164_exercise.mp3")
        open("marconi164_done2.sig", "w").write("...")
