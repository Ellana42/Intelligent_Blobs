import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


class Animate:
    def __init__(self):
        self.fig, self.ax = plt.subplots()
        self.x = np.arange(0, 2 * np.pi, 0.01)
        self.line, = self.ax.plot(self.x, np.sin(self.x))
        self.ani = animation.FuncAnimation(
            self.fig, self.animate, interval=2, blit=True, save_count=50)
        plt.show()

    def animate(self, i):
        self.line.set_ydata(np.sin(self.x + i / 100))  # update the data.
        return self.line,


anime = Animate()
