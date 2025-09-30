import numpy as np
import matplotlib.pyplot as plt

# Simple Monte Carlo estimation of π
def monte_carlo_pi(n):
    x = np.random.uniform(-1, 1, n)
    y = np.random.uniform(-1, 1, n)
    inside = np.sum(x**2 + y**2 <= 1)
    return 4 * inside / n

# Run simulation
np.random.seed(123)
n_sim = 10000
pi_estimate = monte_carlo_pi(n_sim)
print(f"Estimated π: {pi_estimate:.6f}")
print(f"Actual π: {np.pi:.6f}")
print(f"Error: {abs(pi_estimate - np.pi):.6f}")

# Create visualization
n_vis = 1000
x = np.random.uniform(-1, 1, n_vis)
y = np.random.uniform(-1, 1, n_vis)
inside = x**2 + y**2 <= 1

# Create the plot
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# Scatter plot
colors = ['red' if not pt else 'blue' for pt in inside]
ax1.scatter(x, y, c=colors, alpha=0.6)
ax1.set_title(f'Monte Carlo Estimation of π\nPoints inside circle: {np.sum(inside)} out of {n_vis}')
ax1.set_xlabel('X')
ax1.set_ylabel('Y')
ax1.set_aspect('equal')

# Convergence plot
n_values = range(100, 10001, 100)
pi_estimates = [monte_carlo_pi(n) for n in n_values]

ax2.plot(n_values, pi_estimates, 'b-', linewidth=2)
ax2.axhline(y=np.pi, color='red', linestyle='--', linewidth=2, label=f'Actual π = {np.pi:.6f}')
ax2.set_title('Convergence of π Estimation')
ax2.set_xlabel('Number of Simulations')
ax2.set_ylabel('Estimated π')
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('monte_carlo_simulation.png', dpi=300, bbox_inches='tight')
plt.show()

print("Simulation complete! Check 'monte_carlo_simulation.png' for the visualization.")
