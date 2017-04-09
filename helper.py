import pygame

screen_size = None


def load_ff():
    image = pygame.image.load("images/family-feud.png")
    return pygame.transform.scale(image, (get_ff_size(image)))


def get_ff_size(surf):
    height_available = get_screen_size() - get_answer_size() * 4
    scale = height_available / surf.get_size()[1]
    return surf.get_size[0] * scale, surf.get_size[1] * scale


def get_screen_size():
    global screen_size
    if screen_size is None:
        screen_size = pygame.display.Info()
    return screen_size.current_w, screen_size.current_h


def get_answer_size():
    image_size = 900, 225
    ratio = get_screen_size()[0] / 900.0 /2
    return image_size[0] * ratio, image_size[1] * ratio


class ImageManager:

    def __init__(self):
        self.loaded_images = {}

    def has(self, num, x):
        if ("im_" + str(num) + "_" + str(x)) in self.loaded_images.keys():
            return True
        return False

    def get(self, num, x):
        return self.loaded_images["im_" + str(num) + "_" + str(x)]

    def load(self, num, x):
        if x > 15:
            self.loaded_images["im_" + str(num) + "_" + str(x)] = pygame.image.load("images/num0/00" + str(x) + ".png")
        elif x < 10:
            self.loaded_images["im_" + str(num) + "_" + str(x)] = pygame.image.load("images/num" + str(num) + "/000" + str(x) + ".png")
        else:
            self.loaded_images["im_" + str(num) + "_" + str(x)] = pygame.image.load("images/num" + str(num) + "/00" + str(x) + ".png")