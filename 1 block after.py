import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import chi2




amp_before = np.array([0.0065,0.0070,0.0075,0.0080,0.0085,0.0090,0.0095,0.0100,0.0105,0.0110,0.0115,
                       0.0120,0.0125,0.0130,0.0135,0.0140,0.0145,0.0165,0.0170])

err_amp_before = np.array([0.0005]*19)

amp_after = np.array([0.0065,0.0071,0.0073,0.0072,0.0085,0.0098,0.0109,0.0109,0.0097,0.0102,0.0114,
                      0.0127,0.0124,0.013, 0.0137,0.0142,0.0156,0.0179,0.0188])

err_amp_after = np.array([0.0004,0.0002,0.0001,0.0002,0.0007,0.0005,0.0003,0.0003,0.0004,0.0007,
                         0.0004,0.0006,0.0002,0.001,0.0006,0.0004,0.0003,0.0003,0.0003])


# LINEAR MODEL
def linear(x, m, c):
    return m*x + c


# FIT
popt, pcov = curve_fit(linear, amp_before, amp_after, sigma=err_amp_after, absolute_sigma=True)

m, c = popt

# PARAMETER UNCERTAINTIES
m_err = np.sqrt(pcov[0,0])
c_err = np.sqrt(pcov[1,1])


# BEST FIT LINE
x_fit = np.linspace(min(amp_before), max(amp_before)*1.05, 200)
y_fit = linear(x_fit, m, c)

popt_hyp, pcov_hyp = curve_fit(linear, amp_before, amp_before)

m_hyp, c_hyp_fit = popt_hyp

y_hyp_fit = linear(x_fit, m_hyp, c_hyp_fit)


# CHI SQUARED
chi_sq = np.sum(((amp_after - linear(amp_before, m, c)) / err_amp_after)**2)

# DEGREES OF FREEDOM
dof = len(amp_before) - 2

# REDUCED CHI SQUARED
red_chi_sq = chi_sq / dof

# P VALUE
p_value = 1 - chi2.cdf(chi_sq, dof)


# RESIDUALS
residuals = amp_after - linear(amp_before, m, c)
# Normalized residuals
residuals_norm = (amp_after - linear(amp_before, m, c)) / err_amp_after

print(residuals_norm)


# PRINT RESULTS
print("Gradient =", m, "+/-", m_err)
print("Intercept =", c, "+/-", c_err)
print("Chi squared =", chi_sq)
print("Reduced chi squared =", red_chi_sq)
print("p value =", p_value)


# PLOTTING
fig, (ax1, ax2) = plt.subplots(2,1, figsize=(8,8), sharex=True,
    gridspec_kw={'height_ratios':[3,1]})

ax2.axhline(0, linestyle='--', color='grey')

# DATA + FIT
ax1.errorbar(amp_before, amp_after,
             yerr=err_amp_after,
             xerr=err_amp_before,
             fmt='o', markersize=5, capsize=3,
             color='blue',
             ecolor='pink')

ax1.plot(x_fit, y_fit, color= 'green', label='Linear fit')


ax1.plot(x_fit, y_hyp_fit,
         linestyle='--',
         color='orange',
         label='Hypothetical')


ax1.set_ylabel(r'$\eta_{after}$ (m)', fontsize=17)

ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)


# RESIDUALS
ax2.scatter(amp_before, residuals_norm, color= 'green')


ax2.set_xlabel(r'$\eta_{before}$ (m)', fontsize=17)
ax2.set_ylabel('Normalised\nResiduals', fontsize=17)


ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

ax1.tick_params(axis='both', labelsize=14)
ax2.tick_params(axis='both', labelsize=14)




plt.tight_layout()
plt.show()