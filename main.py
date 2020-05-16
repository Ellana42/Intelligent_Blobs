from display import Display
from universe import Universe
from stats import plot, plot_multiple

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
plot_multiple(stats, ['eat_threshold', 'move_threshold', 'born'])
