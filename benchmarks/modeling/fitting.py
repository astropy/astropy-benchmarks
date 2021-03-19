import numpy as np
import warnings

from astropy.modeling import models, fitting


Gaussian1D = models.Gaussian1D(amplitude=1, mean=0, stddev=1)
Gaussian2D = models.Gaussian2D(amplitude=1, x_mean=0,  y_mean=0, \
        x_stddev=1, y_stddev=1)

Polynomial1D = models.Polynomial1D(degree=2)
Polynomial2D = models.Polynomial2D(degree=2)

Chebyshev1D = models.Chebyshev1D(degree=2)
Chebyshev2D = models.Chebyshev2D(x_degree=2, y_degree=2)

combined_gauss_1d = models.Gaussian1D(1, 0, 0.1) + models.Gaussian1D(2, 0.5, 0.1)
combined_gauss_2d = models.Gaussian2D(amplitude=1, x_mean=0,  y_mean=0, x_stddev=0.1, y_stddev=0.1) + \
        models.Gaussian2D(amplitude=2, x_mean=0.5,  y_mean=0.5, x_stddev=0.1, y_stddev=0.1)

x = np.linspace(-5., 5., 200)
y_base = 3 * np.exp(-0.5 * (x - 1.3)**2 / 0.8**2)

x_grid, y_grid = np.meshgrid(x, x)
z_base = 3 * np.exp(-0.5* ((x_grid - 1.3)**2/0.8**2 + (y_grid - 2.1)**2/0.1**2))

fit_LevMarLSQFitter = fitting.LevMarLSQFitter()
fit_SLSQPLSQFitter = fitting.SLSQPLSQFitter()
fit_SimplexLSQFitter = fitting.SimplexLSQFitter()
fit_LinearLSQFitter = fitting.LinearLSQFitter()


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


def time_Gaussian1D_SLSQPLSQFitter():
    warnings.filterwarnings('error')
    try:
        y = y_base + np.random.normal(0., 0.2, y_base.shape)
        t = fit_SLSQPLSQFitter(Gaussian1D, x, y)
    except Warning:
        pass


def time_Gaussian1D_SimplexLSQFitter():
    warnings.filterwarnings('error')
    try:
        y = y_base + np.random.normal(0., 0.2, y_base.shape)
        t = fit_SimplexLSQFitter(Gaussian1D, x, y)
    except Warning:
        pass

def time_Gaussian2D_LevMarLSQFitter():
    warnings.filterwarnings('error')
    try:
        z = z_base + np.random.normal(0., 0.2, z_base.shape)
        t = fit_LevMarLSQFitter(Gaussian2D, x_grid, y_grid, z)
    except Warning:
        pass


def time_Gaussian2D_SLSQPLSQFitter():
    warnings.filterwarnings('error')
    try:
        z = z_base + np.random.normal(0., 0.2, z_base.shape)
        t = fit_SLSQPLSQFitter(Gaussian2D, x_grid, y_grid, z)
    except Warning:
        pass


def time_Gaussian2D_SimplexLSQFitter():
    warnings.filterwarnings('error')
    try:
        z = z_base + np.random.normal(0., 0.2, z_base.shape)
        t = fit_SimplexLSQFitter(Gaussian2D, x_grid, y_grid, z)
    except Warning:
        pass


def time_Polynomial1D_LevMarLSQFitter():
    warnings.filterwarnings('error')
    try:
        y = y_base + np.random.normal(0., 0.2, y_base.shape)
        t = fit_LevMarLSQFitter(Polynomial1D, x, y)
    except Warning:
        pass


def time_Polynomial1D_LinearLSQFitter():
    warnings.filterwarnings('error')
    try:
        y = y_base + np.random.normal(0., 0.2, y_base.shape)
        t = fit_LinearLSQFitter(Polynomial1D, x, y)
    except Warning:
        pass


def time_Polynomial2D_LevMarLSQFitter():
    warnings.filterwarnings('error')
    try:
        z = z_base + np.random.normal(0., 0.2, z_base.shape)
        t = fit_LevMarLSQFitter(Polynomial2D, x_grid, y_grid, z)
    except Warning:
        pass


def time_Polynomial2D_LinearLSQFitter():
    warnings.filterwarnings('error')
    try:
        z = z_base + np.random.normal(0., 0.2, z_base.shape)
        t = fit_LinearLSQFitter(Polynomial2D, x_grid, y_grid, z)
    except Warning:
        pass


def time_Chebyshev1D_LevMarLSQFitter():
    warnings.filterwarnings('error')
    try:
        y = y_base + np.random.normal(0., 0.2, y_base.shape)
        t = fit_LevMarLSQFitter(Chebyshev1D, x, y)
    except Warning:
        pass


def time_Chebyshev1D_LinearLSQFitter():
    warnings.filterwarnings('error')
    try:
        y = y_base + np.random.normal(0., 0.2, y_base.shape)
        t = fit_LinearLSQFitter(Chebyshev1D, x, y)
    except Warning:
        pass


def time_Chebyshev2D_LevMarLSQFitter():
    warnings.filterwarnings('error')
    try:
        z = z_base + np.random.normal(0., 0.2, z_base.shape)
        t = fit_LevMarLSQFitter(Chebyshev2D, x_grid, y_grid, z)
    except Warning:
        pass


def time_Chebyshev2D_LinearLSQFitter():
    warnings.filterwarnings('error')
    try:
        z = z_base + np.random.normal(0., 0.2, z_base.shape)
        t = fit_LinearLSQFitter(Chebyshev2D, x_grid, y_grid, z)
    except Warning:
        pass

def time_combined_gauss_1d_LevMarLSQFitter():
    warnings.filterwarnings('error')
    try:
        y = y_base + np.random.normal(0., 0.2, y_base.shape)
        t = fit_LevMarLSQFitter(combined_gauss_1d, x, y)
    except Warning:
        pass

def time_combined_gauss_1d_SLSQPLSQFitter():
    warnings.filterwarnings('error')
    try:
        y = y_base + np.random.normal(0., 0.2, y_base.shape)
        t = fit_SLSQPLSQFitter(combined_gauss_1d, x, y)
    except Warning:
        pass

def time_combined_gauss_2d_LevMarLSQFitter():
    warnings.filterwarnings('error')
    try:
        z = z_base + np.random.normal(0., 0.2, z_base.shape)
        t = fit_LevMarLSQFitter(combined_gauss_2d, x_grid, y_grid, z)
    except Warning:
        pass

def time_combined_gauss_2d_SLSQPLSQFitter():
    warnings.filterwarnings('error')
    try:
        z = z_base + np.random.normal(0., 0.2, z_base.shape)
        t = fit_SLSQPLSQFitter(combined_gauss_2d, x_grid, y_grid, z)
    except Warning:
        pass

