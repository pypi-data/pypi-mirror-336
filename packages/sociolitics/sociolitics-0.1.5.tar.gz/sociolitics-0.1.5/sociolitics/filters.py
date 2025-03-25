# Copyright © 2024 Dmitry Pronin.
from scipy.signal import savgol_filter


def ensemble_filter(data: list, n_filters=100,
                    polyorder=0, **savgol_args) -> list:
    """
    Smooth the timeseries by the ensemble filter which uses
    an averanging of the results of several Savitzky-Golay filters
    with different window sizes

    Parameters
    ----------
    data : array-like
        The timeseries to be filtered
    n_filters : int
        The number of Savitzky-Golay filters in the ensemble
    polyorder : int
        The order of the polynomial used to fit the samples.
        `polyorder` must be less than `window_length`.
    **savgol_args
        Hyperparameters of the Savitzky-Golay filter from scipy
    """
    filt = 0
    start = len(data)//10
    stop = len(data)//4
    step = (stop-start)//n_filters
    if step == 0:
        step = 1
        n_filters = (stop-start)//step
    for _ in range(start, stop, step):
        res = savgol_filter(data, _, polyorder, mode='mirror', **savgol_args)
        filt += res
    return filt/n_filters


def cascade_filter(data: list, n_iter: int, **savgol_args) -> list:
    """
    Smooth the timeseries by the cascade filter which uses a sequential
    Savitzky-Golay filters

    Parameters
    ----------
    data : array-like
        The timeseries to be filtered
    n_iter : int
        The length of the Savitzky-Golay filters sequence
    **savgol_args
        Hyperparameters of the Savitzky-Golay filter from scipy
    """
    for _ in range(n_iter):
        data = savgol_filter(data, mode='mirror', **savgol_args)
    return data
