import matplotlib.pyplot as plt
from random import randint
from matplotlib.animation import FuncAnimation
import math
import numpy as np

# User-definde input from console
input_args = str(input("Enter the X-values separated by (, ): "))
input_args_list = input_args.split(",")
x = [int(ii) for ii in input_args_list]

# X-values as numpy arrays
x = np.arange(-10, 10, 1)
frames_len = len(x)
y = list(map(math.sin, x))
xs = []
ys = []

fig, ax = plt.subplots()

# function that draws each frame of the animation
def animate(i, xs, ys):
    xs.append(x[i])    
    ys.append(y[i])

    ax.clear()
    ax.grid()
    ax.plot(xs, ys)
    ax.set_xlim([-1000,1000])
    ax.set_ylim([-2,2])
    

ani = FuncAnimation(fig, animate, fargs=(xs, ys), frames=frames_len, interval=200, repeat=False)
plt.show()
