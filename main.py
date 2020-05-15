from display import Display
from universe import Universe
from stats import plot

universe = Universe()
displayer = Display(universe)

running = True
while running:
    if universe.time % 1 == 0:
        inp = displayer.show()
    if inp == 'quit':
        running = False
    universe.tick()

displayer.quit()
stats = universe.stats
plot(stats, 'eat_threshold')
plot(stats, 'move_threshold')
plot(stats, 'born')
