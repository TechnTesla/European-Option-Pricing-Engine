import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from mpl_toolkits.mplot3d import Axes3D


from src.black_scholes import black_scholes
from src.monte_carlo import monte_carlo
from src.variance_reduction import var_reduction
from src.greeks import bs_greeks
from src.greeks import mc_delta

#Fixed Parameters
S0 = 100 #spot price
K = 100 #strike price
R = 0.05 #risk free int
Q = 0.0 # dividends
SIGMA = 0.2 # implied volatility
T = 1.0   # time to maturity (years)

N_RUNS = 10

def test_pricers():
    
    bs_price = black_scholes(S0, K, R, Q, SIGMA, T, 'call')
    mc_price, mc_se, mc_ci = monte_carlo(S0, K, R, Q, SIGMA, T, 10000, 'call')
    
    print(f"BS price:   {bs_price:.4f}")
    print(f"MC price:   {mc_price:.4f}")
    print(f"Std error:  {mc_se:.4f}")
    print(f"95% CI:     ({mc_ci[0]:.4f}, {mc_ci[1]:.4f})")
    print(f"Difference: {abs(bs_price - mc_price):.4f}")

    av_price, av_se, av_ci = var_reduction(S0, K, R, Q, SIGMA, T, 10000, 'call')

    print(f"\nAntithetic price: {av_price:.4f}")
    print(f"Antithetic SE:    {av_se:.4f}")
    print(f"Antithetic CI:    ({av_ci[0]:.4f}, {av_ci[1]:.4f})")

    greeks = bs_greeks(S0, K, R, Q, SIGMA, T, 'call')

    print(f"\nBS Greeks (Call):")
    print(f"Delta: {greeks['delta']:.4f}")
    print(f"Gamma: {greeks['gamma']:.4f}")
    print(f"Vega:  {greeks['vega']:.4f}")
    print(f"Theta: {greeks['theta']:.4f}")
    print(f"Rho:   {greeks['rho']:.4f}")

    print(f"\nMC Delta vs BS Delta (Call):")
    mc_d = mc_delta(S0, K, R, Q, SIGMA, T, 10000 ,'call', h = 1.0, seed=1)
    print(f"MC Delta:   {mc_d:.4f}")
    print(f"BS Delta:   {greeks['delta']:.4f}")
    print(f"Difference: {abs(mc_d - greeks['delta']):.4f}")


def plot_convergence():
    #we are plotting the difference between bs and mc
    N_values = [10**i for i in range(2, 7)]
    bs_price = black_scholes(S0, K, R, Q, SIGMA, T, 'call' )

    mc_errors = []
    av_errors = []

    for N in N_values:
        errors_at_N = [] #temp list of the specific N
        errors_for_av = []  

        for run in range(N_RUNS):
            mc_price, mc_se, mc_ci = monte_carlo(S0, K, R, Q, SIGMA, T, N, 'call', seed=run) 
            av_price, av_se, av_ci = var_reduction(S0, K, R, Q, SIGMA, T, N, 'call', seed=run)
            
            errors_at_N.append(np.mean(abs(mc_price - bs_price)))
            errors_for_av.append(np.mean(abs(av_price - bs_price)))

        mc_errors.append(np.mean(errors_at_N) )
        av_errors.append(np.mean(errors_for_av))

    fig, ax = plt.subplots()
    ax.loglog(N_values, mc_errors, label = 'MC_Baseline')
    ax.set_xlabel("Number of Simulations (N)")
    ax.set_ylabel("Absolute Error")
    ax.set_title("Monte Carlo Convergence")

    ax.loglog(N_values, av_errors, label='Antithetic Variates')
    ax.loglog(N_values, np.array(N_values)**(-0.5), linestyle='--', label='O(N^-0.5) reference')
    ax.legend()


    plt.savefig("results/plots/convergence.png")
    plt.show()
    plt.close()

def plot_delta_convergence():
    N_values = [10**i for i in range (2,7)]
    bs_delta = bs_greeks(S0, K, R, Q, SIGMA, T, "call")["delta"]
    mc_deltas = []

    for N in N_values:
        errors_at_N_delta = []

        for run in range(N_RUNS):
            errors_at_N_delta.append(abs(mc_delta(S0, K, R, Q, SIGMA, T, N, "call", 1.0, seed=run) - bs_delta))

        mc_deltas.append(np.mean(errors_at_N_delta))   

    fig, ax = plt.subplots()
    ax.loglog(N_values, mc_deltas, label = 'MC_DELTA')
    ax.set_xlabel("Number of Simulations (N)")
    ax.set_ylabel("Absolute Error")
    ax.set_title("Monte Carlo DELTA Convergence")

    ax.loglog(N_values, np.array(N_values)**(-0.5), linestyle='--', label='O(N^-0.5) reference')
    ax.legend()


    plt.savefig("results/plots/delta.png")
    plt.show()
    plt.close()

def options_pricing_surface():
    #We are taking 50 strike values from 60 to 140
    K_values = np.linspace(60, 140, 50)
    #We are taking 50 time to expiry values from 0.1 to 2.0 (years)
    T_values = np.linspace(0.1, 2.0, 50)

    #We are now making our 2Darrays so that each strike will have enough values
    #to match its corresponding time to expiry counterpart
    K_grid, T_grid = np.meshgrid(K_values, T_values)

    #We are creating 2D arrays [i][j], i index is time value, j index is strike value
    # AND the value held at this point is the price of the option  
    call_prices = black_scholes(S0, K_grid, R, Q, SIGMA, T_grid, 'call')
    put_prices = black_scholes(S0, K_grid, R, Q, SIGMA, T_grid, 'put')

    fig, (ax1, ax2) = plt.subplots(1, 2, subplot_kw={'projection' : '3d'}, figsize=(14, 6))

    surf1 = ax1.plot_surface(K_grid, T_grid, call_prices, cmap='viridis')
    ax1.set_xlabel('Strike Price K ($)')
    ax1.set_ylabel('Time to Maturity (Years)')
    ax1.set_zlabel('Option Price ($)')
    ax1.set_title('Call Price Surface')
    fig.colorbar(surf1, ax=ax1, shrink=0.5, label='Price ($)')

    surf2 = ax2.plot_surface(K_grid, T_grid, put_prices, cmap='plasma')
    ax2.set_xlabel('Strike Price K ($)')
    ax2.set_ylabel('Time to Maturity (Years)')
    ax2.set_zlabel('Option Price ($)')
    ax2.set_title('Put Price Surface')
    fig.colorbar(surf2, ax=ax2, shrink=0.5, label='Price ($)')


    plt.suptitle('Black-Scholes Option Pricing Surface')
    plt.savefig("results/plots/options_surface.png")
    plt.show()
    plt.close()


if __name__ == "__main__":
    test_pricers()
    plot_convergence()
    plot_delta_convergence()
    options_pricing_surface()