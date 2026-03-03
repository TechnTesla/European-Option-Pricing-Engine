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



## Black–Scholes (Analytical) Pricer — Math Behind the Formula

This project includes a **closed-form** Black–Scholes calculator for European calls and puts. The formula is derived from:

1) **GBM** for the underlying  
2) **Itô’s Lemma** to obtain option dynamics  
3) **No-arbitrage / delta-hedging** to remove risk  
4) The resulting **Black–Scholes PDE**, solved in closed form  
5) **Call–put parity** as a verification check  

---

### 1) Stock model (GBM)

![GBM](https://latex.codecogs.com/svg.latex?\dpi{120}dS_t=\mu%20S_t\,dt+\sigma%20S_t\,dW_t)

Where:
- `S_t` is the stock price
- `μ` is drift (real-world)
- `σ` is volatility
- `W_t` is Brownian motion

---

### 2) Itô’s Lemma (option dynamics)

Let the option value be `V(S,t)`. Applying Itô’s Lemma:

![Ito](https://latex.codecogs.com/svg.latex?\dpi{120}dV=\Big(\frac{\partial%20V}{\partial%20t}+\mu%20S\frac{\partial%20V}{\partial%20S}+\frac{1}{2}\sigma^2S^2\frac{\partial^2%20V}{\partial%20S^2}\Big)\,dt+\sigma%20S\frac{\partial%20V}{\partial%20S}\,dW)

This splits `dV` into a deterministic `dt` part and a random `dW` part.

---

### 3) Delta-hedging + no-arbitrage ⇒ Black–Scholes PDE

Choose the hedge ratio:

![Delta](https://latex.codecogs.com/svg.latex?\dpi{120}\Delta=\frac{\partial%20V}{\partial%20S})

Form a hedged portfolio `Π = V − ΔS` to cancel the `dW` term.  
A riskless portfolio must earn the risk-free rate `r`. With continuous dividend yield `q`, no-arbitrage implies the **Black–Scholes PDE**:

![PDE](https://latex.codecogs.com/svg.latex?\dpi{120}\frac{\partial%20V}{\partial%20t}+(r-q)S\frac{\partial%20V}{\partial%20S}+\frac{1}{2}\sigma^2S^2\frac{\partial^2%20V}{\partial%20S^2}-rV=0)

Expiry boundary conditions:
- Call: `V(S,T) = max(S − K, 0)`
- Put:  `V(S,T) = max(K − S, 0)`

---

### 4) Closed-form Black–Scholes solution

Define:

![d1](https://latex.codecogs.com/svg.latex?\dpi{120}d_1=\frac{\ln(S_0/K)+(r-q+\frac{1}{2}\sigma^2)T}{\sigma\sqrt{T}})
  
![d2](https://latex.codecogs.com/svg.latex?\dpi{120}d_2=d_1-\sigma\sqrt{T})

Let `N(.)` be the standard normal CDF.

Call:

![Call](https://latex.codecogs.com/svg.latex?\dpi{120}C=S_0e^{-qT}N(d_1)-Ke^{-rT}N(d_2))

Put:

![Put](https://latex.codecogs.com/svg.latex?\dpi{120}P=Ke^{-rT}N(-d_2)-S_0e^{-qT}N(-d_1))

This is what `black_scholes.py` implements.

---

### 5) Verification via call–put parity

For European options:

![Parity](https://latex.codecogs.com/svg.latex?\dpi{120}C-P=S_0e^{-qT}-Ke^{-rT})

Parity is a quick check that the call and put implementations are internally consistent for the same inputs.
