#sample script to compute cosmic age for LambdaCDM model 
import numpy as np

#density parameters
Omega_k = 0.0
Omega_r = 0.0
Omega_m = 0.3
Omega_L = 1-Omega_k - Omega_r - Omega_m


##I use a_0=1 convention
Gyr = 1.e9*(365.2422*24*3600)  #Gyr in SI unit

H0Gyr = 70*(1.e3/3.086e22)*Gyr #H0 in unit of Gyr^{-1}


## H as a function of a, in unit of Gyr^{-1}
def Hofa(a):
    return H0Gyr*np.sqrt(Omega_r/a**4 + Omega_m/a**3 + Omega_k/a**2 + Omega_L)

## dt / da in unit of Gyr
def dtbyda(a):
    return 1.0/a/Hofa(a)


nsteps = 5000
astep = 1.0/nsteps
alist = np.arange(astep/2.0, 1.0, astep)
age = sum( [ dtbyda(a) for a in alist ] )*astep 
print("Age = " + str(age) + " Gyr")

