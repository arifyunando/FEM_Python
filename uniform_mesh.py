import numpy as np

def uniform_mesh(d1, d2, p, m , element_type : str):
    PD  = 2  # Problem Dimension
    q   = np.array([[0, 0], [d1, 0], [0, d2], [d1, d2]]) # 4 corners
    NoN = (p + 1) * (m + 1)
    NoE = p*m
    NPE = 4

    ### Nodes ###
    NL  = np.zeros([NoN, PD])
    a   = (q[1, 0] - q[0, 0])/p # Increment in the horizontal dir.
    b   = (q[2, 1] - q[0, 1])/m # Increment in the Vertical dir.

    n   = 0 # This will allow us to go through rows in NL
    for i in range(1, m+2):         # Vertical loop
        for j in range(1, p+2):     # Horizontal loop
            NL[n, 0]    = q[0, 0] + (j - 1)*a   # x values
            NL[n, 1]    = q[0, 1] + (i - 1)*b   # y values
            n += 1
    
    ### Elements ###
    EL = np.zeros([NoE, NPE])
    for i in range(1, m+1):         # Vertical loop
        for j in range(1, p+1):     # Horizontal loop
            if j == 1:
                EL[(i-1)*p + j - 1, 0] = (i - 1)*(p + 1) + j
                EL[(i-1)*p + j - 1, 1] = EL[(i-1)*p + j - 1, 0] + 1
                EL[(i-1)*p + j - 1, 3] = EL[(i-1)*p + j - 1, 0] + (p + 1)
                EL[(i-1)*p + j - 1, 2] = EL[(i-1)*p + j - 1, 3] + 1
            else:
                EL[(i-1)*p + j - 1, 0] = EL[(i-1)*p + j - 2, 1]
                EL[(i-1)*p + j - 1, 3] = EL[(i-1)*p + j - 2, 2] 
                EL[(i-1)*p + j - 1, 1] = EL[(i-1)*p + j - 1, 0] + 1
                EL[(i-1)*p + j - 1, 2] = EL[(i-1)*p + j - 1, 3] + 1

    if element_type == 'D2TR3N':
        NPE_new = 3
        NoE_new = 2*NoE
        EL_new  = np.zeros([NoE_new, NPE_new])

        for i in range(1, NoE+1):
            #for the first triangular element
            EL_new[2*(i-1), 0] = EL[i-1, 0]
            EL_new[2*(i-1), 1] = EL[i-1, 1]
            EL_new[2*(i-1), 2] = EL[i-1, 2]

            #for the second triangular element
            EL_new[2*(i-1) + 1, 0] = EL[i-1, 0]
            EL_new[2*(i-1) + 1, 1] = EL[i-1, 2]
            EL_new[2*(i-1) + 1, 2] = EL[i-1, 3]

        EL = EL_new

    EL = EL.astype(int)
    return (NL, EL)









