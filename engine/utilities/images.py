import pygame
from pygame.locals import *

class Image(object):
    def __init__(self):
        self.images = {}

    def load(self, name, pathfile, alpha=True):
        if alpha == True: img = pygame.image.load(pathfile).convert_alpha()
        else: img = pygame.image.load(pathfile).convert()
        self.images.update({name: img})

    def scale(self, name, scale_width=1, scale_height=1):
        img = self.images[name]
        self.images[name] = pygame.transform.scale(img,
                                                    (int(img.get_width()*scale_width),
                                                     int(img.get_height()*scale_height)))
        
    def get_image(self, name):
        try:
            return self.images[name]
        except:
            return None
        
