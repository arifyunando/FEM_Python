import numpy as np

def GaussPoint(NPE, GPE, gauss_point):
    xi, eta, alpha = 0, 0, 0
    if NPE == 3:
        if GPE == 1:
            if gauss_point == 1:
                xi      = 1/3
                eta     = 1/3
                alpha   = 1
    if NPE == 4:
        if GPE == 1:
            if gauss_point == 1:
                xi      = 0
                eta     = 0
                alpha   = 4
        if GPE == 4:
            if gauss_point == 1:
                xi      = -1/np.sqrt(3)
                eta     = -1/np.sqrt(3)
                alpha   =  1
            if gauss_point == 2:
                xi      =  1/np.sqrt(3)
                eta     = -1/np.sqrt(3)
                alpha   =  1
            if gauss_point == 3:
                xi      =  1/np.sqrt(3)
                eta     =  1/np.sqrt(3)
                alpha   =  1
            if gauss_point == 4:
                xi      = -1/np.sqrt(3)
                eta     =  1/np.sqrt(3)
                alpha   =  1
    return xi, eta, alpha


def gradientN_natural(NPE, xi, eta):
    
    PD      = 2
    result  = np.zeros([PD, NPE])
    if NPE == 3:
        result[0,0] =  1
        result[0,1] =  0
        result[0,2] = -1
        
        result[1,0] =  0 
        result[1,1] =  1
        result[1,2] = -1

    if NPE == 4:
        result[0,0] = -1/4 * (1 - eta)
        result[0,1] =  1/4 * (1 - eta)
        result[0,2] =  1/4 * (1 + eta)
        result[0,3] = -1/4 * (1 + eta)
        
        result[1,0] = -1/4 * (1 - xi)
        result[1,1] = -1/4 * (1 + xi)
        result[1,2] =  1/4 * (1 + xi)
        result[1,3] =  1/4 * (1 - xi)

    return result


def constitutiveMatrix(i, j, k, l):
    youngsMod   = 8/3
    poisson     = 1/3
    C = (youngsMod/(2*(1+poisson))) * (kronecker_delta(i,l)*kronecker_delta(j,k) + kronecker_delta(i,k)*kronecker_delta(j,l))
    C += youngsMod*poisson/(1 - poisson**2) * kronecker_delta(i,j)*kronecker_delta(k,l)
    return C


def kronecker_delta(i, j):
    if i == j:
        return 1
    else:
        return 0


def element_stiffness(nl, NL):
    # Nodes and Problem Dimension Definitions
    NPE = np.size(nl, 0)
    PD  = np.size(NL, 1)

    x   = np.zeros([NPE, PD])
    x[0:NPE, 0:PD] = NL[nl[0:NPE] - 1, 0:PD]

    # Stiffness Matrix Initialization
    K   = np.zeros([NPE*PD, NPE*PD])

    # Transposing Coordinates
    coor = x.T

    # Define Gauss Point Numbers
    if NPE == 3:
        GPE = 1
    elif NPE == 4:
        GPE = 4
    
    # Looping
    for i in range(1, NPE + 1):
        for j in range(1, NPE + 1):
            k = np.zeros([PD, PD])
            for gauss_points in range(1, GPE + 1):
                Jacobian = np.zeros([PD, PD])
                grad     = np.zeros([PD, NPE])
                xi, eta, alpha = GaussPoint(NPE, GPE, gauss_points)
                grad_natural   = gradientN_natural(NPE, xi, eta)
                Jacobian = coor @ grad_natural.T 
                grad     = np.linalg.inv(Jacobian).T @ grad_natural
                for a in range(1, PD + 1):
                    for c in range(1, PD + 1):
                        for b in range(1, PD + 1):
                            for d in range(1, PD + 1):
                                if NPE == 3:
                                    k[a - 1, c - 1] = k[a - 1, c - 1] + grad[b - 1, i - 1] * constitutiveMatrix(a, b, c, d) * grad[d - 1, j - 1] * np.linalg.det(Jacobian) * alpha * 0.5
                                else:
                                    k[a - 1, c - 1] = k[a - 1, c - 1] + grad[b - 1, i - 1] * constitutiveMatrix(a, b, c, d) * grad[d - 1, j - 1] * np.linalg.det(Jacobian) * alpha
            K[((i-1)*PD+1) - 1 : i*PD, ((j-1)*PD + 1) - 1 : j*PD] = k
    
    return K


def stiffness(x, GPE):

    # Nodes and Problem Dimension Definitions
    NPE = np.size(x, 0)
    PD  = np.size(x, 1)

    # Stiffness Matrix Initialization
    K   = np.zeros([NPE*PD, NPE*PD])

    # Transposing Coordinates
    coor = x.T

    # Looping
    for i in range(1, NPE + 1):
        for j in range(1, NPE + 1):
            k = np.zeros([PD, PD])
            for gauss_points in range(1, GPE + 1):
                Jacobian = np.zeros([PD, PD])
                grad     = np.zeros([PD, NPE])
                xi, eta, alpha = GaussPoint(NPE, GPE, gauss_points)
                grad_natural   = gradientN_natural(NPE, xi, eta)
                Jacobian = coor @ grad_natural.T 
                grad     = np.linalg.inv(Jacobian).T @ grad_natural
                for a in range(1, PD + 1):
                    for c in range(1, PD + 1):
                        for b in range(1, PD + 1):
                            for d in range(1, PD + 1):
                                k[a - 1, c - 1] = k[a - 1, c - 1] + grad[b - 1, i - 1] * constitutiveMatrix(a, b, c, d) * grad[d - 1, j - 1] * np.linalg.det(Jacobian) * alpha
            K[((i-1)*PD+1) - 1 : i*PD, ((j-1)*PD + 1) - 1 : j*PD] = k
    
    return K

