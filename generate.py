# from uniform_mesh import *
from void_mesh import *
import matplotlib.pyplot as plt
import numpy as np


### Initialization ###
d1  = 1
d2  = 1
p   = 4
m   = 3
R   = 0.2
e   = 'D2TR3N'

# NL, EL = uniform_mesh(d1, d2, p, m, e)
NL, EL = void_mesh(d1, d2, p, m, R, e)

NoN = np.size(NL, 0)
NoE = np.size(EL, 0)

plt.figure(1)

count = 1
for i in range(0, NoN):
    plt.annotate(count, xy = (NL[i, 0], NL[i, 1]))
    count += 1

if e == 'D2QU4N':
    count2 = 1
    for j in range(0, NoE):
        plt.annotate(count2, xy=(
            (NL[EL[j, 0] - 1, 0] + NL[EL[j, 1] - 1, 0] + NL[EL[j, 2] - 1, 0] + NL[EL[j, 3] - 1, 0])/4,
            (NL[EL[j, 0] - 1, 1] + NL[EL[j, 1] - 1, 1] + NL[EL[j, 2] - 1, 1] + NL[EL[j, 3] - 1, 1])/4),
            c = 'blue')
        count2 += 1
    
    # Plot Lines
    x0, y0 = NL[EL[:, 0] - 1, 0], NL[EL[:, 0] - 1, 1]
    x1, y1 = NL[EL[:, 1] - 1, 0], NL[EL[:, 1] - 1, 1]
    x2, y2 = NL[EL[:, 2] - 1, 0], NL[EL[:, 2] - 1, 1]
    x3, y3 = NL[EL[:, 3] - 1, 0], NL[EL[:, 3] - 1, 1]
    plt.plot(np.array([x0, x1]), np.array([y0, y1]), 'r', linewidth = 3)
    plt.plot(np.array([x1, x2]), np.array([y1, y2]), 'r', linewidth = 3)
    plt.plot(np.array([x2, x3]), np.array([y2, y3]), 'r', linewidth = 3)
    plt.plot(np.array([x3, x0]), np.array([y3, y0]), 'r', linewidth = 3)

if e == 'D2TR3N':
    count2 = 1
    for j in range(0, NoE):
        plt.annotate(count2, xy =(
            (NL[EL[j, 0] - 1, 0] + NL[EL[j, 1] - 1, 0] + NL[EL[j, 2] - 1, 0])/3,
            (NL[EL[j, 0] - 1, 1] + NL[EL[j, 1] - 1, 1] + NL[EL[j, 2] - 1, 1])/3
        ), c = 'blue'
        )
        count2 += 1

        # Plot Lines
    x0, y0 = NL[EL[:, 0] - 1, 0], NL[EL[:, 0] - 1, 1]
    x1, y1 = NL[EL[:, 1] - 1, 0], NL[EL[:, 1] - 1, 1]
    x2, y2 = NL[EL[:, 2] - 1, 0], NL[EL[:, 2] - 1, 1]
    plt.plot(np.array([x0, x1]), np.array([y0, y1]), 'r', linewidth = 3)
    plt.plot(np.array([x1, x2]), np.array([y1, y2]), 'r', linewidth = 3)
    plt.plot(np.array([x2, x0]), np.array([y2, y0]), 'r', linewidth = 3)

plt.axis('scaled')
plt.show()