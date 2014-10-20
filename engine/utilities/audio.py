import pygame
from pygame.locals import *

try:
    import android
except ImportError:
    android = None

try:
    import pygame.mixer as mixer
except ImportError:
    import android.mixer as mixer

class Audio(object):
    def __init__(self):
        try:
            mixer.init(44100, -16, 2, 1024)
        except:
            pass
        
    def sound(self, pathfile):
        return mixer.Sound(pathfile)

    def play(self, soundObject):
        if not mixer.get_busy():
            soundObject.play()

    def music(self, pathfile):
        mixer.music.load(pathfile)
        
    def loop(self):
        if android:
           if mixer.music_channel.get_busy()==False:
              mixer.music.play()
        else:
           if mixer.music.get_busy()==False:
              mixer.music.play()












        

