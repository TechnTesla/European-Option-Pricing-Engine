import numpy as np
from scipy.stats import norm

#S0 is spot, K is strike, r is risk free rate, q is dividends
#sigma is impied volatility, Tis time to expiry and Nis no. of simulations  

def var_reduction(S0, K, r, q, sigma, T, N, option_type, seed = 1):
    np.random.seed(seed)
    Z = np.random.standard_normal(N // 2)
    
    ST_pos = S0 * np.exp(((r - q - (0.5 * sigma * sigma))) * T  + sigma * np.sqrt(T) * Z )
    ST_neg = S0 * np.exp(((r - q - (0.5 * sigma * sigma))) * T  + sigma * np.sqrt(T) * -Z )

    if option_type == "call":
        payoff_pos = np.maximum(ST_pos - K, 0)
        payoff_neg = np.maximum(ST_neg - K, 0)
    elif option_type == "put":
        payoff_pos = np.maximum(K - ST_pos, 0)
        payoff_neg = np.maximum(K - ST_neg, 0)
    else:    
        raise ValueError("option_type must be 'call' or 'put'")
    

    payoff = (payoff_pos + payoff_neg) / 2

    #time value discounting
    price = np.mean(payoff) * np.exp(-r * T)

    std_error = np.exp(-r * T) * np.std(payoff, ddof = 1) * (1 / np.sqrt(N // 2))

    #this is a 95% confidene interval, 95%is chosen at our discresion 
    #the constant 1.96 arises from our choice as it is 1.96 std.devs from the centre
    confidence_interval = (price - 1.96 * std_error, price + 1.96 * std_error )

    return price, std_error, confidence_interval