import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import chi2
from mpl_toolkits.axes_grid1.inset_locator import inset_axes, mark_inset
from matplotlib.ticker import AutoMinorLocator
from matplotlib.ticker import MultipleLocator



amp_before = np.array([0.0065,0.0070,0.0075,0.0080,0.0085,0.0090,0.0095,0.0100,0.0105,0.0110,0.0115,
                       0.0120,0.0125,0.0130,0.0135,0.0140,0.0145,0.0165,0.0170])

err_amp_before = np.array([0.0007]*19)

amp_during = np.array([0.0368,0.0376,0.0376,0.0377,0.0383,0.0390,0.0396,0.0396,0.0398,0.0402,0.0415,
                       0.0428,0.0418,0.0423,0.0427,0.0433,0.0438,0.0456,0.0464])

err_amp_during = np.array([0.0007, 0.0001, 0.0001, 0.0001, 0.0009, 0.0003, 0.0001, 0.0003, 0.0003, 0.0002,
                           0.0002, 0.0005, 0.0001, 0.0003, 0.0005, 0.0003, 0.0006, 0.0002, 0.0002])

amp_after = np.array([0.0065,0.0071,0.0073,0.0072,0.0085,0.0098,0.0109,0.0109,0.0097,0.0102,0.0114,
                      0.0127,0.0124,0.013, 0.0137,0.0142,0.0156,0.0179,0.0188])

err_amp_after = np.array([0.0004,0.0002,0.0001,0.0002,0.0007,0.0005,0.0003,0.0003,0.0004,0.0007,
                         0.0004,0.0006,0.0002,0.001,0.0006,0.0004,0.0003,0.0003,0.0003])



def linear(x, m, c):
    return m*x + c



popt1, pcov1 = curve_fit(linear, amp_before, amp_during, sigma=err_amp_during, absolute_sigma=True)
m1, c1 = popt1

# Normalized residuals
residuals_norm1 = (amp_during - linear(amp_before, m1, c1)) / err_amp_during




popt2, pcov2 = curve_fit(linear, amp_before, amp_after, sigma=err_amp_after, absolute_sigma=True)
m2, c2 = popt2

# Normalized residuals
residuals_norm2 = (amp_after - linear(amp_before, m2, c2)) / err_amp_after


x_fit = np.linspace(min(amp_before), max(amp_before)*1.05, 200)
y_fit1 = linear(x_fit, m1, c1)
y_fit2 = linear(x_fit, m2, c2)



fig, (ax1, ax2, ax3) = plt.subplots(
    3,1, figsize=(8,8), sharex=True,
    gridspec_kw={'height_ratios':[3,1,1]}
)

ax2.axhline(0, linestyle='--', color='grey')
ax3.axhline(0, linestyle='--', color='grey')



ax1.errorbar(amp_before, amp_during,
             yerr=err_amp_during,
             xerr=err_amp_before,
             fmt='o', markersize=5, capsize=3,
             color='black',
             ecolor='orange',)

ax1.errorbar(amp_before, amp_after,
             yerr=err_amp_after,
             xerr=err_amp_before,
             fmt='o', markersize=5, capsize=3,
             color='pink',
             ecolor='darkgoldenrod')

ax1.plot(x_fit, y_fit1,
         color='red',
         linewidth=2)


ax1.plot(x_fit, y_fit2,
         color='green',
         linewidth=2)


ax1.set_ylabel(r'$\eta_{after}$ (m)', fontsize=17)

ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

# -------------------------
# GREEN inset: 2 middle-centre-left amp_after (blue) points, indices 7-8
# Box sits in the lower-left portion of the gap between the two lines
# -------------------------
ig = slice(7, 9)  # x ~ 0.0100-0.0105
xg = amp_before[ig]
yg = amp_after[ig]

axins_green = ax1.inset_axes([0.05, 0.28, 0.26, 0.26])

axins_green.errorbar(xg, yg,
                     xerr=err_amp_before[ig],
                     yerr=err_amp_after[ig],
                     fmt='o', color='pink', ecolor='darkgoldenrod', capsize=2)

axins_green.plot(x_fit, y_fit2, color='green', linewidth=1)

pad_x = 0.0003
pad_y = 0.0010

axins_green.set_xlim(min(xg)-pad_x, max(xg)+pad_x)
axins_green.set_ylim(min(yg)-pad_y, max(yg)+pad_y)

axins_green.set_box_aspect(1)
axins_green.tick_params(labelsize=7)

mark_inset(ax1, axins_green, loc1=1, loc2=2, fc="none", ec="black", lw=0.8)


# -------------------------
# RED inset: 2 middle-right amp_during (purple) points, indices 13-14
# Box sits in the lower-right portion of the gap between the two lines
# -------------------------
ir = slice(13, 15)  # x ~ 0.0130-0.0135
xr = amp_before[ir]
yr = amp_during[ir]

axins_red = ax1.inset_axes([0.62, 0.44, 0.26, 0.26])

axins_red.errorbar(xr, yr,
                   xerr=err_amp_before[ir],
                   yerr=err_amp_during[ir],
                   fmt='o', color='black', ecolor='orange', capsize=2)

axins_red.plot(x_fit, y_fit1, color='red', linewidth=1)

axins_red.set_xlim(min(xr)-pad_x, max(xr)+pad_x)
axins_red.set_ylim(min(yr)-pad_y, max(yr)+pad_y)

axins_red.set_box_aspect(1)
axins_red.tick_params(labelsize=7)

mark_inset(ax1, axins_red, loc1=3, loc2=4, fc="none", ec="black", lw=0.8)

# Residuals
ax2.scatter(amp_before, residuals_norm1, color='red')
ax2.set_ylabel('Normalised\nResiduals', fontsize=17)

ax3.scatter(amp_before, residuals_norm2, color='green')
ax3.set_xlabel(r'$\eta_{before}$ (m)', fontsize=17)
ax3.set_ylabel('Normalised\nResiduals', fontsize=17)

ax1.tick_params(axis='both', labelsize=14)
ax2.tick_params(axis='both', labelsize=14)
ax3.tick_params(axis='both', labelsize=14)


ax1.xaxis.set_minor_locator(MultipleLocator(0.001))

plt.tight_layout()
plt.show()