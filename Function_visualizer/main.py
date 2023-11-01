import matplotlib.pyplot as plt
import matplotlib.ticker as tck
from helper import pi_axis_formatter
from random import randint
from matplotlib.animation import FuncAnimation
import math
import numpy as np
import os


# pylint: disable=line-too-long
class GUI:
    def __init__(self):
        self.function_choice = ''

    def gui_start(self):
        os.system("CLS")
        print(
            "\n####################################### -- FUNCTION VISUALIZER -- ##################################################")
        print(
            "A tool with which the user can visaluze different functions / curves of their choice by entering the input values.")
        print("The following functions can be visualized:")
        print("1 : Circle\n2 : Parabola\n3 : Sine function\n4 : Cosine function\n0 : Exit")
        print(
            "######################################################################################################################")
        func_choice = int(input("Please enter your selection: "))
        self.function_choice = func_choice
        return self.function_choice


class Plotter(GUI):
    # def __init__(self, selection):
    def __init__(self):
        super(Plotter, self).__init__()
        self.user_selection = self.gui_start()
        self.plot_titles = {1: "Circle", 2: "Parabola", 3: "Sine Function", 4: "Cosine Function"}

        self.x_values = []
        self.y_values = []
        self.h = 0
        self.k = 0
        self.xs = []
        self.ys = []
        self.ax_allowance = 2
        self.prev_frame_numer = None

        self.len_frames = 0
        self.fig, self.ax = plt.subplots()

    def start(self):
        if self.user_selection == 1:
            self.__circle()
        elif self.user_selection == 2:
            self.__parabola()
        elif self.user_selection == 3:
            self.__sine_function()
        elif self.user_selection == 4:
            self.__cosine_function()
        elif self.user_selection == 0:
            self.__exit_program()
        else:
            print("Invalid choice!. Please enter numbers between 1 to 4\n")
            self.__retry()

    def __init_prompt(self):
        input_args = str(input("Enter the X-values separated by (, ): "))
        input_args_list = input_args.split(",")
        try:
            x = [int(ii) for ii in input_args_list]
            self.len_frames = len(x)
        except ValueError:
            x = [float(ii) for ii in input_args_list]
            self.len_frames = len(x)
            x = np.append(x, [math.ceil(np.max(x))])
            isTruncation = str(input(
                "There are decimal values in the input arrays, would you like to visualize data with truncation? (Y/N): "))
            if isTruncation.lower() == 'y':
                self.len_frames = len(x)
        x = np.sort(np.array(x, dtype='f'))
        return x

    def __plot_with_animation(self):
        ani = FuncAnimation(self.fig, self.__animate, fargs=(self.xs, self.ys), frames=self.len_frames, interval=50,
                            repeat=False)
        plt.show()

    def __circle(self):
        self.x_values = self.__init_prompt()
        center = str(input("Enter the co-ordinates for the center of the circle (h,k). Default (0,0): ")).split(" ")
        self.h, self.k = float(center[0]), float(center[-1])
        if (self.h == 0) and (self.k == 0):
            self.pos_y_values = np.array(list(map(math.sqrt, pow(max(self.x_values), 2) - pow(self.x_values, 2))))
        else:
            self.x_values += self.h
            radius = math.ceil(max(self.x_values)) - self.h
            self.pos_y_values = np.array(list(map(math.sqrt, pow(radius, 2) - pow(self.x_values-self.h, 2))))
            self.pos_y_values += self.k
        self.neg_y_values = -self.pos_y_values + 2*self.k
        self.y_values = list(self.pos_y_values) + list(self.neg_y_values)
        self.x_values = list(self.x_values)
        print("X-values:", self.x_values, '\n')
        print("Y-values:", self.y_values, '\n')

        self.__plot_with_animation()

    def __parabola(self):
        self.x_values = self.__init_prompt()
        self.a_value = float(input("Enter a value for 'a', the focus of the Parabola: "))
        center = str(input("Enter the co-ordinates for the apex of the Parabola (h k): ")).split(" ")
        self.h, self.k = float(center[0]), float(center[-1])
        self.y_values = (np.array(list(pow(self.x_values - self.h, 2))) / (4 * self.a_value)) + self.k
        self.y_values = list(self.y_values)
        self.x_values = list(self.x_values)
        self.__plot_with_animation()

    def __sine_function(self):
        self.x_values = self.__init_prompt()
        self.y_values = list(map(math.sin, self.x_values))
        self.y_values = list(self.y_values)
        self.x_values = list(self.x_values)
        self.__plot_with_animation()

    def __cosine_function(self):
        self.x_values = self.__init_prompt()
        self.y_values = list(map(math.cos, self.x_values))
        self.y_values = list(self.y_values)
        self.x_values = list(self.x_values)
        self.__plot_with_animation()

    def __animate(self, i, xs, ys):
        self.xs.append(self.x_values[i])
        self.ax.clear()
        if self.user_selection == 1:
            self.ys.append([self.y_values[i], self.y_values[len(self.x_values) + i]])
            self.ax.axis('equal')
            self.ax.plot(self.h, self.k, 'ko')
            self.ax.text(self.h - 0.5, self.k, f'Center{self.h, self.k}', fontsize=8, ha='right')

        elif self.user_selection == 2:
            self.ys.append(self.y_values[i])
            self.ax.plot(self.h, self.a_value + self.k, 'ko')
            self.ax.text(self.h - 0.5, self.a_value + self.k, f'Focus{self.h, self.a_value + self.k}',
                         fontsize=8, ha='right')
            self.ax.plot(self.h, self.k, 'ko')
            self.ax.text(self.h - 0.5, self.k, f'Vertex{self.h, self.k}',
                         fontsize=8, ha='right')

        else:
            self.ys.append(self.y_values[i])

        self.ax.grid()
        self.ax.plot(xs, ys)

        self.ax.set_title(self.plot_titles[self.user_selection], fontdict={'fontsize': 'x-large', 'fontweight': 'bold'})
        self.ax.set_xlabel("X-Values")
        self.ax.set_ylabel("Y-Values")

        if self.user_selection == 3 or self.user_selection == 4:
            ticklen = np.pi / 2
            self.ax.xaxis.set_major_formatter(tck.FuncFormatter(pi_axis_formatter))
            self.ax.xaxis.set_major_locator(tck.MultipleLocator(ticklen))

            self.ax.set_xlim([min(self.x_values) - 1, max(self.x_values) + 1])
            self.ax.set_ylim([-1.5, 1.5])
        else:
            self.ax.set_xlim([min(self.x_values) - self.ax_allowance, max(self.x_values) + self.ax_allowance])
            self.ax.set_ylim([int(min(self.y_values) - self.ax_allowance), int(max(self.y_values)) + self.ax_allowance])

    def __retry(self):
        retry = ''
        while retry.lower() != 'n':
            retry = input("Would you like to try again? (Y/N): ")
            if retry.lower() == 'y':
                self.gui_start()
            else:
                print("Invalid choice!. Please enter (Y/N)\n")
        self.__exit_program()

    @staticmethod
    def __exit_program():
        print("\nThanks for using the Function plotter. Hope it helped ! :)")
        quit()


if __name__ == "__main__":
    gui = GUI()
    # gui.gui_start()
    plotr = Plotter()
    plotr.start()

# User-defined input from console
# input_args = str(input("Enter the X-values separated by (, ): "))
# input_args_list = input_args.split(",")
# x = [int(ii) for ii in input_args_list]

# X-values as numpy arrays
# x = np.arange(-10, 10, 1)
# frames_len = len(x)
# y = list(map(math.sin, x))
# xs = []
# ys = []

# fig, ax = plt.subplots()

# # function that draws each frame of the animation
# def animate(i, xs, ys):
#     xs.append(x[i])
#     ys.append(y[i])

#     ax.clear()
#     ax.grid()
#     ax.plot(xs, ys)
#     ax.set_xlim([-1000,1000])
#     ax.set_ylim([-2,2])


# ani = FuncAnimation(fig, animate, fargs=(xs, ys), frames=frames_len, interval=200, repeat=False)
# plt.show()