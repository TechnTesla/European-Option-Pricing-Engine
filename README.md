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

---
> This is my first quantitative finance project, built from scratch with no prior Python or finance experience.

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


## Black–Scholes (Analytical) Pricer

We use the **Black–Scholes formula** as the benchmark “true” price for a European option because it is an **analytical (closed-form)** solution: it returns the fair value directly (no simulation noise). Starting from the same **GBM** stock model and applying **Itô’s Lemma**, the Black–Scholes price follows from **risk-neutral pricing** (no-arbitrage).

Under risk-neutral pricing, we replace the real-world drift \( \mu \) with \( r-q \). This prevents arbitrage by ensuring that (after hedging away risk in the derivation) any locally risk-free position grows at the **risk-free rate** \( r \). That’s why option values are **discounted** at \( r \): future payoffs are priced as present values.

### Risk-neutral GBM
![risk-neutral-gbm](https://latex.codecogs.com/svg.latex?\dpi{140}\color{White}dS_t=(r-q)S_t\,dt+\sigma%20S_t\,dW_t)

### Inputs (what the function takes)
`black_scholes(S0, K, r, q, sigma, T, option_type)`

- `S0`: current spot price  
- `K`: strike price  
- `r`: risk-free rate (used for discounting)  
- `q`: continuous dividend yield  
- `sigma`: implied volatility  
- `T`: time to maturity (years)  
- `option_type`: `'call'` or `'put'`  

### Closed-form Black–Scholes solution
![d1d2](https://latex.codecogs.com/svg.latex?\dpi{140}\color{White}d_1=\frac{\ln(S_0/K)+(r-q+\tfrac12\sigma^2)T}{\sigma\sqrt{T}},\quad%20d_2=d_1-\sigma\sqrt{T})

![call](https://latex.codecogs.com/svg.latex?\dpi{140}\color{White}C=S_0e^{-qT}N(d_1)-Ke^{-rT}N(d_2))

![put](https://latex.codecogs.com/svg.latex?\dpi{140}\color{White}P=Ke^{-rT}N(-d_2)-S_0e^{-qT}N(-d_1))

### Validation: call–put parity (no-arbitrage check)
Call–put parity links calls and puts through the same discounted components. For the same \((S_0,K,r,q,\sigma,T)\), the prices must satisfy:

![parity](https://latex.codecogs.com/svg.latex?\dpi{140}\color{White}C-P=S_0e^{-qT}-Ke^{-rT})

If the computed call and put violate parity beyond a small tolerance, it indicates an implementation error.

> Note: the equations are forced to white (`\color{White}`) for dark themes. If you view the README in light mode, you may want to remove `\color{White}` from the image URLs.
