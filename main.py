import pygame
from pygame.locals import *
from pygame.time import *
import helper

pygame.init()

c = Clock()
d = pygame.display.set_mode(helper.get_screen_size(), FULLSCREEN | HWACCEL)
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

while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == K_q:
                pygame.quit()
                exit()
            elif event.key in [K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8]:
                g.animate([K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8].index(event.key))
    g.update()
    d.fill((0, 0, 0))
    g.draw(d)
    pygame.display.update()
    c.tick(60)
