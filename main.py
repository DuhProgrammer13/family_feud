import pygame
from pygame.locals import *
from pygame.time import *
import helper
import threading
import json
import urllib
import time

pygame.init()

c = Clock()
d = pygame.display.set_mode(helper.get_screen_size(), FULLSCREEN | HWACCEL)
running = True
print helper.get_screen_size()
im = helper.ImageManager()


def load_images(num):
    images = []
    for x in range(1, 31):
        if im.has(num, x):
            images.append(im.get(num, x))
        else:
            im.load(num, x)
            images.append(im.get(num, x))
    return images


class Answer(pygame.Surface):

    def __init__(self, width, height, num, answer):
        pygame.Surface.__init__(self, (width, height))
        if len(answer) > 0:
            self.images = load_images(num)
        for image in range(len(self.images)):
            self.images[image] = pygame.transform.scale(self.images[image], (self.get_size()[0], self.get_size()[1]))
        self.blit(self.images[0], (0, 0))
        self.animating = False
        self.current_image = 0

    def update(self):
        if self.animating:
            self.current_image += 1
            if self.current_image == len(self.images):
                self.animating = False
                self.current_image = 0
                pygame.Surface.__init__(self, (self.get_size()[0], self.get_size()[1]))
                self.blit(self.images[29], (0, 0))
            else:
                self.blit(self.images[self.current_image], (0, 0))

    def animate(self):
        self.animating = True


class Game:

    def __init__(self):
        self.answer_strings = ["mj" for _ in range(0, 8)]
        self.answers = []
        self.build_answers()
        self.wrong_answers = 0
        self.size = helper.get_screen_size()

    def build_answers(self):
        x = 0
        for answer in self.answer_strings:
            x += 1
            self.answers.append(Answer(helper.get_answer_size()[0], helper.get_answer_size()[1], x, answer))

    def update(self):
        for answer in self.answers:
            answer.update()

    def animate(self, answer_to_animate):
        self.answers[answer_to_animate].animate()

    def draw(self, display):
        for x in range(8):
            if x < 4:
                display.blit(self.answers[x], (0,
                                               helper.get_screen_size()[1] -
                                               helper.get_answer_size()[1] * 4 +
                                               helper.get_answer_size()[1] * x))
            else:
                display.blit(self.answers[x], (helper.get_answer_size()[0],
                                               helper.get_screen_size()[1] -
                                               helper.get_answer_size()[1] * 4 +
                                               helper.get_answer_size()[1] * (x - 4)))

g = Game()


class myThread (threading.Thread):
    def __init__(self, game):
        threading.Thread.__init__(self)
        self.game = game
        self.animating = []
        self.animated = []

    def run(self):
        while running:
            try:
                url = "http://192.168.1.101/api/game"
                data = json.load(urllib.urlopen(url))
                for _answer in data["answers"]:
                    answer = int(_answer["id"])
                    if answer not in self.animating and answer not in self.animated and boolean(answer["answered"]):
                        print answer
                        print _answer
                        self.animating.append(answer)
                        self.game.animate(int(answer))
                time.sleep(0.5)
            except Exception as e:
                tim.sleep(1)


thread = myThread(g)
thread.start()


while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == K_q:
                running = False
                pygame.quit()
                exit()
            elif event.key in [K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8]:
                g.animate([K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8].index(event.key))
    g.update()
    d.fill((0, 0, 0))
    g.draw(d)
    pygame.display.update()
    c.tick(60)
