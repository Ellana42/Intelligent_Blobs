from display import Display
from universe import Universe
from stats import plot

universe = Universe()
displayer = Display(universe)

running = True
while running:
    if universe.time % 3 == 0:
        inp = displayer.show()
    if inp == 'quit':
        running = False
        stats = universe.stats
        plot(stats, 'born')
    universe.tick()
