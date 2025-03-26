
# Power Spectral Density and Smoothing Analysis

This package provides tools for analyzing time-series data using spectral methods such as Fourier and wavelet transforms. It includes functionality for smoothing data, estimating the power spectral density (PSD) for 3D signals, and handling edge effects like the Cone of Influence (CoI) in wavelet analysis.

## Features

- **Data Smoothing**:
  - `smooth`: A wrapper function for logarithmic smoothing of data based on FFT frequency distributions.
  - `smoothing_function`: Core function for performing logarithmic window smoothing, optimized with `numba`.

- **Power Spectral Density Estimation**:
  - `TracePSD`: Computes the PSD using the Fourier transform for 3D signals.
  - `trace_PSD_wavelet`: Estimates the PSD using the Continuous Wavelet Transform (CWT), with optional consideration of the Cone of Influence (CoI).

## Installation

Clone this repository and install the dependencies using `pip`:

```bash
git clone https://github.com/your-repo/SWTurbPy.git
cd SWTurbPy
pip install .
```

## Dependencies

- `numpy`: For numerical operations and FFT computations.
- `pycwt`: For wavelet analysis.
- `numba`: For optimizing computationally intensive functions.

## Usage

### 1. Logarithmic Data Smoothing

```python
import numpy as np
from SWTurbPy import smooth

# Example data
x = np.fft.rfftfreq(1000, d=0.01)
y = np.random.random(len(x))

# Apply smoothing
xoutmean, yout = smooth(x, y, pad=10)
```

### 2. PSD Estimation with FFT

```python
from SWTurbPy import TracePSD

# Example data
x = np.sin(np.linspace(0, 10, 1000))
y = np.cos(np.linspace(0, 10, 1000))
z = np.sin(np.linspace(0, 10, 1000)) * 0.5

dt = 0.01  # Sampling time
freqs, B_pow = TracePSD(x, y, z, dt, norm='forward')
```

### 3. PSD Estimation with Wavelet Transform

```python
from SWTurbPy import trace_PSD_wavelet

# Example data
x = np.sin(np.linspace(0, 10, 1000))
y = np.cos(np.linspace(0, 10, 1000))
z = np.sin(np.linspace(0, 10, 1000)) * 0.5

dt = 0.01  # Sampling time
dj = 0.1   # Scale resolution

db_x, db_y, db_z, freqs, PSD, scales, coi = trace_PSD_wavelet(x, y, z, dt, dj, consider_coi=True)
```

## Function Descriptions

### `smooth(x, y, pad, window=2)`

**Description**: Smooths data using logarithmically spaced intervals. Useful for data with logarithmic frequency distributions.

**Parameters**:
- `x` (numpy.ndarray): Input x-values (e.g., FFT frequencies).
- `y` (numpy.ndarray): Input y-values to smooth.
- `pad` (int): Controls the density of smoothing intervals.
- `window` (int, optional): Size of the smoothing window in logarithmic space.

**Returns**:
- `xoutmean` (numpy.ndarray): Smoothed x-values.
- `yout` (numpy.ndarray): Smoothed y-values.

---

### `TracePSD(x, y, z, dt, norm=None)`

**Description**: Estimates the PSD for 3D signals using the Fourier transform.

**Parameters**:
- `x, y, z` (numpy.ndarray): Time series components of the signal.
- `dt` (float): Sampling time.
- `norm` (str, optional): FFT normalization mode (`"forward"`, `"ortho"`, or `"backward"`).

**Returns**:
- `freqs` (numpy.ndarray): Frequencies of the PSD.
- `B_pow` (numpy.ndarray): Power spectral density.

---

### `trace_PSD_wavelet(x, y, z, dt, dj, consider_coi=True)`

**Description**: Estimates the PSD using wavelet analysis for 3D signals, with optional handling of edge effects via the Cone of Influence (CoI).

**Parameters**:
- `x, y, z` (array-like): Components of the signal.
- `dt` (float): Sampling time.
- `dj` (float): Scale resolution.
- `consider_coi` (bool, optional): Whether to consider CoI in PSD estimation.

**Returns**:
- `db_x, db_y, db_z` (array-like): Wavelet coefficients for each component.
- `freqs` (array-like): Frequencies of the PSD.
- `PSD` (array-like): Power spectral density.
- `scales` (array-like): Wavelet scales.
- `coi` (array-like): Cone of Influence.

## Example Visualization

Visualize the results using `matplotlib`:

```python
import matplotlib.pyplot as plt

# Plot FFT-based PSD
plt.loglog(freqs, B_pow)
plt.title('Power Spectral Density (FFT)')
plt.xlabel('Frequency')
plt.ylabel('PSD')
plt.grid()
plt.show()

# Plot Wavelet-based PSD
plt.loglog(freqs, PSD)
plt.title('Power Spectral Density (Wavelet)')
plt.xlabel('Frequency')
plt.ylabel('PSD')
plt.grid()
plt.show()
```

## Contribution

Contributions are welcome! Please submit issues or pull requests to improve the code or documentation.

## License

This project is licensed under the [MIT License](LICENSE).
