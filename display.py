from pygame import *
from math import sin, cos


class Display:
    def __init__(self, universe):
        self.universe = universe
        self.size = self.universe.universe_size
        init()
        self.window = display.set_mode((self.size, self.size))
        self.background = self.make_background()
        self.food = self.make_food()

    def show(self):
        self.window.blit(self.background, (0, 0))
        self.window.blit(
            self.food, (self.universe.food.x, self.universe.food.y))
        events = event.get()
        inp = ''
        for evt in events:
            if evt.type == KEYDOWN and evt.key == K_ESCAPE:
                inp = 'quit'
        for blob in self.universe.blobs:
            radius = min(int(blob.energy) // 10, 10)
            draw.circle(self.window, (0, 128, 129),
                        (self.size // 2 + int(blob.x), self.size // 2 + int(blob.y)), radius)

            draw.circle(self.window, (255, 255, 255), (self.size // 2 + int(blob.x + cos(blob.heading) * radius),
                                                       self.size // 2 + int(blob.y + sin(blob.heading) * radius)), 2)
        display.update()
        return inp

    def make_background(self):
        background = Surface(
            (self.size, self.size))
        background.convert()
        background.fill((0, 0, 0))
        return background

    def make_food(self):
        food = Surface((self.size * 2, self.size * 2))
        for y in range(self.size)[::-1]:
            intensity = int(self.universe.food.depletion(
                0, y) / 10 * 255)
            intensity = min(255, intensity)
            draw.circle(food, (intensity, 0, 0),
                        (self.size // 2, self.size // 2), y)
        return food


# food_bit = Surface((1, 1))
#         food_bit.convert()
#         for y in range(-self.size * 2, self.size * 2):
#             for x in range(-self.size * 2, self.size * 2):
#                 intensity = int(self.universe.food.depletion(x, y) * 25.5)
#                 food_bit.fill((intensity, 0, 0))
#                 food.blit(food_bit, (x + self.size // 2, y + self.size // 2))
