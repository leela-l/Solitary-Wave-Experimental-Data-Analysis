import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import chi2
from matplotlib.ticker import AutoMinorLocator
from matplotlib.ticker import MultipleLocator


amp1 = np.array([0.0025,0.0030,0.0035,0.0040,0.0045,0.0050,0.0055,0.0060,0.0070,0.0075,
                0.0080,0.0085,0.0090,0.0095,0.0105,0.0110,0.0120,0.0125,0.0130,0.0140,
                0.0150,0.0165,0.0170,0.0175,0.0180,0.0185])

err_height1 = np.array([0.0007]*26)

av_speed1 = np.array([0.728,0.72,0.72,0.712,0.728,0.74,0.718,0.726,0.73,0.75,0.740,0.754,
                     0.760,0.762,0.79,0.760,0.785,0.750,0.775,0.794,0.790,0.800,0.807,0.780,
                     0.79,0.81])

err_speed1 = np.array([0.002,0.01,0.02,0.005,0.005,0.02,0.006,0.004,0.01,0.010,0.003,0.007,0.005,
                      0.006,0.02,0.007,0.008,0.005,0.007,0.009,0.009,0.009,0.008,0.006,0.02,0.01])

c_hyp1 = np.array([0.711, 0.71, 0.72, 0.721, 0.725, 0.73, 0.732, 0.736, 0.74, 0.75, 0.750, 0.753,
                  0.757, 0.760, 0.77, 0.771, 0.778, 0.782, 0.785, 0.792, 0.799, 0.810, 0.813,
                  0.817, 0.82 ,0.82])



amp2 = np.array([0.006, 0.0065, 0.007, 0.0075, 0.0085, 0.009, 0.0095, 0.01, 0.0105, 0.011, 0.0115, 0.012,
                0.0125, 0.013, 0.0135, 0.014, 0.0145, 0.015, 0.0155, 0.016, 0.0165, 0.017])

av_speed2 = np.array([0.67, 0.649, 0.650, 0.654, 0.68, 0.67, 0.67, 0.673, 0.69, 0.69, 0.707, 0.705, 0.73, 0.70,
                     0.721, 0.73, 0.74, 0.743, 0.74, 0.74, 0.727, 0.76])

err_speed2 = np.array([0.01, 0.009, 0.006, 0.004, 0.02, 0.01, 0.01, 0.008, 0.01, 0.01, 0.009, 0.007, 0.02,
                      0.01, 0.006, 0.02, 0.02, 0.006, 0.01, 0.01, 0.009, 0.01])

err_height2 = np.array([0.0007]*22)



def linear(x, m, c):
    return m*x + c



popt1, pcov1 = curve_fit(linear, amp1, av_speed1, sigma=err_speed1, absolute_sigma=True)
m1, c1 = popt1

residuals_norm1 = (av_speed1 - linear(amp1, m1, c1)) / err_speed1



popt2, pcov2 = curve_fit(linear, amp2, av_speed2, sigma=err_speed2, absolute_sigma=True)
m2, c2 = popt2

residuals_norm2 = (av_speed2 - linear(amp2, m2, c2)) / err_speed2



x_fit = np.linspace(min(amp1), max(amp1), 200)
y_fit1 = linear(x_fit, m1, c1)
y_fit2 = linear(x_fit, m2, c2)



fig, (ax1, ax2, ax3) = plt.subplots(
    3,1, figsize=(8,8), sharex=True,
    gridspec_kw={'height_ratios':[3,1,1]}
)

ax2.axhline(0, linestyle='--', color='grey')
ax3.axhline(0, linestyle='--', color='grey')



ax1.errorbar(amp1, av_speed1,
             yerr=err_speed1,
             xerr=err_height1,
             fmt='o',
             color='darkorange',
             ecolor='darkgreen',
             markersize=5,
             capsize=3,
             label='Dataset 1')

ax1.plot(x_fit, y_fit1,
         color='royalblue',
         linewidth=2)



ax1.errorbar(amp2, av_speed2,
             yerr=err_speed2,
             xerr=err_height2,
             fmt='o',
             color='lightseagreen',
             ecolor='palevioletred',
             markersize=5,
             capsize=3,
             label='Dataset 2')

ax1.plot(x_fit, y_fit2,
         color='purple',
         linewidth=2)


ax1.set_ylabel(r'$c$ (m s$^{-1}$)', fontsize=17)

ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)



ax2.scatter(amp1, residuals_norm1, color='royalblue')



ax2.set_ylabel('Normalised\nResiduals', fontsize=17)



ax3.scatter(amp2, residuals_norm2, color='purple')

ax3.set_xlabel(r'$\eta_0$ (m)', fontsize=17)
ax3.set_ylabel('Normalised\nResiduals', fontsize=17)

ax1.tick_params(axis='both', labelsize=14)
ax2.tick_params(axis='both', labelsize=14)

ax1.xaxis.set_minor_locator(MultipleLocator(0.00125))
ax1.yaxis.set_minor_locator(MultipleLocator(0.025))

ax1.tick_params(which='minor', length=3)


plt.tight_layout()
plt.show()