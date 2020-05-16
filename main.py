from display import Display
from universe import Universe
from stats import plot, plot_multiple
from stats import plot
from settings import settings
from brain import RandomSmartBrain, RandomSmartBrain2, SmartBrain

settings['brain_prototype'] = RandomSmartBrain(actions=None,
                                               eat_threshold=settings['randomsmartbrain_eat_threshold'],
                                               move_threshold=settings['randomsmartbrain_move_threshold'],
                                               reprod_distance_threshold=settings['randomsmartbrain_reproduce_distance_threshold'])

settings['breed_type'] = RandomSmartBrain.smart_breed

settings['brain_prototype'] = SmartBrain(actions=None, eat_threshold=4, move_threshold=0.4, reprod_distance_threshold=3)

settings['breed_type'] = SmartBrain.smart_breed

universe = Universe(settings)
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
plot_multiple(stats, ['n', 'born', 'eat_threshold', 'move_threshold'])
