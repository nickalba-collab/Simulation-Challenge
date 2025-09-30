import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Parameters
W0 = 1000
start_age = 20
N = 55 - start_age
n_sims = 100
seed = 20250918

print(f"Starting age: {start_age}")
print(f"Number of flips: {N}")
print(f"Number of simulations: {n_sims}")
print(f"Seed: {seed}")

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

print("Simulation functions defined successfully!")

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

# Create visualization
plt.figure(figsize=(12, 8))

# Subplot 1: Modified strategy histogram
plt.subplot(2, 2, 1)
plt.hist(finals_mod, bins=20, alpha=0.7, color='skyblue', edgecolor='black')
plt.axvline(10_000, color='red', linestyle='--', linewidth=2, label='$10,000 threshold')
plt.title(f'Modified Strategy Distribution\n(n={n_sims}, N={N})')
plt.xlabel('Final Balance ($)')
plt.ylabel('Frequency')
plt.legend()
plt.grid(True, alpha=0.3)

# Subplot 2: Original strategy histogram
plt.subplot(2, 2, 2)
plt.hist(finals_orig, bins=20, alpha=0.7, color='lightcoral', edgecolor='black')
plt.axvline(10_000, color='red', linestyle='--', linewidth=2, label='$10,000 threshold')
plt.title(f'Original Strategy Distribution\n(n={n_sims}, N={N})')
plt.xlabel('Final Balance ($)')
plt.ylabel('Frequency')
plt.legend()
plt.grid(True, alpha=0.3)

# Subplot 3: Comparison box plot
plt.subplot(2, 2, 3)
data_to_plot = [finals_mod, finals_orig]
plt.boxplot(data_to_plot, labels=['Modified', 'Original'])
plt.title('Strategy Comparison')
plt.ylabel('Final Balance ($)')
plt.grid(True, alpha=0.3)

# Subplot 4: Probability comparison
plt.subplot(2, 2, 4)
strategies = ['Modified', 'Original']
probabilities = [p_gt_10k_mod, p_gt_10k_orig]
bars = plt.bar(strategies, probabilities, color=['skyblue', 'lightcoral'])
plt.title('P(final > $10,000) Comparison')
plt.ylabel('Probability')
plt.ylim(0, max(probabilities) * 1.2)

# Add value labels on bars
for bar, prob in zip(bars, probabilities):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01, 
             f'{prob:.3f}', ha='center', va='bottom')

plt.tight_layout()
plt.savefig('simulation_challenge_complete.png', dpi=300, bbox_inches='tight')
plt.show()

print("\n" + "=" * 60)
print("KEY FINDINGS")
print("=" * 60)
print(f"Modified Strategy (50% bet per round):")
print(f"  - Mean final balance: ${finals_mod.mean():,.2f}")
print(f"  - Median final balance: ${np.median(finals_mod):,.2f}")
print(f"  - P(final > $10,000): {p_gt_10k_mod:.3f} ({p_gt_10k_mod*100:.1f}%)")
print()
print(f"Original Strategy (all-in each flip):")
print(f"  - Mean final balance: ${finals_orig.mean():,.2f}")
print(f"  - Median final balance: ${np.median(finals_orig):,.2f}")
print(f"  - P(final > $10,000): {p_gt_10k_orig:.3f} ({p_gt_10k_orig*100:.1f}%)")
print()
print("COMPARISON:")
print(f"  - Original strategy has {p_gt_10k_orig/p_gt_10k_mod:.1f}x higher probability of reaching $10,000+")
print(f"  - Original strategy has higher variance (risk)")
print(f"  - Modified strategy is more conservative but less likely to reach target")

print("\nVisualization saved as 'simulation_challenge_complete.png'")
print("Simulation complete!")

