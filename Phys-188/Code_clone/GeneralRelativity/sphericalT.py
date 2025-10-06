#sample code: calculate energy-momentum tensor conservation equation
#this code has been optmized 
import sympy as sym
sym.init_printing()

#dimension of the spacetime
dim = 4

#define u[0], u[1], ... in a single line
u = sym.symarray('u',dim)

#for more readable outut
t, r, theta, phi = sym.symbols(r't, r, theta, phi')

#define the Newtonian potential, spatial curvature, energy density and pressure
Phi, Psi, rho, p = sym.symbols('Phi, Psi, rho, p', cls =sym.Function)

#covariant metric
gdown = sym.diag( sym.exp(2*Phi(u[1])), -sym.exp(-2*Psi(u[1])) , -u[1]**2, -u[1]**2 * sym.sin(u[2]) **2 )

#contravariant metric
gup = gdown ** -1

#determinant of the covariant metric
detg = gdown.det()

#\Gamma_{ijk}
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

#\Gamma^i_{\ jk}
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


#covariant derivative V^i_{\ j;k}
def tensor_ud_derivative(v, i, j, k):
    dv = sym.diff(v[i, j], u[k])
    for l in range(dim):
        dv += (gam_up[i, l, k] * v[l, j]-gam_up[l, j, k] * v[i, l])
    return sym.simplify(dv)

#T^\mu_{\ \nu}
Tud = sym.diag(rho(u[1]), -p(u[1]), -p(u[1]), -p(u[1]))

#T^i_{\ j;i}
for j in range(dim):
    flow = 0    
    for i in range(dim):
        flow += tensor_ud_derivative(Tud, i, j, i)
    print(j, sym.simplify(flow).subs(u[1], r))
