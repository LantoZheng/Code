#luminosity distance and angular diameter distances for LCDM model

#use 1/H_0 as the length and time unit

import numpy as np

#density parameters
Omega_m = 0.3
Omega_k = 0.1
Omega_r = 0.0 #for z < 100 ignore the radiation

Omega_L = 1.0 - Omega_m - Omega_k - Omega_r

#Hubble parameter H = dot a / a as a function of z
def Hofz(z):
    return np.sqrt(Omega_L + Omega_m*(1+z)**3 + Omega_k * (1+z)**2 + Omega_r*(1+z)**4)

def dchibydz(z):
    return 1.0/Hofz(z)

def rofchi(chi):
    if(abs(Omega_k)<1.e-20):
        return chi
    if(Omega_k < 0):
        return np.sin(np.sqrt(-Omega_k)*chi)/np.sqrt(-Omega_k)
    return np.sinh(np.sqrt(Omega_k)*chi)/np.sqrt(Omega_k)


z = 1.0

nsteps = 5000
step = z/nsteps
zlist = np.arange(0.0, z+step/2.0, step)
chi = (sum( [ dchibydz(zzz) for zzz in zlist ] )-(dchibydz(0.0)+dchibydz(z))/2.0)*step
r = rofchi(chi)
print("At z = " + str(z))
print("luminosity distance * H_0 ="+str(r*(1+z)))
print("angular diameter distance * H_0 = "+str(r/(1+z)))
    
#now if you want to convert to Mpc
H0 = 70  #km/s/Mpc
speed_of_light = 2.998e5 ##speed of light in km/s
H0Mpc = H0/speed_of_light # H0*Mpc/c 
print("if H_0 = "+str(H0)+" km/s/Mpc")
print("luminosity distance  = "+str(r*(1+z)/H0Mpc)+" Mpc")
print("angular diameter distance  = "+str(r/(1+z)/H0Mpc)+" Mpc")



    


