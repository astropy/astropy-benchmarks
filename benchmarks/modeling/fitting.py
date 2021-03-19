import numpy as np

from astropy.modeling import models, fitting


Gaussian1D = models.Gaussian1D(amplitude=1, mean=0, stddev=1)
Gaussian2D = models.Gaussian2D(amplitude=1, x_mean=0,  y_mean=0, \
        x_stddev=1, y_stddev=1)

x = np.linspace(-5., 5., 200)
y_base = 3 * np.exp(-0.5 * (x - 1.3)**2 / 0.8**2)

x_grid, y_grid = np.meshgrid(x, x)
z_base = 3 * np.exp(-0.5* ((x_grid - 1.3)**2/0.8**2 + (y_grid - 2.1)**2/0.1**2))


fit_LevMarLSQFitter = fitting.LevMarLSQFitter()
fit_SLSQPLSQFitter = fitting.SLSQPLSQFitter()
fit_SimplexLSQFitter = fitting.SimplexLSQFitter()


def time_init_LevMarLSQFitter():
    fit = fitting.LevMarLSQFitter()


def time_init_SLSQPLSQFitter():
    fit = fitting.SLSQPLSQFitter()


def time_init_SimplexLSQFitter():
    fit = fitting.SimplexLSQFitter()


def time_init_LinearLSQFitter():
    fit = fitting.LinearLSQFitter()


def time_Gaussian1D_LevMarLSQFitter():
    y = y_base + np.random.normal(0., 0.2, y_base.shape)
    t = fit_LevMarLSQFitter(Gaussian1D, x, y)


# def time_Gaussian1D_SLSQPLSQFitter():
#     y = y_base + np.random.normal(0., 0.2, y_base.shape)
#     t = fit_SLSQPLSQFitter(Gaussian1D, x, y)


# def time_Gaussian1D_SimplexLSQFitter():
#     y = y_base + np.random.normal(0., 0.2, y_base.shape)
#     t = fit_SimplexLSQFitter(Gaussian1D, x, y)


def time_Gaussian2D_LevMarLSQFitter():
    z = z_base + np.random.normal(0., 0.2, z_base.shape)
    t = fit_LevMarLSQFitter(Gaussian2D, x_grid, y_grid, z)


# def time_Gaussian2D_SLSQPLSQFitter():
#     z = z_base + np.random.normal(0., 0.2, z_base.shape)
#     t = fit_SLSQPLSQFitter(Gaussian2D, x_grid, y_grid, z)


# def time_Gaussian2D_SimplexLSQFitter():
#     z = z_base + np.random.normal(0., 0.2, z_base.shape)
#     t = fit_SimplexLSQFitter(Gaussian2D, x_grid, y_grid, z)

