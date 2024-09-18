##sample code to solve the quartic potential oscillator problem:
##oscilator with potential V=1/4 kx^4, k=10^4 N/m^3
##natural length = 1m, oscillation amplitude = 0.5m
## mass = 1 kg
## find the maximum radiation frequency
##-----------------------------------------
import numpy as np
import matplotlib.pyplot as plt

mass = 1.0
k = 1.e4
length = 1.0
amp = 0.5
T = 7.4162987*np.sqrt(mass/(k*amp**2))

def compute_dervs(t, x):
    """t: time
        x[0]: position
        x[1]: velocity
        output: dx/dt"""
    return np.array( [ x[1] , -k*x[0]**3/mass ])

def runge_kutta_dervs(t, x, dt):
    vel1 = compute_dervs(t, x)
    vel2 = compute_dervs(t + dt/2, x + vel1 * (dt/2))
    vel3 = compute_dervs(t + dt/2, x + vel2 * (dt/2))
    vel4 = compute_dervs(t + dt, x + vel3 * dt)
    return (vel1 + vel4)/6.0 + (vel2 + vel3)/3.0
        
t = 0.
x = np.array([amp, 0.0])
n = 80000
dt = T/(n-1.0)
quad_list = [ (x[0]+length)**2 ] ##the quadruple (length + x)^2 
tlist = [ t ]

#solve x(t) and save the list of quadruple ((length+x)^2)
#I am always dropping the mass because I just want to compare different modes
for i in range(n):
    dxdt = runge_kutta_dervs(t, x, dt)
    x = x + dxdt * dt
    t = t + dt
    quad_list.append( (x[0]+length)**2 )  ##the quadruple
    tlist.append(t)


dim = 15
c = np.zeros(dim)

#decompose the quadruple into Fourier modes
for j in range(dim):  
    omega = np.pi * 2.0 /T * j
    c[j] = 0.0
    for i in range(n):
        c[j] += np.cos(omega*tlist[i])*quad_list[i]
    c[j] -= (np.cos(omega*tlist[0])*quad_list[0]+np.cos(omega*tlist[n-1])*quad_list[n-1])/2.0
    c[j] *= dt
    if(j==0):
        c[j] /= T ##for 0 mode the normalization factor is 1/T (1/ integral of 1)
    else:
        c[j] /= T/2.0 ##otherwhise the normalization factor is 2/T (1/integral of cos^2)
    print(j/T, c[j]**2*j**6) ##gravitational radiation power is proportional to quadruple**2 * frequency ** 6 
    
    
#check decomposition
plt.plot(tlist, quad_list, 'r', linewidth = 1.0)
plt.plot(tlist, [c[0] + c[1]*np.cos(np.pi*2/T * t)+c[2]*np.cos(np.pi*4/T*t)+c[3]*np.cos(np.pi*6/T*t)+c[4]*np.cos(np.pi*8/T*t) for t in tlist], 'b--', linewidth=1.0)
plt.xlabel(r'$t$')
plt.ylabel(r'$x$')
plt.show()

    




