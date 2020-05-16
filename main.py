from display import Display
from universe import Universe
from stats import plot_multiple
from settings import settings
from brain import RandomSmartBrain, RandomSmartBrain2, SmartBrain

'''


    # RandomSmartBrain
    'randomsmartbrain_eat_threshold': 10,
    'randomsmartbrain_move_threshold': 4,
    'randomsmartbrain_reproduce_distance_threshold': 10,


settings['brain_prototype'] = RandomSmartBrain(actions=None,
                                               eat_threshold=settings['randomsmartbrain_eat_threshold'],
                                               move_threshold=settings['randomsmartbrain_move_threshold'],
                                               reprod_energy_threshold=settings['randomsmartbrain_reproduce_distance_threshold'])
settings['breed_type'] = RandomSmartBrain.smart_breed
'''

'''
Bons paramètres pour des SmartBrain qui survivent

settings['brain_prototype'] = SmartBrain(actions=None, eat_threshold=6, move_threshold=1, reprod_energy_threshold=40)
settings['breed_type'] = SmartBrain.smart_breed
'''

settings['nb_blobs'] = 400

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
plot_multiple(stats, ['n', 'born', 'eat_threshold', 'move_threshold', 'reprod_energy_threshold'])
