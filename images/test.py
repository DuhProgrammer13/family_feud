import pygame
from pygame.locals import *
from pygame.image import load
import time

d = pygame.display.set_mode((1200, 300), pygame.FULLSCREEN)
c = pygame.time.Clock()

images = []


def get_image_name(i):
    if i >= 10:
        return "images/00" + str(i) + ".png"
    return "images/000" + str(i) + ".png"


for i in range(1, 30):
    images.append(pygame.image.load(get_image_name(i)))

i = 0
waitNext = False
while True:
    if waitNext:
        time.sleep(3)
        waitNext = False
    i += 1
    if i >= len(images):
        i = 0
        time.sleep(3)
        waitNext = True
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_q:
                pygame.quit()
                exit()

    c.tick(60)
    d.fill((255, 255, 255))
    d.blit(images[i], (0, 0))
    pygame.display.update()
