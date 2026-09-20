import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import chi2

# DATA
amp = np.array([0.006, 0.0065, 0.007, 0.0075, 0.0085, 0.009, 0.0095, 0.01, 0.0105, 0.011, 0.0115, 0.012,
                0.0125, 0.013, 0.0135, 0.014, 0.0145, 0.015, 0.0155, 0.016, 0.0165, 0.017])

err_height = np.array([0.0005]*22)

av_speed = np.array([0.67, 0.649, 0.650, 0.654, 0.68, 0.67, 0.67, 0.673, 0.69, 0.69, 0.707, 0.705, 0.73, 0.70,
                     0.721, 0.73, 0.74, 0.743, 0.74, 0.74, 0.727, 0.76])

err_speed = np.array([0.01, 0.009, 0.006, 0.004, 0.02, 0.01, 0.01, 0.008, 0.01, 0.01, 0.009, 0.007, 0.02,
                      0.01, 0.006, 0.02, 0.02, 0.006, 0.01, 0.01, 0.009, 0.01])

c_hyp = np.array([0.59, 0.593, 0.598, 0.602, 0.61, 0.62, 0.62, 0.625, 0.63, 0.63, 0.639, 0.644, 0.65, 0.65,
                  0.658, 0.66, 0.67, 0.671, 0.68, 0.68, 0.685, 0.69])


# LINEAR MODEL
def linear(x, m, c):
    return m*x + c


# FIT
popt, pcov = curve_fit(linear, amp, av_speed, sigma=err_speed, absolute_sigma=True)

m, c = popt

# PARAMETER UNCERTAINTIES
m_err = np.sqrt(pcov[0,0])
c_err = np.sqrt(pcov[1,1])


# BEST FIT LINE
x_fit = np.linspace(min(amp), max(amp), 200)
y_fit = linear(x_fit, m, c)

popt_hyp, pcov_hyp = curve_fit(linear, amp, c_hyp)

m_hyp, c_hyp_fit = popt_hyp

y_hyp_fit = linear(x_fit, m_hyp, c_hyp_fit)


# CHI SQUARED
chi_sq = np.sum(((av_speed - linear(amp, m, c)) / err_speed)**2)

# DEGREES OF FREEDOM
dof = len(amp) - 2

# REDUCED CHI SQUARED
red_chi_sq = chi_sq / dof

# P VALUE
p_value = 1 - chi2.cdf(chi_sq, dof)


# RESIDUALS
residuals = av_speed - linear(amp, m, c)
# Normalized residuals
residuals_norm = (av_speed - linear(amp, m, c)) / err_speed

print(residuals_norm)
print(np.mean(residuals_norm))


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
ax1.errorbar(amp, av_speed,
             yerr=err_speed,
             xerr=err_height,
             fmt='o', markersize=5, capsize=3,
             color='lightseagreen',  # points
             ecolor='palevioletred')

ax1.plot(x_fit, y_fit, color= 'purple', label='Linear fit')

ax1.plot(x_fit, y_hyp_fit,
         linestyle='--',
         color='purple',
         label='Hypothetical')

ax1.set_ylabel(r'$c$ (m s$^{-1}$)', fontsize=14)

ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)


# RESIDUALS
ax2.scatter(amp, residuals_norm, color= 'green')


ax2.set_xlabel(r'$\eta_0$ (m)', fontsize=14)
ax2.set_ylabel('Norm. Residuals')


ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)


plt.tight_layout()
plt.show()
