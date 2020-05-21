import matplotlib.pyplot as plt


def plot_multiple(stats, chosen_stats):
    plt.style.use('ggplot')
    time = range(len(stats))
    fig, axes = plt.subplots(len(chosen_stats), 1)
    fig.subplots_adjust(hspace=1)
    i = 0
    for axe in axes:
        stat = [stat[chosen_stats[i]] for stat in stats]
        axe.plot(time, stat)
        axe.set_xlabel('time')
        axe.set_ylabel(chosen_stats[i])
        i += 1
    plt.show()
