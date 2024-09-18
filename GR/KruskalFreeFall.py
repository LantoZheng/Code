##this script uses Kruskal coordinates to calculate free fall into Schwarzschild BH along the radial direction
##================== I use 2GM as length unit =================================================================
import numpy as np
import matplotlib.pyplot as plt

r0 = 4  #initial position, multiply 2GM to get the actual initial r

##W(x)
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



eps = np.sqrt(1.0-1.0/r0)  #conserved energy



r = r0*0.995  ##initial position, you cannot really start with r0 because numerically you will be stuck at r0
s = s_exact(r)   ##use analytic solution to set the initial condition

slist = [ 0., s] # the list to save s, 
rlist = [ r0, r] # the list to save (derived) r (except that the two presaved values are analytic solutions)


tau = 0. #initial tau, in principle can set to be anything
mu = np.sqrt(tau**2 + (r-1.0)*np.exp(r)) #initial mu

ds = 1.e-4  #step size
lastr = r0



while(r > 0.003):
    vel = runge_kutta_dervs(tau, mu, eps, ds)
    if(vel is None):
        break;
    tau = tau + vel[0]*ds
    mu = mu + vel[1]*ds
    s += ds
    r = wofx(mu**2-tau**2)
    if(r < lastr*0.99  ):  #save for plotting if r has varied quite a bit
        lastr = r
        slist.append(s)
        rlist.append(r)
        print("s="+str(s)+", r=" + str(r) + ", tau=" + str(tau)+", mu="+str(mu))
        
plt.plot( slist, rlist, 'r', linewidth=2.0, label="Kruskal numeric")
slist = [ s_exact(r) for r in rlist ]
plt.plot( slist, rlist, 'b:', linewidth=2.0,label="exact solution")
plt.xlabel(r'$\frac{s}{2GM}$')
plt.ylabel(r'$\frac{r}{2GM}$')
plt.legend()
plt.show()
