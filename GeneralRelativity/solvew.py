import numpy as np
import matplotlib.pyplot as plt

def xofw(w):
    return (w-1.0)*np.exp(w)

def wofx(x):
    """for input x >= -1 find w>0 such that (w-1)e^w = x"""
    ##check error
    if x < -1:
        print("Error: Invalid input for wofx")
        return None
    ##where the slope is 0 use a Talor approximation    
    if x < -0.995: 
        return np.sqrt(2.0+2.0*x-2.0/3.0*(2.0*x+2.0)**1.5)
    ##otherwise use Newton Raphson method interation    
    w = np.log((2.0+x)/np.log(3.0+x)) #a more or less random guess
    lastw = w
    w = (x*np.exp(-w)-w+1.0)/w+w    
    while(abs(w-lastw)>1.e-8):
        lastw = w
        w = (x*np.exp(-w)-w+1.0)/w+w    
    return w

x = np.arange(-1., 3., 0.025)
w = [ wofx(t) for t in x ]
plt.plot(x, w, color='r', linewidth=2.0)
plt.xlabel('$x$')
plt.ylabel('$W(x)$')
plt.show()


    
