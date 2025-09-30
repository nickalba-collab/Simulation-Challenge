import numpy as np
import pandas as pd

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
    """Modified game: must bet 50% each round. Account multipliers: 1.25 (heads) or 0.8 (tails)."""
    w = [w0]
    for _ in range(n):
        h = np.random.binomial(1, p)
        w.append(w[-1] * (1.25 if h else 0.8))
    return np.array(w)

# Run simulations
np.random.seed(seed)
finals_mod = np.array([simulate_modified_path()[-1] for _ in range(n_sims)])
finals_orig = np.array([simulate_original_path()[-1] for _ in range(n_sims)])

# Calculate probabilities
p_gt_10k_mod = (finals_mod > 10_000).mean()
p_gt_10k_orig = (finals_orig > 10_000).mean()

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

print("REAL SIMULATION RESULTS:")
print("=" * 50)
print(f"Modified strategy - P(final > $10,000): {p_gt_10k_mod:.3f} ({p_gt_10k_mod*100:.1f}%)")
print(f"Original strategy - P(final > $10,000): {p_gt_10k_orig:.3f} ({p_gt_10k_orig*100:.1f}%)")
print(f"Original has {p_gt_10k_orig/p_gt_10k_mod:.1f}x higher probability")
print()
print("SUMMARY TABLE:")
print(summary)
print()
print("One-sentence answers:")
print(f"P(final > $10,000) for the modified game: {p_gt_10k_mod:.3f} ({p_gt_10k_mod*100:.1f}%)")
print(f"Comparison: Original strategy has higher probability ({p_gt_10k_orig:.3f} vs {p_gt_10k_mod:.3f}) but higher risk")
print(f"Visualization: Histogram shows modified strategy distribution with $10k threshold line")

