# Write the benchmarking functions here.
# See "Writing benchmarks" in the asv docs for more information.

import os

from astropy.io import fits
from astropy.wcs import WCS

try:
    from astropy.visualization.wcsaxes import WCSAxes
except ImportError:
    pass

# Use the OO interface to really benchmark WCSAxes and not pyplot

from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

ROOT = os.path.abspath(os.path.dirname(__file__))

MSX_HEADER = fits.Header.fromtextfile(os.path.join(ROOT, 'msx_header'))
MSX_WCS = WCS(MSX_HEADER)


def time_basic_plot():

    fig = Figure()
    canvas = FigureCanvas(fig)

    ax = WCSAxes(fig, [0.15, 0.15, 0.7, 0.7], wcs=MSX_WCS)
    fig.add_axes(ax)

    ax.set_xlim(-0.5, 148.5)
    ax.set_ylim(-0.5, 148.5)

    canvas.draw()


def time_basic_plot_with_grid():

    fig = Figure()
    canvas = FigureCanvas(fig)

    ax = WCSAxes(fig, [0.15, 0.15, 0.7, 0.7], wcs=MSX_WCS)
    fig.add_axes(ax)

    ax.grid(color='red', alpha=0.5, linestyle='solid')

    ax.set_xlim(-0.5, 148.5)
    ax.set_ylim(-0.5, 148.5)

    canvas.draw()


def time_basic_plot_with_grid_and_overlay():

    fig = Figure()
    canvas = FigureCanvas(fig)

    ax = WCSAxes(fig, [0.15, 0.15, 0.7, 0.7], wcs=MSX_WCS)
    fig.add_axes(ax)

    ax.grid(color='red', alpha=0.5, linestyle='solid')

    ax.set_xlim(-0.5, 148.5)
    ax.set_ylim(-0.5, 148.5)

    overlay = ax.get_coords_overlay('fk5')
    overlay.grid(color='purple', ls='dotted')

    canvas.draw()
