from display import Display
from universe import Universe

universe = Universe()
displayer = Display(universe)
running = True

while running:
    inp = displayer.show()
    if inp == 'quit':
        running = False
    universe.tick()
