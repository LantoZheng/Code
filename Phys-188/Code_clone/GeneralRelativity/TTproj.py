#this script calculate Q_{ij}*Q_{kl}P^{ijkl}
# where the TT projection operator in (theta, phi) direction (spherical coordinate)

import sympy as sym

dim = 3

theta, phi = sym.symbols('theta, phi')

Q = sym.Matrix( [
    [1, -sym.I, 0],
    [-sym.I, -1, 0],
    [0, 0, 0]
    ])

n = [ sym.sin(theta) * sym.cos(phi), sym.sin(theta) * sym.sin(phi), sym.cos(theta) ]


def proj(i, j):
    if(i==j):
        return n[i]*n[j]-1
    else:
        return n[i]*n[j]


def TTproj(i,j,k,l):
    return proj(i, k)*proj(j, l)-proj(i,j)*proj(k, l)/2


s = 0
for i in range(dim):
    for j in range(dim):
        for k in range(dim):
            for l in range(dim):
                s += TTproj(i, j, k, l)*sym.conjugate(Q[i,j])*Q[k, l]

s = sym.simplify(s)

print("Gravitational Radiation in theta, phi direction:")                
print(s)

print("Total radiation")
print(sym.integrate(sym.integrate(s*sym.sin(theta), (theta, 0, sym.pi)), (phi, 0, 2*sym.pi)))

