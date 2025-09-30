import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Test the simulation challenge code
W0 = 1000
start_age = 20
N = 55 - start_age
n_sims = 100
seed = 20250918
np.random.seed(seed)

def simulate_original_path(w0=W0, n=N, p=0.5):
    """Original game: account x1.5 on heads, x0.6 on tails."""
    w = [w0]
    for _ in range(n):
        h = np.random.binomial(1, p)
        w.append(w[-1] * (1.5 if h else 0.6))
    return np.array(w)

def simulate_modified_path(w0=W0, n=N, p=0.5):
    """
    Modified game: must bet 50% each round.
    Account multipliers: 1.25 (heads) or 0.8 (tails).
    """
    w = [w0]
    for _ in range(n):
        h = np.random.binomial(1, p)
        w.append(w[-1] * (1.25 if h else 0.8))
    return np.array(w)

# Run simulations
print("Running simulations...")
finals_mod = np.array([simulate_modified_path()[-1] for _ in range(n_sims)])
finals_orig = np.array([simulate_original_path()[-1] for _ in range(n_sims)])

p_gt_10k_mod = (finals_mod > 10_000).mean()
p_gt_10k_orig = (finals_orig > 10_000).mean()

summary = pd.DataFrame({
    "strategy": ["modified_50pct_bet", "original_all_in"],
    "mean_final": [finals_mod.mean(), finals_orig.mean()],
    "median_final": [np.median(finals_mod), np.median(finals_orig)],
    "P(final > $10,000)": [p_gt_10k_mod, p_gt_10k_orig],
    "n_sims": [n_sims, n_sims],
    "N_flips": [N, N],
    "seed": [seed, seed],
})

print("\nResults:")
print(summary)

print(f"\nP(final > $10,000) for modified strategy: {p_gt_10k_mod:.3f}")
print(f"P(final > $10,000) for original strategy: {p_gt_10k_orig:.3f}")

# Create visualization
plt.figure(figsize=(9,5))
plt.hist(finals_mod, bins=20)
plt.axvline(10_000, linestyle="--", linewidth=2, color='red', label='$10,000 threshold')
plt.title(f"Modified Strategy: Final Balance Distribution (n={n_sims}, N={N})")
plt.xlabel("Final Balance ($)")
plt.ylabel("Frequency")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig('simulation_challenge_results.png', dpi=300, bbox_inches='tight')
plt.show()

print("\nVisualization saved as 'simulation_challenge_results.png'")
