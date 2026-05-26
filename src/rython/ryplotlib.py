import numpy as np
import matplotlib as mpl


def get_base_rc_params(c0, tickcolor):
    return {
        "axes.edgecolor": c0,
        "axes.labelcolor": c0,
        "axes.titlecolor": c0,
        "font.size": 16.0,
        "font.stretch": "normal",
        "font.style": "normal",
        "font.variant": "normal",
        "font.weight": "medium",  #'normal',
        "figure.edgecolor": c0,
        "grid.alpha": 0.5,
        "grid.linestyle": "-",
        "grid.linewidth": 1,
        "xtick.color": tickcolor,
        "xtick.labelcolor": c0,
        "ytick.color": tickcolor,
        "ytick.labelcolor": c0,
        "legend.edgecolor": "none",
        "legend.facecolor": "none",
        "legend.framealpha": 0.8,
        "legend.frameon": True,
        "legend.labelcolor": c0,
    }


def set_darkmode(c0="w", tickcolor="darkgrey"):

    rcDarkMode = get_base_rc_params(c0, tickcolor)
    rcDarkMode |= {
        "axes.facecolor": "232323",
        "figure.facecolor": "k",
        "grid.color": "darkgrey",
    }

    for p in rcDarkMode:
        mpl.rcParams[p] = rcDarkMode[p]


def set_lightmode(c0="k", tickcolor="grey"):
    rcLightMode = get_base_rc_params(c0, tickcolor)
    rcLightMode |= {
        "axes.facecolor": "w",
        "figure.facecolor": "w",
        "grid.color": "lightgrey",
    }

    for p in rcLightMode:
        mpl.rcParams[p] = rcLightMode[p]


def dateformat(ax, which="x"):
    """
    Sets the date format for the specified axis to a concise format.

    Plot should be created with datetime objects on the specified axis.

    Usage:
        dateformat(ax, which="x")  # For x-axis
        dateformat(ax, which="y")  # For y-axis
    """
    locator = mpl.dates.AutoDateLocator()
    formatter = mpl.dates.ConciseDateFormatter(locator)
    if which == "x":
        ax.xaxis.set_major_locator(locator)
        ax.xaxis.set_major_formatter(formatter)
    elif which == "y":
        ax.yaxis.set_major_locator(locator)
        ax.yaxis.set_major_formatter(formatter)
    else:
        print(f"{which} not a recognized axis")


def autoscale_y(ax, margin=0.1):
    """
    Rescales the y-axis based on data visible in the current xlim.

    Usage:
        ax.set_xlim(2, 4)
        autoscale_y(ax)
    """
    lines = ax.get_lines()
    low, high = np.inf, -np.inf

    for line in lines:
        x_data = line.get_xdata()
        y_data = line.get_ydata()
        xlim = ax.get_xlim()

        # Find y-values within current x-limits
        mask = (x_data >= xlim[0]) & (x_data <= xlim[1])
        visible_y = y_data[mask]

        if len(visible_y) > 0:
            low = min(low, np.min(visible_y))
            high = max(high, np.max(visible_y))

    if low != np.inf:
        # Add a small margin
        delta = (high - low) * margin
        ax.set_ylim(low - delta, high + delta)
