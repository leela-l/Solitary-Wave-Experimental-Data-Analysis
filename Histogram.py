import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import skew
from matplotlib.ticker import AutoMinorLocator
from matplotlib.ticker import MultipleLocator

ratio_no_block = np.array([0.976,0.99,1.00,1.014,0.996,0.99,1.020,1.013,1.02,1.00,1.013,0.999,0.996,
                           0.998,0.97,1.014,0.992,1.042,1.013,0.998,1.011,1.012,1.008,1.047,1.04,1.02])


ratio_3_block = np.array([0.87, 0.914, 0.920, 0.921, 0.90, 0.92, 0.93, 0.929, 0.91, 0.92, 0.904, 0.913,
                          0.89, 0.93, 0.912, 0.91, 0.90, 0.903, 0.91, 0.92, 0.942, 0.90])





skew_no_block = skew(ratio_no_block)
skew_3_block = skew(ratio_3_block)

print(skew_no_block)
print(skew_3_block)


plt.figure(figsize=(7,5))

plt.hist(ratio_no_block, bins=8,
         color='royalblue',
         alpha=0.6, edgecolor='black',
         label='Dataset 1')

plt.hist(ratio_3_block, bins=8,
         color='purple', edgecolor='black',
         alpha=0.6,
         label='Dataset 2')

plt.axvline(1, linestyle='--', color='grey', label='Expected value')

plt.xlabel(r'$\frac{c_{measured}}{c_{expected}}$', fontsize=17)
plt.ylabel('Frequency', fontsize=17)

plt.tick_params(axis='both', labelsize=14)
plt.tick_params(axis='both', labelsize=14)



plt.tick_params(which='minor', length=3)

plt.tight_layout()
plt.show()