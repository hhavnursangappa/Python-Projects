import matplotlib.pyplot as plt
from random import randint
from matplotlib.animation import FuncAnimation
import math
import numpy as np
import os

class GUI:
    def __init__(self):
        self.funcction_choice = None
    
    def start(self):
        os.system("CLS")
        print("\n####################################### -- FUNCTION VISUALIZER -- ##################################################")
        print("A tool with which the user can visaluze different functions / curves of their choice by entering the input values.")
        print("The following functions can be visualized:")
        print("1 : Circle\n2: Parabola\n3: Sine function\n4: Cosine function\n0: Exit")
        print("######################################################################################################################")
        func_choice = int(input("Please enter your selection: "))
        
        self.function_choice = func_choice
        return self.function_choice


class Plotter:
    def __init__(self, selection):
        self.plot_titles = {1: "Circle", 2: "Parabola", 3: "Sine Function", 4:"Cosine Function"}
        self.user_selection = selection
        
        self.x_values = []
        self.y_values = []
        self.xs = []
        self.ys = []
        self.ax_allowance = 10
        
        self.len_frames = 0
        self.fig, self.ax = plt.subplots()

    def start(self):
        if (self.user_selection == 1):
            self.__circle()
        elif (self.user_selection == 2):
            self.__parabola()
        elif (self.user_selection == 3):
            self.__sine_function()
        elif (self.user_selection == 4):
            self.__cosine_function()
        elif (self.user_selection == 0):
            self.__exit_program()
        else:
            print("Invalid choice!. Please enter numbers between 1 to 4\n")
            self.__retry()
    
    def __init_prompt(self):
        input_args = str(input("Enter the X-values separated by (, ): "))
        input_args_list = input_args.split(",")
        x = [int(ii) for ii in input_args_list]
        self.len_frames = len(x)
        return np.array(x)

    def __plot_with_animation(self):
        self.ax.plot([0,0], 'ko')
        self.ax.text(0,0, 'center (0,0)', fontsize=8, ha='right')
        ani = FuncAnimation(self.fig, self.__animate, fargs=(self.xs, self.ys), frames=self.len_frames, interval=50, repeat=False)
        plt.show()
    
    def __circle(self):
        self.x_values = self.__init_prompt()
        
        self.pos_y_values = np.array(list(map(math.sqrt, pow(max(self.x_values), 2) - pow(self.x_values, 2))))
        self.neg_y_values = -self.pos_y_values
        
        self.y_values = list(self.pos_y_values) + list(self.neg_y_values)
        self.x_values = list(self.x_values)

        self.__plot_with_animation()
        
    def __animate(self, i, xs, ys):
        self.xs.append(self.x_values[i])    
        self.ys.append([self.y_values[i], self.y_values[len(self.x_values)+i]])

        self.ax.clear()
        self.ax.axis('equal')
        self.ax.grid()        
        
        self.ax.plot(xs, ys)
        self.ax.set_title(self.plot_titles[self.user_selection], fontdict={'fontsize':'x-large','fontweight': 'bold'})
        self.ax.set_xlabel("X-Values")                       
        self.ax.set_ylabel("Y-Values")
        self.ax.set_xlim([min(self.x_values)-self.ax_allowance, max(self.x_values)+self.ax_allowance])
        self.ax.set_ylim([int(min(self.y_values)-self.ax_allowance), int(max(self.y_values))+self.ax_allowance])  

    def __retry(self):
        retry = input("Would you like to try again? (Y/N): ")
    
    def __exit_program(self):
        quit()


if __name__ == "__main__":
    gui = GUI()
    choice = gui.start()
    plotr = Plotter(choice)
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