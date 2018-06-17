# Write the benchmarking functions here.
# See "Writing benchmarks" in the asv docs for more information.

import os

import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
from astropy.utils import NumpyRNGContext
from scipy.ndimage import gaussian_filter

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

TWOMASS_HEADER = fits.Header.fromtextfile(os.path.join(ROOT, '2mass_header'))
TWOMASS_WCS = WCS(TWOMASS_HEADER)

with NumpyRNGContext(12345):
    DATA = gaussian_filter(np.random.random((256, 256)), 3)


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


def time_contour_with_transform():

    fig = Figure()
    canvas = FigureCanvas(fig)

    ax = WCSAxes(fig, [0.15, 0.15, 0.7, 0.7], wcs=MSX_WCS)
    fig.add_axes(ax)

    ax.contour(DATA, transform=ax.get_transform(TWOMASS_WCS))

    # The limits are to make sure the contours are in the middle of the result
    ax.set_xlim(32.5, 150.5)
    ax.set_ylim(-64.5, 64.5)

    canvas.draw()


def time_contourf_with_transform():

    fig = Figure()
    canvas = FigureCanvas(fig)

    ax = WCSAxes(fig, [0.15, 0.15, 0.7, 0.7], wcs=MSX_WCS)
    fig.add_axes(ax)

    ax.contourf(DATA, transform=ax.get_transform(TWOMASS_WCS))

    # The limits are to make sure the contours are in the middle of the result
    ax.set_xlim(32.5, 150.5)
    ax.set_ylim(-64.5, 64.5)

    canvas.draw()
