import numpy as np
from scipy.stats import norm
#Takes in inputs of spot, strike, time to maturity, implied vol, 
# the risk free rate and dividend yield then outputs the BS fair value
# of an European option (also takes a string call or put so it knows which type)


#S0 is spot, K is strike, r is risk free rate, q is dividend yield
# #sigma is implied vol, T is time to expiry 
def black_scholes(S0, K, r, q, sigma, T, option_type):
     d1 = (np.log(S0/ K) + ((r - q + (sigma * sigma) / 2) * T)) / (sigma * np.sqrt(T))
     d2 = d1 - sigma * np.sqrt(T)  

     if option_type == 'call':
        value = (S0 * np.exp(-q * T) * norm.cdf(d1)) - (K * np.exp(-r * T) * norm.cdf(d2)) 
     elif option_type == 'put':
        value = (K * np.exp(-r * T) * norm.cdf(-d2)) - (S0 * np.exp(-q * T) * norm.cdf(-d1))
     else:
         raise ValueError("option_type must be either 'call' or 'put'")
     return value