##this script solves the Qiuku problem
##================== I use 2GM as length unit =================================================================
import numpy as np
import matplotlib.pyplot as plt

r0 = 4.0  #initial position, multiply 2GM to get the actual initial r

def wofx(x):
    """for input x >= -1 find w>0 such that (w-1)e^w = x"""
    ##check error
    if x < -1.0:
        print("Error: Invalid input for wofx")
        return None
    ##where the slope is 0 use a Talor approximation    
    if x < -0.98: 
        w = np.sqrt((2.0+2.0*x)/(1.0+np.sqrt(2.0+2.0*x)*(2.0/3.0)))
        #iterate to improve accuracy
        lastw = w
        w = 1.0+x*np.exp(-w)        
        while(abs(w-lastw) > 1.e-8):
            lastw = w            
            w = 1.0+x*np.exp(-w)
        return w
    ##otherwise use Newton Raphson method interation
    w = np.log((2.0+x)/np.log(3.0+x)) #a more or less random guess
    lastw = w
    w = (x*np.exp(-w)-w+1.0)/w+w    
    while(abs(w-lastw)>1.e-9):
        lastw = w
        w = (x*np.exp(-w)-w+1.0)/w+w    
    return w


def compute_dervs(tau, mu, eps):
    """INPUT:
        tau : \tau/(2GM) 
        mu: \mu/(2GM)
        eps: \varepsilon, conserved energy per unit mass
       OUTPUT: 
        [d\tau/ds, d\mu/ds] if inputs are valid
        None if inputs are unphysical
    """
    diff = (mu-tau)*(mu+tau)
    if (diff <= -1.0):
        print("Error 01: unphysical input")
        return None
    w = wofx(diff)    
    if (eps**2 + 1.0/w < 1.0):
        print("Error 02: unphysical input")
        return None    
    wew = w * np.exp(w)
    if(abs(tau) < 1.e-4):
        if(abs(mu) > 1.e-3):
            dtauds = eps/2.0*wew/mu
            dmuds = -np.sqrt(dtauds**2 - wew/4.0) ##this is assuming infalling particle
            dtauds += tau*dmuds/mu
            return [ dtauds, dmuds ]
        else:
            print("Error 03: approaching ORIGIN")
            return None
    a = wew/4.0
    b = 2.0*eps*a*mu
    c = a*(tau**2+4*eps**2*a)
    if (abs(diff*c) > 1.e-4*b**2):
        if(tau >= 0):
            dtauds = (b - np.sqrt(max(b**2-diff*c, 0.0)))/diff
        else:
            dtauds = (b + np.sqrt(max(b**2-diff*c, 0.0)))/diff            
    else:
        dtauds = c/(b*2.0)*(1.0+diff*c/b**2/4.0)
    dmuds  =  (mu * dtauds - 2.0*a*eps)/tau
    return [dtauds, dmuds]



def runge_kutta_dervs(tau, mu, eps, ds):
    """INPUT:
       tau: \tau / (2GM)
       mu:  \mu / (2GM)
       eps: \varepsilon, conserved energy per unit mass
       ds: step size \Delta s
       OUTPUT:
       [ \Delta \tau/\Delta s, \Delta \mu/\Delta s ] for finite step size 
    """
    vel1 = compute_dervs(tau, mu, eps)
    vel2 = compute_dervs(tau + vel1[0]*ds/2.0, mu + vel1[1]*ds/2.0, eps)
    vel3 = compute_dervs(tau + vel2[0]*ds/2.0, mu + vel2[1]*ds/2.0, eps)
    vel4 = compute_dervs(tau + vel3[0]*ds, mu + vel3[1]*ds, eps)
    return [ (vel1[0] + vel4[0])/6.0 + (vel2[0]+vel3[0])/3.0, (vel1[1] + vel4[1])/6.0 + (vel2[1]+vel3[1])/3.0 ]

def s_exact(r):
    """ exact solution derived in Schwarzschild coordinates
       INPUT:  
           r: r/(2GM)
       OUTPUT:
           s: s/(2GM)
    """
    theta = np.pi*2.0-np.arccos(1-2*r/r0)
    return r0/2.0*np.sqrt(r0)*(theta-np.pi-np.sin(theta))


def Sch_t(tau, mu):
    """INPUT:
        tau: \tau / (2GM)
        mu:  \mu / (2GM)
    OUTPUT:
        t/(2GM) where t is Schwarzschild 
    """
    r = wofx(mu**2-tau**2)
    if(r == 1.0 ):
        return np.Infinity
    if(r > 1.0):
        rat = tau/mu
    else:
        rat = mu/tau
    return np.arctanh(rat)*2.0

eps = np.sqrt(1.0-1.0/r0)  #conserved energy



r = r0*0.997  ##initial position, you cannot really start with r0 because numerically you will be stuck at r0
s = s_exact(r)   ##use analytic solution to set the initial condition

t_ini  = 1.0/eps * s ## initial Schwarzschild time
mu = np.sqrt((r-1.0)*np.exp(r)/(1.0-np.tanh(t_ini/2.0)**2)) #initial mu
tau =  mu * np.tanh(t_ini/2.0) #initial tau

ds = 2.e-4  #step size

while( (mu-tau)*(mu+tau) > -0.9999 ):
    vel = runge_kutta_dervs(tau, mu, eps, ds)
    if(vel is None):
        break;
    tau = tau + vel[0]*ds
    mu = mu + vel[1]*ds
    s += ds

print("now mu + tau = "+str(mu+tau)+", r = "+str(wofx(mu**2-tau**2)))
print("let us refine the result:")

ds = 1.e-6 ##when approaching the singularity needs smaller time step size    

while( (mu-tau)*(mu+tau) > -0.999999 ):
    vel = runge_kutta_dervs(tau, mu, eps, ds)
    if(vel is None):
        break;
    tau = tau + vel[0]*ds
    mu = mu + vel[1]*ds
    s += ds

print("now mu + tau = "+str(mu+tau)+", r = "+str(wofx(mu**2-tau**2)))
    
mt_add = tau + mu     ##this is conserved for photon trajectory

#now find (tau, mu) such that tau+mu = mt_add (the photon world line) and mu**2-tau**2 = (r0-1)*exp(r0) (the space station world line)
mt_minus = (r0-1.0)*np.exp(r0)/mt_add ## mu - tau
mu = (mt_add + mt_minus)/2.0
tau = (mt_add - mt_minus)/2.0
#convert to the Schwarzschild t coordinate
t = Sch_t(tau, mu)
#convert to the proper time observed on the space station
t_prop = t*np.sqrt(1-1.0/r)
print("The space station must send the Qiuku signal no later than t_{space station} = "+str(t_prop*2) + "GM.")
