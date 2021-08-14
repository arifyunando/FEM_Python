import numpy as np
from functions import *

x = np.array([
    [0, 0],
    [1, 0],
    [1, 2],
    [0, 2]
])

xtr = np.array([
    [0, 0],
    [2, 0],
    [1, 1]
])

GPE = 1 #Gaussian Points per Elements
K   = stiffness(x, GPE)
print(K) 