# -*- coding: utf-8 -*-
"""
Created on Mon Sep 26 12:52:48 2022

@author: hohle
"""

# =============================================================================
# #usage:
# #    n1 = 4
# #    k1 = np.random.binomial(n1, 0.2)
# #    [q1,b,Prior] = bayesian_bino(n1,k1)
# #    print(q1)
#     
# #    n2 = 5
# #    k2 = np.random.binomial(n2, 0.2)
# #    [q2,b,Prior] = bayesian_bino(n2,k2, Prior = Prior)
# #    print(q2)
#     
# #    n = 4
# #    q = 0.2
# #    k = np.random.binomial(n, q)
# #    [q,b,Prior] = bayesian_bino(n,k)
# #    for i in range(10):
# #        k = np.random.binomial(n, q)
# #        [q,b,Prior] = bayesian_bino(n,k, Prior = Prior)
# #        print(q)
# 
# =============================================================================
import numpy as np
import matplotlib.pyplot as plt

def bayesian_bino(n, k, CI = 0.68, **Prior):


    
    dq     = 1/(1000*n)
    q      = np.arange(0,1,dq)
    #qGuess = k/n
    
    if Prior:
        P        = Prior['Prior']
        [nr, nc] = P.shape
        if nr < nc:
            P = np.transpose(P)
        yint = np.interp(q, P[:,0], P[:,1])
    else:
        yint = 1
    
    #uniform prior
    Pu     = (q**k)*(1 - q)**(n - k) * yint
    C      = np.trapz(Pu,q)#for normalization: first y, then x 
    Pu     = Pu/C #normalizing pdf for conf int
    whereq = Pu.argmax()#getting index and value of most likely q and Pu
    maxPu  = Pu.max()
    maxq   = q[whereq]
    
    #determining errors (gauss approx of pdf)
    sig_q  = (maxq*(1-maxq)/n)**0.5
    
    ###########################################################################
    #determining errors from actual integral
    #right tail
    d1     = 0
    intv1  = 0
    d2     = 1
    intv2  = 0
    
    sumintv = intv1 + intv2
    
    while (sumintv < CI*0.999): #I leave a margin here in order to account for 
                                #numerical inacurracy
        if (whereq+d1<len(q)):
            
            d1     = d1 + 1
            indi   = np.arange(whereq, whereq+d1,1)
            intv1  = sum(Pu[indi])*dq
    #left tail
        if (whereq+d2>0):
            
            d2      = d2 - 1
            indi    = np.arange(whereq+d2,whereq,1)
            intv2   = sum(Pu[indi])*dq
            
        sumintv = intv1 + intv2

    idxU    = whereq + d1
    qUP     = q[idxU]
    idxL    = whereq+d2
    qLO     = q[idxL]
    diff_up = qUP - maxq
    diff_do = maxq - qLO
    
    
###############################################################################
#####the ploting part##########################################################

        
    xtofill     = q[np.arange(idxL,idxU,1)]
    ytofill     = Pu[np.arange(idxL,idxU,1)]
    ytofill[0]  = 0
    ytofill[-1] = 0
        
    plt.plot(q,Pu, color = 'black')
    plt.xlabel('estimated q')
    plt.ylabel('P(q|data)')
    plt.fill(xtofill, ytofill, facecolor = 'black', alpha = 0.02)
    plt.plot([qLO, qLO],[0,Pu[idxL]],'k-')
    plt.plot([qUP, qUP],[0,Pu[idxU]],'k-')
    plt.plot([maxq, maxq],[0,maxPu],'k--')
    plt.title('$q = %1.2f ^{+ %1.2f}_{-%1.2f}$' % (maxq, \
                  diff_up, diff_do))
    plt.show()
        

    return([qLO, maxq, qUP], sig_q, np.array([q,Pu]))

###############################################################################
import numpy as np
import matplotlib.pyplot as plt

import numpy as np
import matplotlib.pyplot as plt

