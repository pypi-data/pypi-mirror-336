import numpy as np
import pycwt as wavelet
from numba import prange, jit

def smooth(x, y, pad, window=2):
    """
    Smooths data using logarithmic spacing of indices.

    This function creates a set of logarithmically spaced indices based on the length of `x` and the `pad` parameter. 
    It then smooths the `y` values using a specified window size by calling the `smoothing_function`.

    Parameters:
    ----------
    x : numpy.ndarray
        An array of x-values, typically representing frequencies (e.g., output from `numpy.fft.rfftfreq`).
    y : numpy.ndarray
        An array of y-values corresponding to `x`, typically representing a signal or spectrum.
    pad : int
        A parameter to control the density of smoothing intervals. 
        Higher values result in fewer intervals by increasing the spacing between indices.
    window : int, optional, default=2
        The size of the window used for smoothing. The window size is applied in logarithmic space.

    Returns:
    -------
    xoutmean : numpy.ndarray
        Array of mean x-values for each smoothing interval.
    yout : numpy.ndarray
        Array of smoothed y-values for each interval.

    Notes:
    -----
    - This function is particularly useful for processing data with frequencies that are logarithmically spaced.
    - The `smoothing_function` assumes that `x` values are monotonically increasing.
    """


    # Generate logarithmically spaced indices
    loop = np.logspace(0, np.log10(len(x)), int(len(x)/pad))
    loop = np.array(loop, dtype=np.int64)
    loop = np.unique(loop)

    # Call the smoothing function
    xoutmean, yout = smoothing_function(x, y, loop, window)

    return xoutmean, yout

@jit(nopython=True, parallel=True)
def smoothing_function(x, y, loop, window):
    """
    Computes smoothed averages of `x` and `y` over logarithmic intervals.

    This function calculates the mean values of `x` and `y` within intervals defined 
    by the indices in `loop`. The size of each interval is controlled by the `window` parameter.

    Parameters:
    ----------
    x : numpy.ndarray
        An array of x-values, typically representing frequencies (e.g., output from `numpy.fft.rfftfreq`).
    y : numpy.ndarray
        An array of y-values corresponding to `x`, typically representing a signal or spectrum.
    loop : numpy.ndarray
        Array of indices specifying the start of each smoothing interval. 
        These indices are logarithmically spaced.
    window : int
        The size of the window used to define the end of each smoothing interval.

    Returns:
    -------
    xoutmean : numpy.ndarray
        Array of mean x-values for each smoothing window.
    yout : numpy.ndarray
        Array of smoothed y-values for each interval.

    Notes:
    -----
    - The smoothing process is parallelized for performance using `numba`.
    - The function assumes that `x` values are monotonically increasing and logarithmically spaced.
    """


    len_x = len(x)  # Total length of the x array

    # Initialize output arrays with NaN values
    xoutmean = np.full(len(loop), np.nan)
    yout = np.full(len(loop), np.nan)

    # Iterate over the loop indices in parallel
    for i1 in prange(len(loop)):
        
        i = int(loop[i1])  # Current index
        e = int(i * window)  # End index

        if e < len_x:
            # Compute the mean x and y values for the interval
            if i == e:
                xoutmean[i1] = x[i]
                yout[i1] = y[i]
            else:
                xoutmean[i1] = np.nanmean(x[i:e])
                yout[i1] = np.nanmean(y[i:e])


    return xoutmean, yout



def TracePSD(x, y, z, dt, norm=None):
    """
    Estimates the power spectral density (PSD) for a 3D timeseries.

    This function computes the PSD for a 3D signal given its components `x`, `y`, and `z`. 
    The PSD is calculated using the Fourier transform of each component, and the results are summed to give the total power.

    Parameters:
    ----------
    x : numpy.ndarray
        Time series data for the x-component of the signal.
    y : numpy.ndarray
        Time series data for the y-component of the signal.
    z : numpy.ndarray
        Time series data for the z-component of the signal.
    dt : float
        Time step between consecutive samples, equivalent to the reciprocal of the sampling frequency.
    norm : {“backward”, “ortho”, “forward”}, optional, default=None
        Normalization mode for the Fourier transform:
        - "forward": Keeps the transformed spectrum comparable across different sampling frequencies.
        - "ortho": Conserves energy between the time domain and frequency domain.
        - "backward": The default mode.

    Returns:
    -------
    freqs : numpy.ndarray
        Frequencies corresponding to the PSD values.
    B_pow : numpy.ndarray
        Power spectral density for the 3D signal, normalized by the length of the time series and sampling frequency.

    Notes:
    -----
    - The method uses the real-valued fast Fourier transform (`numpy.fft.rfft`) for efficiency.
    - The normalization ensures consistency across different signal lengths and sampling frequencies.
    - The coefficient `len(x)/(2*dt)` is used to properly scale the PSD.

    References:
    ----------
    For normalization modes, see the documentation for `numpy.fft.rfft`:
    https://docs.scipy.org/doc/scipy/reference/generated/scipy.fft.rfft.html
    """

    
    B_pow = np.abs(np.fft.rfft(x, norm=norm))**2 \
          + np.abs(np.fft.rfft(y, norm=norm))**2 \
          + np.abs(np.fft.rfft(z, norm=norm))**2

    freqs = np.fft.rfftfreq(len(x), dt)

    coeff = len(x)/(2*dt)
    
    return freqs, B_pow/coeff


def trace_PSD_wavelet(x, y, z, dt, dj, consider_coi=True):
    """
    Calculate the power spectral density (PSD) using wavelet transform.

    Parameters
    ----------
    x, y, z : array-like
        Components of the field to transform.
    dt : float
        Sampling time of the time series.
    dj : float
        Scale resolution; smaller values increase the number of scales.
    consider_coi : bool, optional (default=True)
        Whether to consider the Cone of Influence (CoI) in PSD estimation.

    Returns
    -------
    db_x, db_y, db_z : array-like
        Wavelet coefficients for the x, y, z components.
    freqs : array-like
        Frequencies corresponding to the PSD points.
    PSD : array-like
        Power spectral density of the signal.
    scales : array-like
        Wavelet scales used for the transform.
    coi : array-like
        Cone of Influence (CoI) indicating regions affected by edge effects.
    """
    mother = wavelet.Morlet()

    db_x, scales, freqs, coi, _, _ = wavelet.cwt(x, dt, dj, wavelet=mother)
    db_y, _, _, _, _, _ = wavelet.cwt(y, dt, dj, wavelet=mother)
    db_z, _, _, _, _, _ = wavelet.cwt(z, dt, dj, wavelet=mother)

    if consider_coi:
        PSD = np.zeros_like(freqs)
        for i, scale in enumerate(scales):
            valid = coi > scale

            if np.any(valid):
                PSD[i] = (
                    np.nanmean(np.abs(db_x[i, valid]) ** 2) +
                    np.nanmean(np.abs(db_y[i, valid]) ** 2) +
                    np.nanmean(np.abs(db_z[i, valid]) ** 2)
                ) * (2 * dt)
            else:
                PSD[i] = np.nan
    else:
        PSD = (
            np.nanmean(np.abs(db_x) ** 2, axis=1) +
            np.nanmean(np.abs(db_y) ** 2, axis=1) +
            np.nanmean(np.abs(db_z) ** 2, axis=1)
        ) * (2 * dt)

    return db_x, db_y, db_z, freqs, PSD, scales, coi