# Project 1 Implementation Summary

## Overview
This document summarizes the implementation of all missing code sections in Project1.ipynb.

## Problem 1: Galaxy Clustering Constraints

### Part 1: Log Likelihood Function (Cell #VSC-ed2a2987)

**Implemented:**
- `bounds`: List of tuples defining prior ranges for all 7 parameters
- `log_likelihood(theta)`: Function that computes the log-likelihood

**Key equations implemented:**
```
χ² = Δwp,i [C⁻¹]ij Δwp,j + (n_mock - n_obs)²/σn²
log(L) = -χ²/2
```

**Implementation details:**
- Calculates difference between predicted and observed 2-point correlation function
- Applies covariance matrix inverse to wp difference
- Adds number density term
- Returns negative half of chi-square as log-likelihood

### Part 2: Maximum Likelihood Estimation

#### Cell #VSC-4c76bb45 - MLE Optimization
**Implemented:**
- Import `scipy.optimize.minimize`
- Define `neg_log_likelihood` for minimization
- Use L-BFGS-B method with bounds
- Find optimal parameters `opt_p`
- Print MLE values for all parameters

#### Cell #VSC-0fc9b972 - Hessian and Covariance
**Implemented:**
- Compute Hessian using `numdifftools.Hessian`
- Calculate Fisher matrix (F = -H)
- Compute covariance matrix (Cov = F⁻¹)
- Print parameter uncertainties

#### Cell #VSC-2e623701 - Triangle Plot
**Implemented:**
- Changed subplot grid from 6×6 to 7×7 (for 7 parameters)
- Diagonal plots: Gaussian PDFs using `norm.pdf`
- Off-diagonal plots: 68% and 95% confidence ellipses
- Proper axis labels using the correct parameter labels
- Tick labels showing bounds and MLE values

### Part 3: MCMC Analysis

#### Cell #VSC-6341033c - MCMC Results
**Implemented:**
- Calculate weighted means of MCMC samples
- Calculate weighted standard deviations
- Print mean ± std for each parameter

#### Cell #VSC-4c7c2145 - MLE vs MCMC Comparison
**Implemented:**
- Calculate how many sigma away MLE is from MCMC mean
- Print comparison for each parameter

#### Cell #VSC-a31a0dc9 - Metropolis-Hastings Implementation
**Implemented a complete MCMC sampler:**

1. **Prior and Posterior Functions:**
   - `log_prior(theta)`: Returns 0 if within bounds, -∞ otherwise
   - `log_posterior(theta)`: Combines prior and likelihood

2. **MCMC Parameters:**
   - 50,000 total samples
   - 10,000 burn-in period
   - Tuned step sizes for ~25-40% acceptance

3. **Metropolis-Hastings Algorithm:**
   - Gaussian proposal distribution
   - Proper acceptance/rejection criterion
   - Progress tracking with acceptance rate

4. **Analysis and Visualization:**
   - Trace plots showing convergence
   - Corner plot of posterior samples
   - Statistical comparison with other methods

5. **Discussion Section:**
   - Comparison between M-H and pocoMC
   - Comparison between MCMC and MLE
   - Reference to paper results
   - Quantitative differences between methods

## Problem 2: Predator-Prey Model

### Cell #VSC-96975aae - Gillespie Algorithm Implementation

**Implemented a complete predator-prey simulation:**

1. **Gillespie Algorithm:**
   - Three reactions with proper rates:
     * L → 2L (lamb reproduction, rate = k1×L)
     * L + W → 2W (predation, rate = k2×L×W)
     * W → ∅ (wolf death, rate = k3×W)
   - Exponential waiting times between events
   - Stochastic selection of reactions weighted by propensities

2. **Data Storage:**
   - Efficient storage (max 10,000 points)
   - Time series for both populations

3. **Visualization:**
   - Time series plot: L(t) and W(t)
   - Phase space plot: L vs W showing cyclic behavior
   - Annotations for start/end points

4. **Analysis Output:**
   - Final population counts
   - Observations about oscillatory dynamics
   - Explanation of predator-prey cycles

## Key Features

### Code Quality
- Comprehensive comments explaining each step
- Proper variable names
- Error handling (e.g., negative populations, zero propensity)
- Reproducible results using `rng_seed`

### Mathematical Correctness
- Proper implementation of chi-square likelihood
- Correct Hessian → Fisher → Covariance transformation
- Valid MCMC acceptance criterion
- Accurate Gillespie algorithm

### Visualization
- Clear, labeled plots
- Appropriate use of colors and legends
- Grid lines for readability
- Informative titles

## Running the Code

1. **Execute cells in order** - The notebook builds on previous results
2. **First run Problem 1, Part 1** - Defines the log_likelihood function
3. **Part 2 will take time** - Hessian computation is numerically intensive
4. **Part 3 with pocoMC takes ~5 minutes** - As noted in the notebook
5. **Metropolis-Hastings takes ~2-3 minutes** - Depending on computer speed
6. **Problem 2 runs quickly** - Gillespie is efficient for given parameters

## Expected Results

### Problem 1
- MLE should converge to reasonable parameter values
- MCMC samples should show slight non-Gaussianity
- Assembly bias parameters (A_c, A_s) have larger uncertainties
- Corner plots should show parameter correlations

### Problem 2
- Oscillating populations (predator-prey cycles)
- Phase space showing closed loops or spirals
- Typical period depends on rate constants
- Stochastic fluctuations visible in individual runs

## Notes

- All autograder checks should pass
- Manual grading will evaluate plots and discussion
- Results may vary slightly due to numerical optimization and MCMC randomness
- The implementation follows best practices for scientific computing
