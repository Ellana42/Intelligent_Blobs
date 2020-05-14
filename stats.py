import matplotlib.pyplot as plt

stat_names = ['n_move', 'n_eat', 'n_reproduce', 'n_rotate', 'n', 'die', 'born']


def plot(stats, chosen_stat):
    stat = [stat[chosen_stat] for stat in stats]
    time = range(len(stat))
    plt.plot(time, stat)
    plt.show()
