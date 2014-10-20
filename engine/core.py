#!/usr/bin/python
import pygame
import math
import os
from pygame.locals import *
from sys import exit

try:
    import android
except ImportError:
    android = None

from .utilities.ouyacontroller import *
from .utilities.images import *
from .utilities.events import *
from .utilities.audio import *

class Engine(object):
    def __init__(self, size=(1280, 720), FPS=32):
        pygame.init()
        pygame.display.init()
        
        try:
            info = pygame.display.Info()        
            diag = math.hypot(info.current_w,
                              info.current_h) / android.get_dpi()
            
            width, height = (info.current_w, info.current_h)
            self.scale_width = width / float(size[0])
            self.scale_height = height / float(size[1])
            self.screen = pygame.display.set_mode((width, height))

            print(width, height, size)
            print(self.scale_width, self.scale_height)
            
        except AttributeError:
            self.screen = pygame.display.set_mode(size)
            self.scale_width = 1
            self.scale_height = 1

        if android:
            android.init()

        self.red  = pygame.color.Color('red')
        self.black  = pygame.color.Color('black')
        self.width  = self.screen.get_width()
        self.height = self.screen.get_height()
        self.clock  = pygame.time.Clock()
        self.FPS    = FPS
        self.image  = Image()
        self.audio  = Audio()
        self.events = EventHandler()
        self.controller = OuyaController()

        self.safe_percentage = 0.05
        self.vertical_safe_zone = pygame.Surface((int(self.width * self.safe_percentage), int(self.height)))
        self.vszwidth = self.vertical_safe_zone.get_width()
        self.vszheight = self.vertical_safe_zone.get_height() * self.safe_percentage
        self.horizontal_safe_zone = pygame.Surface((int(self.width - 2 * self.vszwidth), int(self.vszheight)))

        self.sz_left = (0,0)
        self.sz_right = (self.width / self.scale_width - self.vszwidth / self.scale_width, 0)
        self.sz_up = (self.vszwidth / self.scale_width, 0)
        self.sz_down = (self.vszwidth / self.scale_width,
                        self.height / self.scale_height - self.vszheight / self.scale_height)

        self.vertical_safe_zone.fill(self.red)
        self.vertical_safe_zone.set_alpha(92)
        self.horizontal_safe_zone.fill(self.red)
        self.horizontal_safe_zone.set_alpha(92)
        
        if android:
            if android.check_pause():
                android.wait_for_resume()
                
    def clear(self):
        self.play_music()
        self.screen.fill(self.black)
        self.events.get_events()
        if android:
            self.controller.get_events()

    def blit(self, img, position=(0,0)):
        self.screen.blit(img, (position[0] * self.scale_width,
                               position[1] * self.scale_height))
        
    def update(self):
        if android:
            self.controller.update()
            if android.check_pause():
                android.wait_for_resume()

        self.events.update()
        pygame.display.flip()
        self.clock.tick(self.FPS)

    def back(self, button=None):
        if android:
            if button == None:
                if self.controller.down(self.controller.BUTTON_A):
                    return True
            else:
                if self.controller.down(button):
                    return True
            
        if self.events.down(K_ESCAPE):
            return True
        else:
            return False

    def stop(self, button=None):
        if android:
            if button == None:
                if self.controller.down(self.controller.BUTTON_A):
                    pygame.quit()
                    exit()
            else:
                if self.controller.down(button):
                    pygame.quit()
                    exit()
                
        if self.events.down(K_ESCAPE):
            pygame.quit()
            exit()

    def get_sound(self, pathfile):
        return self.audio.sound(pathfile)

    def play_sound(self, sound):
        self.audio.play(sound)

    def get_music(self, pathfile):
        self.audio.music(pathfile)
        return None
    
    def load_music(self, pathfile):
        self.audio.music(pathfile)
        return None
        
    def play_music(self, music=None):
        self.audio.loop()
        
    def load_image(self, pathfile, name="placeholder", alpha=True):
        self.image.load(name, pathfile, alpha)
        self.image.scale(name, self.scale_width, self.scale_height)
        return self.image.get_image(name)
        
    def get_image(self, name):
        return self.image.get_image(name)

    def draw_circle(self, pos, radius, width):
        pygame.draw.circle(self.screen, self.white, pos, radius, width)

    def up(self, button, player=0):
        return self.controller.up(button, player)
    
    def down(self, button, player=0):
        return self.controller.down(button, player)
    
    def motion(self, button, player=0):
        return self.controller.motion(button, player)

    def get_text(self, font, text, color="white"):
        try:
            color = pygame.color.Color(color)
        except ValueError:
            pass
        return font.render(text, 0, color)

    def get_font(self, pathfile, size, color="black"):
        font_size = int((size * self.scale_width +
                         size * self.scale_height) / 2.0)
        
        if pathfile != None and os.path.exists(pathfile):
            font = pygame.font.Font(pathfile, font_size)
        else:
            font = pygame.font.Font(None, font_size)

        return font

    def render_text(self, text, pos=(0,0)):
        self.blit(text, pos)

    def safe_zone(self):
        self.blit(self.vertical_safe_zone, self.sz_left)
        self.blit(self.vertical_safe_zone, self.sz_right)
        self.blit(self.horizontal_safe_zone, self.sz_up)
        self.blit(self.horizontal_safe_zone, self.sz_down)









        
