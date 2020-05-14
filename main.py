from display import Display
from universe import Universe
from stats import plot

universe = Universe()
displayer = Display(universe)

running = True
while running:
    inp = displayer.show()
    if inp == 'quit':
        running = False
        stats = universe.stats
        plot(stats, 'n')
    universe.tick()
