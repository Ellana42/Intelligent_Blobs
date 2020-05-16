from display import Display
from universe import Universe
from stats import plot_multiple
from settings import settings
from brain import RandomBrainGenerator, SmmartBrainGenerator, RandomBrain, SmartBrain


'''
Bons paramètres pour des SmartBrain qui survivent

settings['brain_generator'] = SmartBrainGenerator(eat_threshold=6, move_threshold=1, reprod_energy_threshold=40)
settings['breed_type'] = SmartBrain.smart_breed
'''

'''


    # RandomSmartBrain
    'randomsmartbrain_eat_threshold': 10,
    'randomsmartbrain_move_threshold': 4,
    'randomsmartbrain_reproduce_distance_threshold': 10,

'''
settings['brain_generator'] = RandomBrainGenerator(max_eat_threshold=6, max_move_threshold=1, max_reprod_energy_threshold=40,
                                                   var_eat_threshold=0.4, var_move_threshold=0.4, var_reprod_energy_threshold=0.3)
settings['brain_generator'] = RandomBrainGenerator(max_eat_threshold=10, max_move_threshold=10, max_reprod_energy_threshold=200,
                                                   var_eat_threshold=0.4, var_move_threshold=0.4, var_reprod_energy_threshold=0.3)
settings['breed_type'] = RandomBrain.smart_breed


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
