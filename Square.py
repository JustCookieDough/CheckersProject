import pygame as p
import Variables as v

class Square():  # board square
    def __init__(self, x, y):
        self.x = x
        self.y = y
        if (self.x + self.y) % 2 == 0:   #creates checkerboard pattern
            self.color = (222, 71, 51)
        else:
            self.color = (235, 145, 35)

    def draw(self, screen): # draws square
        p.draw.rect(screen, self.color, (self.x*v.SQ_SIZE, self.y*v.SQ_SIZE, v.SQ_SIZE, v.SQ_SIZE))