def assign_BCs(NL, BC_flag, defV):
    NoN = np.size(NL, 0)
    PD  = np.size(NL, 1)

    ENL = np.zeros([NoN, 6*PD])
    ENL[:, 0:PD] = NL

    if BC_flag == 'extension':
        for i in range(NoN):
            if ENL[i, 0] == 0:
                ENL[i, 2] = -1
                ENL[i, 3] = -1
                ENL[i, 8] = -defV
                ENL[i, 9] = 0

            elif ENL[i, 0] == 1:
                ENL[i, 2] = -1
                ENL[i, 3] = -1
                ENL[i, 8] = defV
                ENL[i, 9] = 0

            else:
                ENL[i, 2 ] = 1
                ENL[i, 3 ] = 1
                ENL[i, 10] = 0
                ENL[i, 11] = 0
    
    if BC_flag == "expansion":
        for i in range(NoN):
            if ENL[i, 0] in [0, 1] or ENL[i, 1] in [0 , 1]:
                ENL[i, 2] = -1
                ENL[i, 3] = -1
                ENL[i, 8] = defV * ENL[i, 0]
                ENL[i, 9] = defV * ENL[i, 1]
            
            else:
                ENL[i, 2]  = 1
                ENL[i, 3]  = 1
                ENL[i, 10] = 0
                ENL[i, 11] = 0

    if BC_flag == 'shear':
        for i in range(NoN):
            if ENL[i, 1] == 0:
                ENL[i, 2] = -1
                ENL[i, 3] = -1
                ENL[i, 8] = 0
                ENL[i, 9] = 0
            
            elif ENL[i, 1] == 1:
                ENL[i, 2] = -1
                ENL[i, 3] = -1
                ENL[i, 8] = defV
                ENL[i, 9] = 0
            
            else:
                ENL[i, 2]  = 1
                ENL[i, 3]  = 1
                ENL[i, 10] = 0
                ENL[i, 11] = 0
    
    DOFs = 0
    DOCs = 0

    for i in range(NoN):
        for j in range(PD):
            if ENL[i, PD + j] == -1:
                DOCs -= 1
                ENL[i, 2*PD + j] = DOCs
            else:
                DOFs += 1
                ENL[i, 2*PD + j] = DOFs

    for i in range(NoN):
        for j in range(PD):
            if ENL[i, 2*PD + j] < 0:
                ENL[i , 3*PD + j] = abs(ENL[i, 2*PD + j]) + DOFs
            else:
                ENL[i , 3*PD + j] = abs(ENL[i, 2*PD + j])
    
    DOCs = abs(DOCs)

    return ENL, DOFs, DOCs
                
def assemble_stiffness(ENL, EL, NL):
    NoE = np.size(EL, 0)
    NPE = np.size(EL, 1)
    NoN = np.size(NL, 0)
    PD  = np.size(NL, 1)

    K   = np.zeros([NoN*PD, NoN*PD])

    for i in range(1, NoE + 1):
        nl  = EL[i - 1, 0 : NPE]
        k   = element_stiffness(nl, NL)
        for r in range(NPE):
            for p in range(PD):
                for q in range(NPE):
                    for s in range(PD):
                        row = ENL[nl[r] - 1, p + 3*PD]
                        col = ENL[nl[q] - 1, s + 3*PD]
                        val = k[r*PD + p, q*PD + s]
                        K[int(row) - 1, int(col) - 1] = K[int(row) - 1, int(col) - 1] + val
    
    return K


def assemble_displacements(ENL, NL):
    NoN = np.size(NL, 0)
    PD  = np.size(NL, 1)
    DOC = 0
    Up  = []
    for i in range(NoN):
        for j in range(PD):
            if ENL[i, PD + j] == -1:
                DOC += 1
                Up.append(ENL[i, 4*PD + j])
    Up = np.vstack([Up]).reshape(-1, 1)
    return Up


def assemble_forces(ENL, NL):
    NoN = np.size(NL, 0)
    PD  = np.size(NL, 1)
    DOF = 0
    Fp  = []
    for i in range(NoN):
        for j in range(PD):
            if ENL[i, PD + j] == 1:
                DOF += 1
                Fp.append(ENL[i, 5*PD + j])
    Fp = np.vstack([Fp]).reshape(-1, 1)
    return Fp


def update_nodes(ENL, Uu, Fu, NL):
    NoN  = np.size(NL, 0)
    PD   = np.size(NL, 1)
    DOFs = 0
    DOCs = 0
    for i in range(NoN):
        for j in range(PD):
            if ENL[i, PD + j] == 1:
                DOFs += 1
                ENL[i, 4*PD + j] = Uu[DOFs - 1]
            else:
                DOCs += 1
                ENL[i, 5*PD + j] = Fu[DOCs - 1]
    return ENL


            



