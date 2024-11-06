#sample script: calculate covariant derivatives

import sympy as sym
sym.init_printing()

#dimension of the space
dim = 2

#define u[0],u[1],... in a single line
u = sym.symarray('u',dim)


#----covariant metric
#r = sym.symbols('r')
gdown = sym.diag( 1, sym.sin(u[0])**2 )
#gdown = sym.diag( r**2, r**2*sym.sin(u[0])**2 )
#gdown = sym.diag(1, sym.exp(2*u[0]))
#gdown = sym.diag(1/(1+u[0]**2+u[1]**2),1/(1+u[0]**2+u[1]**2))
#gdown = sym.diag(1/(1+u[0]**2+u[1]**2)**2,1/(1+u[0]**2+u[1]**2)**2)
#gdown = sym.Matrix([[1/(u[0]**2+u[1]**2+1), 1/(u[0]**2+u[1]**2+1)/2],[1/(u[0]**2+u[1]**2+1)/2, 1/(u[0]**2+u[1]**2+1)]])

#contravariant metric
gup = gdown ** -1

#determinant of the covariant metric
detg = gdown.det()

def connection_down(i, j, k):
    return (sym.diff(gdown[i, j], u[k]) + sym.diff(gdown[i, k], u[j]) - sym.diff(gdown[j, k], u[i]))/2

##allocate space to save connections
gam_down = sym.MutableDenseNDimArray(range(dim**3), shape=(dim, dim, dim))
gam_up = sym.MutableDenseNDimArray(range(dim**3), shape=(dim, dim, dim))

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
                
def vector_down_derivative(v, i, j):
    dv = sym.diff(v[i], u[j])
    for k in range(dim):
        dv -= gam_up[k, i, j] * v[k]
    return sym.simplify(dv)


def vector_up_derivative(v, i, j):
    dv = sym.diff(v[i], u[j])
    for k in range(dim):
        dv += gam_up[i, k, j] * v[k]
    return sym.simplify(dv)
        

def tensor_down_derivative(v, i, j, k):
    dv = sym.diff(v[i, j], u[k])
    for l in range(dim):
        dv -= (gam_up[l, i, k] * v[l, j] + gam_up[l, j, k] * v[i, l])
    return sym.simplify(dv)

def tensor_up_derivative(v, i, j, k):
    dv = sym.diff(v[i, j], u[k])
    for l in range(dim):
        dv += (gam_up[i, l, k] * v[l, j] + gam_up[j, l, k] * v[i, l])
    return sym.simplify(dv)


def tensor_ud_derivative(v, i, j, k):
    dv = sym.diff(v[i, j], u[k])
    for l in range(dim):
        dv += (gam_up[i, l, k] * v[l, j]-gam_up[l, j, k] * v[i, l])
    return sym.simplify(dv)
        

def tensor_du_derivative(v, i, j, k):
    dv = sym.diff(v[i, j], u[k])
    for l in range(dim):
        dv += (gam_up[j, l, k] * v[i, l] - gam_up[l, i, k] * v[l, j])
    return sym.simplify(dv)


##================test metric derivatives (must = 0) ==============
#print('-----metric derivatives------')
#for i in range(dim):
#    for j in range(i+1):
#        for k in range(dim):
#            vd = tensor_up_derivative(gup, i, j, k)
#            if(not vd == 0):
#                print(i, j, k, vd)
##==================================================================

print("--------------vec down-------------------")
#covariant vector
vec = sym.Array( [ sym.sin(u[0]), sym.sin(u[1]) ])  
for i in range(dim):
    print(vec[i])
print('-----vector derivatives------')
div = 0 #to save divergence
for i in range(dim):
    for j in range(dim):
        vd = vector_down_derivative(vec, i, j)
        if(vd != 0):
            print(i, j, vd)
            div += vd * gup[i, j]
print("divergence = "+str(div))
#print("divergence at (0, 0):"+str(div.subs(u[0],0).subs(u[1],0).evalf()))

print("--------------vec up-------------------")
#contravariant vector
#vecup = sym.simplify(gup*sym.Matrix(vec)) 
vecup = sym.Array( [ sym.sin(u[0]), sym.sin(u[1])])
for i in range(dim):
    print(vecup[i])

div = 0 #to save divergence
for i in range(dim):
    for j in range(dim):
        vd = vector_up_derivative(vecup, i, j)
        if(vd != 0):
            print(i, j, vd)
            if(i==j):
                div += vd
print("divergence = "+str(div))
#print("divergence at (0, 0):"+str(div.subs(u[0],0).subs(u[1],0).evalf()))

