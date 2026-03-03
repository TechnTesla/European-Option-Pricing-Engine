import numpy as np
from scipy.stats import norm

from src.monte_carlo import monte_carlo

def bs_greeks(S0, K, r, q, sigma, T, option_type):
    d1 = (np.log(S0/ K) + ((r - q + (sigma * sigma) / 2) * T)) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    gamma = np.exp(-q * T) * norm.pdf(d1) * (1 / (S0 *sigma *  np.sqrt(T))) 
    vega = S0 * np.exp(-q * T) * norm.pdf(d1) * np.sqrt(T)

    if option_type == "call":
        delta = np.exp(-q * T) * norm.cdf(d1) 
        theta = (-S0 *np.exp(-q * T) * norm.pdf(d1) * sigma) / (2 * np.sqrt(T)) - (r * K * np.exp(-r * T) * norm.cdf(d2)) + (q *S0 *np.exp(-q * T) * norm.cdf(d1))  
        rho = K * T * np.exp(-r * T) * norm.cdf(d2)  
    elif option_type == "put":
        delta = -np.exp(-q * T) * norm.cdf(-d1)
        theta = (-S0 *np.exp(-q * T) * norm.pdf(d1) * sigma) / (2 * np.sqrt(T)) + (r * K * np.exp(-r * T) * norm.cdf(-d2)) - (q *S0 *np.exp(-q * T) * norm.cdf(-d1))  
        rho = -K * T * np.exp(-r * T) * norm.cdf(-d2)
    else:
        raise ValueError("option_type must be either 'call' or 'put'")

    return {

        'delta' : delta,
        'gamma' : gamma,
        'vega' : vega,
        'theta' : theta,
        'rho' : rho
    }


# h stands for bump
def mc_delta(S0, K, r, q, sigma, T, N, option_type, h=1.0, seed=1):

    # the [0] only extracts the price from the monte carlo
    price_up =  monte_carlo(S0 + h, K, r, q, sigma, T, N, option_type, seed)[0]
    price_down = monte_carlo(S0 - h, K, r, q, sigma, T, N, option_type, seed)[0]
    delta = (price_up - price_down) / (2*h)
    
    return delta