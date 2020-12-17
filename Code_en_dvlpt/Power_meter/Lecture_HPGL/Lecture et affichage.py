import numpy as np
import matplotlib.pyplot as plt

import matplotlib.pyplot as plt

import re

text = ";SC0,2047,0,2193;;SP1;;PA150,150;PD;PA150,1814;PU;PA310,1814;PD;PA310,150;"
separators = ";", ","
list=[str]

def custom_split(sepr_list, str_to_split):
    # create regular expression dynamically
    regular_exp = '|'.join(map(re.escape, sepr_list))
    return re.split(regular_exp, str_to_split)

print(text)
a = custom_split(sepr_list, str_to_split)
print(type(text))
print(text)


def scalar_screen():
    i = 0
    # parti scalaire permettant de créer le quadrillage

    # while True:
    #     c = HPGL[i]
    #     while c == ';' or c == ' ' or c == '\r' or c == '\n':
    #         c = HPGL[i]
    #         i += i + 1
    #     cmd = c + HPGL[i + 1]
    #     i+=1
    #     print(cmd)


scalar_screen()

import matplotlib.pyplot as plt

# x_coordinates = [150,150,210,210]
# y_coordinates = [150,1814,1814,150]
x_coordinates = [150, 154, 158, 162]
y_coordinates = [470, 444, 458, 483]
t = 0
for i in [0, 1]:
    x = []
    y = []
    for j in [0, 1]:
        x.append(x_coordinates[t])
        y.append(y_coordinates[t])
        t += 1
    plt.plot(x, y)

plt.xlabel('x - axis')
# Set the y axis label of the current axis.
plt.ylabel('y - axis')
# Set a title of the current axes.
plt.title('Two or more lines on same plot with suitable legends ')
# show a legend on the plot
# Display a figure.
plt.show()
