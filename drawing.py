#!/usr/bin/python

import pygame
from pygame.draw import *

class Tile(pygame.Surface):

    def __init__(self, width, height):
        pygame.Surface.__init__(self, width, height)

        self.draw()

    def draw(self):
        rect(self, (50, 50, 255), (0, 0, self.width, self.height), 4)


