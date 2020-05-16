from display import Display
from universe import Universe
from stats import plot_multiple
from settings import settings
from brain import RandomBrainGenerator, SmmartBrainGenerator, RandomBrain, SmartBrain, RandomBrainGeneratorCentered


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


def run_until(max_time, settings, display=True):
    universe = Universe(settings)
    if display:
        displayer = Display(universe)

    running = True
    while running:
        if display:
            inp = displayer.show()
            if inp == 'quit':
                running = False
        universe.tick()
        if universe.time > max_time:
            running = False

    if display:
        displayer.quit()

    return universe


cumulated_stats = []

for factor in [1.0, 0.8, 0.5, 0.2, 0.1]:
    universe1 = run_until(max_time=300, settings=settings, display=True)
    stats = universe1.stats
    cumulated_stats.extend(stats)
    last_stat = stats.pop(-1)
    settings['brain_generator'] = RandomBrainGeneratorCentered(
        eat_threshold=last_stat['eat_threshold'],
        move_threshold=last_stat['move_threshold'],
        reprod_energy_threshold=last_stat['reprod_energy_threshold'],
        var_eat_threshold=0.4 * factor,
        var_move_threshold=0.4 * factor,
        var_reprod_energy_threshold=0.3 * factor
    )

plot_multiple(cumulated_stats, ['n', 'born', 'eat_threshold', 'move_threshold', 'reprod_energy_threshold'])

