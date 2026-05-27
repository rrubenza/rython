import numpy as np


def timebin(time, meas, meas_err, binsize):
    """Bin in equal sized time bins

    This routine bins a set of times, measurements, and measurement errors
    into time bins.  All inputs and outputs should be floats or double.
    binsize should have the same units as the time array.
    (from Andrew Howard, ported to Python by BJ Fulton)

    Args:
        time (array): array of times
        meas (array): array of measurements to be combined
        meas_err (array): array of measurement uncertainties
        binsize (float): width of bins in same units as time array

    Returns:
        tuple: (bin centers, binned measurements, binned uncertainties)
    """

    ind_order = np.argsort(time)
    time = time[ind_order]
    meas = meas[ind_order]
    meas_err = meas_err[ind_order]

    ct = 0
    while ct < len(time):
        ind = np.where((time >= time[ct]) & (time < time[ct] + binsize))[0]
        num = len(ind)
        wt = (1.0 / meas_err[ind]) ** 2.0  # weights based in errors
        wt = wt / np.sum(wt)  # normalized weights
        if ct == 0:
            time_out = [np.sum(wt * time[ind])]
            meas_out = [np.sum(wt * meas[ind])]
            meas_err_out = [1.0 / np.sqrt(np.sum(1.0 / (meas_err[ind]) ** 2))]
        else:
            time_out.append(np.sum(wt * time[ind]))
            meas_out.append(np.sum(wt * meas[ind]))
            meas_err_out.append(1.0 / np.sqrt(np.sum(1.0 / (meas_err[ind]) ** 2)))
        ct += num

    return time_out, meas_out, meas_err_out
