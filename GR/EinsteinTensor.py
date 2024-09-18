#sample script: calculate Einstein tensor

import sympy as sym
sym.init_printing()

#dimension of the spacetime
dim = 4

##allocate space to save connections, Riemann tensor, and Ricci tensor
#\Gamma_{ijk}
gam_down = sym.MutableDenseNDimArray(range(dim**3), shape=(dim, dim, dim))
#\Gamma^i_{ jk}
gam_up = sym.MutableDenseNDimArray(range(dim**3), shape=(dim, dim, dim))
#R_{ij}
ricci_down = sym.MutableDenseNDimArray(range(dim**2), shape=(dim, dim))
#R^i_{ j}
ricci_mixed = sym.MutableDenseNDimArray(range(dim**2), shape=(dim, dim))
#R_{ij}
ricci_up = sym.MutableDenseNDimArray(range(dim**2), shape=(dim, dim))
#G_{ij}
einstein_down = sym.MutableDenseNDimArray(range(dim**2), shape=(dim, dim))
#G^i_{ j}
einstein_mixed = sym.MutableDenseNDimArray(range(dim**2), shape=(dim, dim))
#G^{ij}
einstein_up = sym.MutableDenseNDimArray(range(dim**2), shape=(dim, dim))


#define u[0],u[1],... in a single line
u = sym.symarray('u',dim)

#--------------define covariant metric -----------------
a = sym.symbols('a', cls=sym.Function)
##FRW flat 
gdown = sym.diag( 1, -a(u[0])**2, -a(u[0])**2, -a(u[0])**2)
##FRW non-flat metric, k is the spatial curvature parameter
#k = sym.symbols('k')
#gdown = sym.diag( 1, -a(u[0])**2/(1-k*u[1]**2), -a(u[0])**2*u[1]**2, -a(u[0])**2 * u[1]**2 * sym.sin(u[2])**2 )

#contravariant metric
gup = gdown ** -1

#determinant of the covariant metric
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

for i in range(dim):
    for j in range(dim):
        ricci_mixed[i, j] = 0
        for k in range(dim):
            ricci_mixed[i, j] += gup[i, k] * ricci_down[k, j]
        ricci_mixed[i, j] = sym.simplify(ricci_mixed[i, j])

for i in range(dim):
    for j in range(i+1):
        ricci_up[i, j] = 0
        for k in range(dim):
            ricci_up[i, j] += ricci_mixed[i, k] * gup[k, j]
        ricci_up[i, j] = sym.simplify(ricci_up[i, j])
        if(i != j):
            ricci_up[j, i] = ricci_up[i, j]
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
        einstein_up[i,j] = sym.simplify(ricci_up[i, j] - ricci_scalar/2 * gup[i, j])
    if(i != j):
        einstein_down[j, i] = einstein_down[i, j]
        einstein_up[j, i] = einstein_up[i, j]        
    
for i in range(dim):
    for j in range(dim):
        if( i == j ):
            einstein_mixed[i,j] = sym.simplify(ricci_mixed[i, j] - ricci_scalar/2)
        else:
            einstein_mixed[i,j] = ricci_mixed[i, j]


print("---------------G_{ij}--------------")            
for i in range(dim):
    for j in range(i+1):
        if(einstein_down[i, j] != 0):
            print(i, j, einstein_down[i, j])


print("---------------G^{ij}--------------")                        
for i in range(dim):
    for j in range(i+1):
        if(einstein_up[i, j] != 0):
            print(i, j, einstein_up[i, j])            

            
print("---------------G^i_{ j}--------------")                        
for i in range(dim):
    for j in range(i+1):
        if(einstein_mixed[i, j] != 0):
            print(i, j, einstein_mixed[i, j])            

            
