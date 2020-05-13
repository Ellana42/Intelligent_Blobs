from display import Display
from universe import Universe

universe = Universe()
displayer = Display(universe)

running = True
while running:
    if universe.time % 3 == 0:
        inp = displayer.show()
    if inp == 'quit':
        running = False
    universe.tick()