def bayesian_poiss(data, CI = 0.68, plot=True, **Prior):
    """
    params: 
        data: list or 1D np.ndarray of data.
        CI: Confidence interval for lower to upper bound, defaults to 0.68
        plot: whether to plot the figure. Do not change
        Prior: Allows an input for a prior.
    
    returns: ([lambda lower bound (float), lambda max (float), lambda upper bound (float)], 
              np.array(lambda, P(lambda)) (N x 2 ndarray))
    lambda max here denotes the lambda at which P(lambda | data) is maximized.
    The plot should plot P(lambda | data) as well as shade the range between lambda lower bound and lambda upper bound
    """


    max_l_range = max(20, 4 * np.mean(data)) if mean_data > 0 else 20
    num_steps = 2000
    dl = max_l_range / num_steps
    l = np.arange(dl, max_l_range, dl)

    if Prior:
        P = Prior['Prior']
        if P.shape[0] < P.shape[1]:
            P = P.T
        yint = np.interp(l, P[:,0], P[:,1])
    else:
        yint = 1
    
    N = len(data)
    sum_x = np.sum(data)
    
    with np.errstate(divide='ignore', over='ignore', invalid='ignore'):
        Pu = (l**sum_x) * np.exp(-N * l) * yint
    
    Pu[~np.isfinite(Pu)] = 0
    
    C = np.trapz(Pu, l)
    if C == 0:
        C = 1.0 # Avoid division by zero if posterior is zero everywhere
    Pu = Pu / C
    
    where_l = Pu.argmax()
    max_l = l[where_l]
    
    d1 = 0
    intv1 = 0
    d2 = 1
    intv2 = 0
    sumintv = 0
    
    while (sumintv < CI*0.999):
        if (where_l + d1 < len(l)):
            d1 = d1 + 1
            indi = np.arange(where_l, where_l + d1, 1)
            intv1 = sum(Pu[indi]) * dl
        if (where_l + d2 > 0):
            d2 = d2 - 1
            indi = np.arange(where_l + d2, where_l, 1)
            intv2 = sum(Pu[indi]) * dl
        sumintv = intv1 + intv2

    idxU = min(where_l + d1, len(l) - 1)
    l_UP = l[idxU]
    idxL = max(where_l + d2, 0)
    l_LO = l[idxL]

###############################################################################
#####the ploting part##########################################################

    if plot:
        plt.figure(figsize=(10, 6))
        
        plt.plot(l, Pu, color='black', label='Posterior $P(\lambda|D)$')
        
        fill_indices = np.arange(idxL, idxU + 1)
        plt.fill_between(l[fill_indices], Pu[fill_indices], 
                         color='gray', alpha=0.4, label=f'{int(CI*100)}% Credible Interval')
        
        plt.axvline(max_l, color='red', linestyle='--', label=f'Max $\lambda = {max_l:.2f}$')
        plt.axvline(l_LO, color='blue', linestyle=':', label=f'Lower bound = {l_LO:.2f}')
        plt.axvline(l_UP, color='blue', linestyle=':', label=f'Upper bound = {l_UP:.2f}')
        
        plt.xlabel('Parameter $\lambda$')
        plt.ylabel('Posterior Probability Density $P(\lambda|data, I)$')
        diff_up = l_UP - max_l
        diff_do = max_l - l_LO
        plt.title(f'Bayesian Estimation for Poisson Parameter\n'
                  f'$\lambda = {max_l:.2f}^{{+{diff_up:.2f}}}_{{-{diff_do:.2f}}}$')
        plt.legend()
        plt.grid(True, linestyle=':', alpha=0.5)
        
        plt.show()

    bounds = [l_LO, max_l, l_UP]
    posterior_array = np.vstack((l, Pu)).T

    return (bounds, posterior_array)


#########################################################################

import math
import matplotlib.pyplot as plt

def prob_at_least_n(N, n, rho):
    """
    计算在 N 次独立检验中至少出现 n 个假阳性的概率（精确二项求和）。
    N: 非负整数
    n: 非负整数，要求至少 n 个
    rho: 单次假阳性概率（0 <= rho <= 1）
    """
    if n <= 0:
        return 1.0
    if n > N:
        return 0.0
    # 使用 1 - CDF(n-1) 的形式以减少求和量（和从 0 到 n-1）
    cdf = 0.0
    for k in range(0, n):
        cdf += math.comb(N, k) * (rho**k) * ((1-rho)**(N-k))
    return 1.0 - cdf

def plot_P_vs_N(N_max, n, rho):
    """
    画出 P(N) = Prob(at least n false positives after N tests) 的曲线，
    N 从 0 到 N_max。
    """
    N_vals = list(range(N_max + 1))
    P_vals = [prob_at_least_n(N, n, rho) for N in N_vals]

    plt.figure(figsize=(8,4.5))
    plt.plot(N_vals, P_vals, marker='o', linestyle='-')
    plt.xlabel("N (number of tests)")
    plt.ylabel(f"P(K ≥ {n}) with ρ={rho}")
    plt.title(f"Probability of at least {n} false positives vs N")
    plt.grid(True)
    plt.ylim(-0.02, 1.02)
    plt.show()

# 示例调用
if __name__ == "__main__":
    plot_P_vs_N(N_max=100, n=5, rho=0.05)
