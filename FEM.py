from os import kill
import numpy as np
from void_mesh import *
from functions import *

d1  = 1
d2  = 1
p   = 6
m   = 6
R   = 0.2
element_type = 'D2QU4N'
defValue = 0.1 #Deformation Value

NL, EL  = void_mesh(d1, d2, p, m, R, element_type)
BC_flag = 'extension'

ENL, DOFs, DOCs = assign_BCs(NL, BC_flag, defValue)

K = assemble_stiffness(ENL, EL, NL)

Fp = assemble_forces(ENL, NL)
Up = assemble_displacements(ENL, NL)

K_UU = K[0 : DOFs, 0 : DOFs]
K_UP = K[0 : DOFs, DOFs : DOCs + DOFs]
K_PU = K[DOFs : DOCs + DOFs, 0 : DOFs]
K_PP = K[DOFs : DOCs + DOFs, DOFs : DOCs + DOFs]

F = Fp - (K_UP @ Up)
Uu = np.linalg.solve(K_UU, F)
Fu = (K_PU @ Uu) + (K_PP @ Up)

ENL = update_nodes(ENL, Uu, Fu, NL)

print(K[1:6, 1:6])