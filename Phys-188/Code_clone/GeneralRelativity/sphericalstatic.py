#sample code: calculate Einstein tensor for spherical static metric

import sympy as sym

#optimize printing
sym.init_printing()

#dimension of the space-time
dim = 4

##allocate space to save connections, Riemann tensor, and Ricci tensor
gam_down = sym.MutableDenseNDimArray(range(dim**3), shape=(dim, dim, dim))
gam_up = sym.MutableDenseNDimArray(range(dim**3), shape=(dim, dim, dim))
ricci_down = sym.MutableDenseNDimArray(range(dim**2), shape=(dim, dim))
einstein_down = sym.MutableDenseNDimArray(range(dim**2), shape=(dim, dim))


#define u[0], u[1], ... in a single line
u = sym.symarray('u',dim)

#for more readable output
r, t, theta, phi = sym.symbols(r'r, t, theta, phi')

#define Newtonian Potential and Spatial curvature
Phi = sym.Function('Phi')
Psi = sym.Function('Psi')

#define covariant metric
gdown = sym.diag( sym.exp(2*Phi(u[1])), -sym.exp(-2*Psi(u[1])) , -u[1]**2, -u[1]**2 * sym.sin(u[2]) **2 )

#define contravariant metric
gup = gdown ** -1

#calculate the determinant of the covariant metric
detg = gdown.det()

def connection_down(i, j, k):
    return (sym.diff(gdown[i, j], u[k]) + sym.diff(gdown[i, k], u[j]) - sym.diff(gdown[j, k], u[i]))/2


#compute connection \Gamma_{ijk}
for i in range(dim):
    for j in range(dim):
        for k in range(j+1):
            gam_down[i,j,k] = connection_down(i, j, k) 
            if(j != k):
                gam_down[i,k,j] = gam_down[i,j,k]


def connection_up(i, j, k):
    gam = 0
    for l in range(dim):
        gam += gam_down[l,j, k] * gup[l, i]
    return sym.simplify(gam)

#compute connection \Gamma^i_{ jk}
for i in range(dim):
    for j in range(dim):
        for k in range(j+1):
            gam_up[i,j,k] = connection_up(i, j, k) 
            if(j != k):
                gam_up[i,k,j] = gam_up[i,j,k]

##now we have both gam_down and gam_up saved

##===================compute Ricci tensor ==============================
def Riemann_tensor_up(i, j, k, l): ## R^i_{  jkl}
    R = sym.diff(gam_up[i, j, k], u[l]) - sym.diff(gam_up[i, j, l], u[k])
    for m in range(dim):
        R += gam_up[i, m, l] * gam_up[m, j, k] - gam_up[i, m, k] * gam_up[m, j, l]
    return sym.simplify(R)

for i in range(dim):
    for j in range(i+1):
        ricci_down[i, j] = 0
        for k in range(dim):
            ricci_down[i, j] += Riemann_tensor_up(k, i, j, k)
        ricci_down[i,j] = sym.simplify(ricci_down[i,j])
        if(i != j):
            ricci_down[j, i] = ricci_down[i, j]
## ------------------ now Ricci tensor is saved-----------------------

##===========================compute Ricci scalar ====================
ricci_scalar = 0
for k in range(dim):
    for l in range(k+1):
        if(gup[k, l] != 0):
            if(k==l):
                ricci_scalar += ricci_down[k, l]*gup[k,l]
            else:
                ricci_scalar += 2 * ricci_down[k, l]*gup[k,l]    
ricci_scalar =  sym.simplify(ricci_scalar)
##-------------------now Ricci scalar is saved-----------------------

##=======================compute Einstein tensor ==================
for i in range(dim):
    for j in range(i+1):
        einstein_down[i,j] = sym.simplify(ricci_down[i, j] - ricci_scalar/2 * gdown[i, j])
    if(i != j):
        einstein_down[j, i] = einstein_down[i, j]
    

def Einstein_tensor_mixed(i, j): #G^i_j
    Gij = 0
    for k in range(dim):
        Gij += einstein_down[k, j] * gup[i, k]
    return sym.simplify(Gij)


###export latex expressions for G^i_j
print(r'\begin{eqnarray}')
for i in range(dim):
    for j in range(i+1):
        Gij = Einstein_tensor_mixed(i, j).subs(u[0], t).subs(u[1], r).subs(u[2], theta).subs(u[3], phi)
        if(Gij != 0):
            print(str(r'G^' + str(i)+ r'_' + str(j)+ r' &=& '+sym.latex(Gij) +r' \nonumber \\').replace(r'\Phi{\left (r \right )}', r'\Phi').replace(r'\Psi{\left (r \right )}', r'\Psi').replace(r'\frac{d}{d r} \Phi', r'\Phi_{,r}').replace(r'\frac{d}{d r} \Psi', r'\Psi_{, r}').replace(r'\frac{d^{2}}{d r^{2}}  \Phi', r'\Phi_{,r,r}') )
print(r'\end{eqnarray}')

            
