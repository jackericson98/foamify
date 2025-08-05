import matplotlib.pyplot as plt
import numpy as np
from joblib import load
import pandas as pd

# Load your model
model = load('C:/Users/Optiplex_7060/PycharmProjects/foam_gen/Data/linreg_pipeline.pkl')

densities = np.linspace(0.1, 0.75, 100)
distribution = 'gamma'
mean = 1.0
params = [(overlap, num, cv) for overlap in [1.5, 1.0, 0.5] for num in [100, 1000] for cv in [0.5, 1.0]]
colors = plt.cm.rainbow(np.linspace(0, 1, len(params)))  # Color map for differentiation
fig, ax = plt.subplots(figsize=(10, 7))  # Increase figure size

# Plot each set of parameters
for (overlap, num, cv), color in zip(params, colors):
    new_data = pd.DataFrame({
        'Adjusted Density': densities, 'Mean': [mean] * len(densities),
        'CV': [cv] * len(densities), 'Number': [num] * len(densities),
        'Distribution': [distribution] * len(densities),
        'Overlap': [overlap] * len(densities),
        'PBC': [True] * len(densities)
    })
    new_density_vals = model.predict(new_data)
    ax.plot(densities, new_density_vals, label=f"{num}, {overlap:.1f}, {cv:.2f}", color=color)

ax.set_ylabel('Set Density', fontsize=25)
ax.set_xlabel('Target Density', fontsize=25)
ax.set_title('Overlapping Foams Density Adjustment', fontsize=30)
ax.set_ylim([0, 1.25])
ax.set_xlim([0, 1])
ax.legend(title='n, overlap, cv', fontsize=12, title_fontsize=14)
ax.grid(True)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.tight_layout()
plt.show()
