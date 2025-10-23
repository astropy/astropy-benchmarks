# Test the parallel_fit_dask function in synchronous mode

import numpy as np

from astropy.modeling.models import Gaussian1D, Const1D
from astropy.modeling.fitting import TRFLSQFitter, parallel_fit_dask

x = np.linspace(0, 100, 20)

y = 5 * np.exp(-((x - 30) ** 2) / (2 * 10**2)) + np.random.normal(0, 1, 20)
y = y.reshape((20, 1, 1))
y = np.broadcast_to(y, (20, 30, 10))

y_plus_y0 = y + 3

g = Gaussian1D(1, 20, 1)
g_plus_const = g + Const1D(0)

fitter = TRFLSQFitter()


def time_parallel_gaussian_fit():
    parallel_fit_dask(
        model=g,
        fitter=fitter,
        data=y,
        fitting_axes=0,
        world=(x,),
        scheduler="synchronous",
    )


def time_parallel_compound_fit():
    parallel_fit_dask(
        model=g_plus_const,
        fitter=fitter,
        data=y,
        fitting_axes=0,
        world=(x,),
        scheduler="synchronous",
    )
