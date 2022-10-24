from matplotlib import pyplot as plt
import numpy as np

def fill_interval(x, /, xmin=None, xmax=None, ax=None, **kwargs):
    """
    Fills a vertical slice of the viewport between the `xmin` and `xmax`
    values
    """
    x = np.asanyarray(x)
    ax = plt.gca() if ax is None else ax
    min_cond = True if xmin is None else x >= xmin
    max_cond = True if xmax is None else x <= xmax

    # y0 and y1 are relative to the x axis transform, meaning
    # the bottom and top of the viewport
    return ax.fill_between(x, 0, 1,
        where=(np.logical_and(min_cond, max_cond)),
        transform=ax.get_xaxis_transform(), **kwargs)