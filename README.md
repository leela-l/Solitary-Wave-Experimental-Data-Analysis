# Solitary Wave Experimental Data Analysis

Python scripts for analysing experimental data on solitary waves, focusing on how wave speed and amplitude behave with and without an obstacle in the wave's path. A linear regression is fitted to the data, normalised residuals are computed to assess fit quality, and distributions of measured vs expected wave speed ratios are plotted.

## Script Descriptions
`Histogram.py`: Compares the ratio of measured to expected wave speed (`c_measured / c_expected`) for two setups (no block vs. 3 blocks), and returns the skewness of each distribution.
`1 block.py`: Fits linear regressions of amplitude "during" and "after" passing a single block, against the "before" amplitude. Includes error bars, normalised residual plots, and zoomed inset views of selected data points.
`1 block before.py`: Analyses amplitude data before the wave passes a single block.
`1 block during.py`: Analyses amplitude data while the wave passes a single block.
`1 block after.py`: Analyses amplitude data after the wave passes a single block.
`No block graph c vs h.py`: Plots wave speed (*c*) vs. wave height (*η*) with no block present, fitting a linear regression and normalised residuals.
`3 blocks graph c vs h.py`: Same analysis as above, but for the 3-block configuration.
`both c vs h.py`: Plots *c* vs. *η* for two datasets (e.g. different block configurations) on the same figure for comparison.

## Method

1. Experimental data arrays (amplitude, wave speed/height, and associated measurement uncertainties).
2. A linear model `y = mx + c` fitted to the data using `scipy.optimize.curve_fit`, weighted by measurement uncertainty (`sigma`, `absolute_sigma=True`).
3. Normalised residuals `(observed - fit) / uncertainty` computed to check how well the linear model describes the data.
4. `matplotlib` figures showing the raw data with error bars, the fitted line, and a residuals subplot beneath.

## Requirements

- Python 3.x
- NumPy
- SciPy
- Matplotlib

## Usage

Each script is standalone and can be run directly, e.g.:

```bash
python "1 block.py"
```

Running a script will open a Matplotlib window showing the corresponding plot. Filenames contain spaces, so quote them when running from the command line.
