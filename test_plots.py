import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Parameters
W0 = 1000
start_age = 20
N = 55 - start_age
n_sims = 100
seed = 20250918

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

# Set seed for reproducibility
np.random.seed(seed)

# Run simulations
print("Running simulations...")
finals_mod = np.array([simulate_modified_path()[-1] for _ in range(n_sims)])
finals_orig = np.array([simulate_original_path()[-1] for _ in range(n_sims)])

# Calculate probabilities
p_gt_10k_mod = (finals_mod > 10_000).mean()
p_gt_10k_orig = (finals_orig > 10_000).mean()

print(f"Modified strategy - P(final > $10,000): {p_gt_10k_mod:.3f}")
print(f"Original strategy - P(final > $10,000): {p_gt_10k_orig:.3f}")

# Create summary table
summary = pd.DataFrame({
    "strategy": ["modified_50pct_bet", "original_all_in"],
    "mean_final": [finals_mod.mean(), finals_orig.mean()],
    "median_final": [np.median(finals_mod), np.median(finals_orig)],
    "P(final > $10,000)": [p_gt_10k_mod, p_gt_10k_orig],
    "n_sims": [n_sims, n_sims],
    "N_flips": [N, N],
    "seed": [seed, seed],
})

print("\nSummary Results:")
print(summary)

# Create the required histogram for modified strategy
plt.figure(figsize=(10, 6))
plt.hist(finals_mod, bins=20, alpha=0.7, color='skyblue', edgecolor='black')
plt.axvline(10_000, color='red', linestyle='--', linewidth=2, label='$10,000 threshold')
plt.title(f'Modified Strategy: Final Balance Distribution\n(n={n_sims}, N={N})')
plt.xlabel('Final Balance ($)')
plt.ylabel('Frequency')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('modified_strategy_histogram.png', dpi=300, bbox_inches='tight')
plt.show()

print(f"\nKey Results:")
print(f"P(final > $10,000) for modified game: {p_gt_10k_mod:.3f} ({p_gt_10k_mod*100:.1f}%)")
print(f"P(final > $10,000) for original game: {p_gt_10k_orig:.3f} ({p_gt_10k_orig*100:.1f}%)")
print(f"Original strategy has {p_gt_10k_orig/p_gt_10k_mod:.1f}x higher probability of reaching $10,000+")

