import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import chi2

# DATA
amp = np.array([0.0025,0.0030,0.0035,0.0040,0.0045,0.0050,0.0055,0.0060,0.0070,0.0075,
                0.0080,0.0085,0.0090,0.0095,0.0105,0.0110,0.0120,0.0125,0.0130,0.0140,
                0.0150,0.0165,0.0170,0.0175,0.0180,0.0185])

err_height = np.array([0.0005]*26)

av_speed = np.array([0.728,0.72,0.72,0.712,0.728,0.74,0.718,0.726,0.73,0.75,0.740,0.754,
                     0.760,0.762,0.79,0.760,0.785,0.750,0.775,0.794,0.790,0.800,0.807,0.780,
                     0.79,0.81])

err_speed = np.array([0.002,0.01,0.02,0.005,0.005,0.02,0.006,0.004,0.01,0.010,0.003,0.007,0.005,
                      0.006,0.02,0.007,0.008,0.005,0.007,0.009,0.009,0.009,0.008,0.006,0.02,0.01])

c_hyp = np.array([0.711, 0.71, 0.72, 0.721, 0.725, 0.73, 0.732, 0.736, 0.74, 0.75, 0.750, 0.753,
                  0.757, 0.760, 0.77, 0.771, 0.778, 0.782, 0.785, 0.792, 0.799, 0.810, 0.813,
                  0.817, 0.82 ,0.82])


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
x_fit = np.linspace(min(amp), max(amp)*1.05, 200)
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
             color='darkorange',
             ecolor='darkgreen')

ax1.plot(x_fit, y_fit, color= 'royalblue', label='Linear fit')

ax1.plot(x_fit, y_hyp_fit,
         linestyle='--',
         color='purple',
         label='Hypothetical')


ax1.set_ylabel(r'$c$ (m s$^{-1}$)', fontsize=14)

ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)


# RESIDUALS
ax2.scatter(amp, residuals_norm, color= 'purple')


ax2.set_xlabel(r'$\eta_0$ (m)', fontsize=14)
ax2.set_ylabel('Norm. Residuals')


ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)


plt.tight_layout()
plt.show()



