import numpy as np
from scipy.stats import norm



#S0 is spor price, K is the strike price, r is the risk free rate
#q is the dividend yield, sigma is IV, T is time to maturity
#N is the number of simulations and option_type is wheteher its a call or a put 
def monte_carlo(S0, K, r, q, sigma, T, N, option_type, seed = 1):
    # the seed cannot be constant due to random seed variance
    #lets avg over multiple runs
    np.random.seed(seed)
    Z = np.random.standard_normal(N)

    #Geometric Brownian Motion handles the randomness of the option moving
    #an array of option payoffs
    ST = S0 * np.exp(((r - q - (0.5 * sigma * sigma))) * T  + sigma * np.sqrt(T) * Z )

    #if payoff is greater than zero take it else zero -> compure average then discount
    if option_type == 'call':
        payoffs =  np.maximum(ST - K, 0)
    elif option_type == 'put':
        payoffs = np.maximum(K - ST, 0)
    else:
        raise ValueError("option_type must be 'call' or 'put'")   
    

    #discounting handles the time value
    price = np.mean(payoffs) * np.exp(-r *T )

    #ddof here serves to act as the number you subtract in the denominator 
    #of rhe coefficent in the std.dev formula 
    std_error = np.std(payoffs, ddof = 1) * (1 / np.sqrt(N))

    #this is a 95% confidene interval, 95%is chosen at our discresion 
    #the constant 1.96 arises from our choice as it is 1.96 std.devs from the centre
    confidence_interval = (price - 1.96 * std_error, price + 1.96 * std_error )

    return price, std_error, confidence_interval