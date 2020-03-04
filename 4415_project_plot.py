import sys
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from matplotlib.ticker import FormatStrFormatter


style.use('fivethirtyeight')
fig  = plt.figure()
ax1 = fig.add_subplot(1,1,1)
ax1.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))



def animate(i):
    #read dataftom file
    my_dict = {}

    with open('plot_this.txt','r') as plotting_file:
        for line in plotting_file.readlines():
            y_vals = []
            x_vals = []
            name, useless, value  = line.partition(',')

            #print(float(value))
            my_dict[name] = float(value)

    #ax1.clear()
    ax1.cla()
    ax1.bar(list(my_dict.keys()),list(my_dict.values()),width=0.09)
    ax1.set_xlabel("x axis",fontsize=1)

#basically after 500ms, update my graph
ani = animation.FuncAnimation(fig, animate, interval=100)
plt.show()

animate(2)