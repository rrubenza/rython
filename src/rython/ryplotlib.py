import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt


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


def autoscale_x(ax, margin=0.1):
    """
    Rescales the x-axis based on data visible in the current ylim.

    Usage:
        ax.set_ylim(2, 4)
        autoscale_x(ax)
    """
    lines = ax.get_lines()
    low, high = np.inf, -np.inf

    for line in lines:
        x_data = line.get_xdata()
        y_data = line.get_ydata()
        ylim = ax.get_ylim()

        # Find x-values within current y-limits
        mask = (y_data >= ylim[0]) & (y_data <= ylim[1])
        visible_x = x_data[mask]

        if len(visible_x) > 0:
            low = min(low, np.min(visible_x))
            high = max(high, np.max(visible_x))

    if low != np.inf:
        # Add a small margin
        delta = (high - low) * margin
        ax.set_xlim(low - delta, high + delta)


class PiecewiseNorm(mpl.colors.Normalize):
    def __init__(self, levels, cmap_positions=None):
        self.levels = np.asarray(levels, dtype=float)
        if cmap_positions is None:
            self.cmap_positions = np.linspace(0, 1, len(levels))
        else:
            self.cmap_positions = np.asarray(cmap_positions, dtype=float)
        super().__init__(vmin=levels[0], vmax=levels[-1])

    def __call__(self, value, clip=None):
        return np.ma.masked_array(np.interp(value, self.levels, self.cmap_positions))

    def inverse(self, value):
        return np.interp(value, self.cmap_positions, self.levels)


def visualize_color_mapping(bounds, cmap, norm):
    fig, axes = plt.subplots(2, 1, figsize=(8, 1.8), layout="constrained")

    norms = [
        mpl.colors.Normalize(vmin=bounds[0], vmax=bounds[-1]),
        norm,  # e.g. PiecewiseNorm
    ]
    labels = ["Linear", "PiecewiseNorm"]

    for ax, n, label in zip(axes, norms, labels):
        sm = mpl.cm.ScalarMappable(cmap=cmap, norm=n)
        sm.set_array([])
        cb = fig.colorbar(sm, cax=ax, orientation="horizontal")
        cb.set_ticks(bounds)
        cb.ax.set_title(label, loc="left", fontsize=10)

    for b in bounds[1:-1]:
        cb.ax.axvline(b, color="k", ls="-", lw=2)

    plt.show()
