# European Option Pricing Engine

A European option is a financial contract giving the holder the right, but not the 
obligation, to buy (call) or sell (put) an underlying asset at a fixed strike price 
on a specific expiry date. Pricing these contracts fairly is a fundamental problem 
in quantitative finance — one that sits at the intersection of probability theory, 
stochastic calculus, and numerical methods.

---

## Overview

This project builds a complete European option pricing engine from first principles, implementing and validating multiple pricing methodologies:

- **Geometric Brownian Motion (GBM)** to model stock price evolution under risk-neutral pricing
- **Black-Scholes formula** derived via Itô's Lemma — a closed-form analytical solution
- **Monte Carlo simulation** as a numerical alternative, averaging thousands of simulated stock paths
- **Antithetic variates** for variance reduction — achieving lower error at the same computational cost
- **Option Greeks** computed analytically (BS) and numerically (finite differences on MC)
- **3D pricing surface** visualising call and put prices across all strikes and maturities

## Project Structure
```
European-Option-Pricing-Engine/
├── src/
│   ├── black_scholes.py       # Analytical BS pricer
│   ├── monte_carlo.py         # MC simulation pricer
│   ├── variance_reduction.py  # Antithetic variates implementation
│   └── greeks.py              # BS analytical Greeks and MC delta
├── results/
│   └── plots/
│       ├── convergence.png    # MC vs BS price convergence
│       ├── delta.png          # MC vs BS delta convergence
│       └── options_surface.png # 3D pricing surface
├── main.py                    # Entry point — runs all pricing and plots
├── requirements.txt           # Dependencies
└── README.md
```


### What This Project Demonstrates
| Component | Method | Key Result |
|-----------|--------|------------|
| Option Pricing | Black-Scholes & Monte Carlo | MC converges to BS at O(N⁻¹/²) |
| Variance Reduction | Antithetic Variates | 33% reduction in standard error at same N |
| Sensitivities | BS Greeks & MC Finite Differences | MC delta converges to BS delta at O(N⁻¹/²) |
| Pricing Landscape | 3D BS Surface | Full call/put surface across strike and maturity |

---

## Key Results

Running with parameters S₀=100, K=100, r=0.05, σ=0.20, T=1.0, q=0.0:

| Method | Price | Std Error | 95% CI |
|--------|-------|-----------|--------|
| Black-Scholes (Analytical) | 10.4506 | — | — |
| Monte Carlo (N=10,000) | 10.5515 | 0.1566 | (10.2446, 10.8584) |
| Antithetic Variates (N=10,000) | 10.4692 | 0.1044 | (10.2646, 10.6738) |

| Greek | BS Analytical | MC Finite Diff | Difference |
|-------|--------------|----------------|------------|
| Delta | 0.6368 | 0.6432 | 0.0063 |
| Gamma | 0.0188 | — | — |
| Vega | 37.5240 | — | — |
| Theta | -6.4140 | — | — |
| Rho | 53.2325 | — | — |



---
> This is my first quantitative finance project, built from scratch with no prior Python or finance experience.
## Black–Scholes (Analytical) Pricer — Math Behind the Formula

This project includes a **closed-form** Black–Scholes calculator for European calls and puts. The formula is not “assumed”; it is derived from:

1) **Geometric Brownian Motion (GBM)** for the underlying  
2) **Itô’s Lemma** to get the option’s stochastic dynamics  
3) **No-arbitrage / delta-hedging** to eliminate risk  
4) The resulting **Black–Scholes PDE**, solved to obtain a closed-form price  
5) **Call–put parity** as a verification check

---

### 1) Stock model (GBM)
We assume the stock price follows GBM:

\[
dS_t = \mu S_t\,dt + \sigma S_t\,dW_t
\]

- \(S_t\): stock price  
- \(\mu\): real-world drift  
- \(\sigma\): volatility  
- \(W_t\): Brownian motion  

---

### 2) Itô’s Lemma (option dynamics)
Let the option value be \(V(S,t)\). Applying Itô’s Lemma:

\[
dV = \Big(\frac{\partial V}{\partial t} + \mu S\frac{\partial V}{\partial S} + \frac{1}{2}\sigma^2 S^2 \frac{\partial^2 V}{\partial S^2}\Big)dt
+ \sigma S\frac{\partial V}{\partial S}\,dW
\]

This separates the option change into:
- a deterministic \(dt\) term, and
- a random \(dW\) term.

---

### 3) Delta-hedging + no-arbitrage ⇒ Black–Scholes PDE
Form a hedged portfolio \(\Pi = V - \Delta S\) with \(\Delta = \partial V/\partial S\).  
This choice cancels the stochastic term, making \(\Pi\) locally riskless.

A riskless portfolio must earn the risk-free rate. With continuous dividend yield \(q\), the no-arbitrage condition yields the **Black–Scholes PDE**:

\[
\frac{\partial V}{\partial t}
+ (r-q)S\frac{\partial V}{\partial S}
+ \frac{1}{2}\sigma^2 S^2\frac{\partial^2 V}{\partial S^2}
- rV = 0
\]

Boundary conditions at expiry \(t=T\):
- Call payoff: \(\;V(S,T)=\max(S-K,0)\)
- Put payoff:  \(\;V(S,T)=\max(K-S,0)\)

---

### 4) Closed-form Black–Scholes solution
Solving the PDE gives the Black–Scholes closed-form prices.

Define:

\[
d_1 = \frac{\ln(S_0/K) + (r-q+\frac{1}{2}\sigma^2)T}{\sigma\sqrt{T}},
\qquad
d_2 = d_1 - \sigma\sqrt{T}
\]

Let \(N(\cdot)\) be the standard normal CDF.

**Call:**
\[
C = S_0 e^{-qT}N(d_1) - Ke^{-rT}N(d_2)
\]

**Put:**
\[
P = Ke^{-rT}N(-d_2) - S_0 e^{-qT}N(-d_1)
\]

This is what the `black_scholes.py` module implements.

---

### 5) Verification via call–put parity
A key consistency check is **call–put parity** (European options):

\[
C - P = S_0 e^{-qT} - Ke^{-rT}
\]

In this repo, parity is used to verify that the call and put implementations are internally consistent for the same \((S_0, K, r, q, \sigma, T)\).

