from pygame import *


class Display:
    def __init__(self, universe):
        self.universe = universe
        self.size = self.universe.universe_size
        init()
        self.window = display.set_mode((self.size, self.size))
        self.background = self.make_background()

    def show(self):
        self.window.blit(self.background, (0, 0))
        events = event.get()
        inp = ''
        for evt in events:
            if evt.type == KEYDOWN and evt.key == K_ESCAPE:
                inp = 'quit'
        for blob in self.universe.blobs:
            draw.circle(self.window, (0, 128, 129),
                        (int(blob.x), int(blob.y)), int(blob.energy) // 2)
        display.update()
        return inp

    def make_background(self):
        background = Surface(
            (self.size, self.size))
        background.convert()
        background.fill((250, 250, 250))
        return background
