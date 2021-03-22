import os
import warnings

import numpy as np

from astropy.io import ascii
from astropy import units as u
from astropy.modeling import models, fitting

fit_LevMarLSQFitter = fitting.LevMarLSQFitter()
fit_SLSQPLSQFitter = fitting.SLSQPLSQFitter()
fit_SimplexLSQFitter = fitting.SimplexLSQFitter()
fit_LinearLSQFitter = fitting.LinearLSQFitter()

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

large_gauss_combined_1d = models.Gaussian1D()
large_gauss_combined_2d = models.Gaussian2D()
for i in range(20):
    mean = i*0.5
    stddev = i*0.1
    large_gauss_combined_1d += models.Gaussian1D(mean=mean, stddev=stddev)
    large_gauss_combined_2d += models.Gaussian2D(x_mean=mean, y_mean=mean, \
            x_stddev=stddev, y_stddev=stddev)

x = np.linspace(-5., 5., 200)
y_base = 3 * np.exp(-0.5 * (x - 1.3)**2 / 0.8**2)

x_grid, y_grid = np.meshgrid(x, x)
z_base = 3 * np.exp(-0.5* ((x_grid - 1.3)**2/0.8**2 + (y_grid - 2.1)**2/0.1**2))

# Constraint Data Fitting:
#   Based on Exercise 2 in this notebook:
#       https://github.com/spacetelescope/JWSTUserTraining2016/blob/master/Day_Zero_Notebooks/06.Modeling/astropy_modeling_solutions.ipynb
here = os.path.abspath(os.path.dirname(__file__))
sdss = ascii.read(os.path.join(here, 'sample_sdss.txt'))
wave = sdss['lambda']
flux = sdss['flux']
mean_flux = flux.mean()
cont = np.where(flux > mean_flux, mean_flux, flux)
hbeta_combo = models.Gaussian1D(34, 4862.721, 5) + \
        models.Gaussian1D(170, 5008.239, 5) + \
        models.Gaussian1D(57, 4958.911, 5) + \
        fit_LinearLSQFitter(models.Polynomial1D(1), wave, cont)

def tie_ampl(model):
    return model.amplitude_2 / 3.1
hbeta_combo.amplitude_1.tied = tie_ampl

def tie_wave(model):
    return model.mean_0 * 4858.911/4862.721
hbeta_combo.mean_1.tied = tie_wave

# Model Set fitting:
#   Based on Fitting Model Sets example:
#       https://docs.astropy.org/en/latest/modeling/example-fitting-model-sets.html
depth, width, height = 10, 500, 500
t = np.arange(depth, dtype=np.float64)*10
fluxes = np.arange(1. * width * height).reshape(width, height)
image = fluxes[np.newaxis, :, :] * t[:, np.newaxis, np.newaxis]
image += np.random.normal(0.0, image*0.05, size=image.shape)
line = models.Polynomial1D(degree=1, n_models=width*height)
pixels = image.reshape((depth, width*height))

# Physical model fitting with units
#   Based on this test:
#       https://github.com/astropy/astropy/blob/master/astropy/modeling/tests/test_physical_models.py#L65
black_body = models.BlackBody(3000 * u.K, scale=5e-17 * u.Jy / u.sr)
wav = np.array([0.5, 5, 10]) * u.micron
fnu = np.array([1, 10, 5]) * u.Jy / u.sr

# Fitting models with uncertainties
#   Based on this example:
#       https://docs.astropy.org/en/latest/modeling/example-fitting-line.html#fit-using-uncertainties
line_orig = models.Linear1D(slope=1.0, intercept=0.5)
x_points = np.random.uniform(0.0, 10.0, 200)
y_unc = np.absolute(np.random.normal(0.5, 2.5, x_points.shape))
y_points = line_orig(x_points) + np.random.normal(0.0, y_unc, y_unc.shape)
line_init = models.Linear1D()


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


def time_datafit_Polynomial1D_LinearLSQFitter():
    warnings.filterwarnings('error')
    try:
        poly_cont = fit_LinearLSQFitter(models.Polynomial1D(1), wave, cont)
    except Warning:
        pass


def time_datafit_compound_LevMarLSQFitter():
    warnings.filterwarnings('error')
    try:
        fitted_model = fit_LevMarLSQFitter(hbeta_combo, wave, flux)
    except Warning:
        pass


def time_large_gauss_combined_1d_LevMarLSQFitter():
    warnings.filterwarnings('error')
    try:
        y = y_base + np.random.normal(0., 0.2, y_base.shape)
        t = fit_LevMarLSQFitter(large_gauss_combined_1d, x, y)
    except Warning:
        pass


def time_large_gauss_combined_1d_SLSQPLSQFitter():
    warnings.filterwarnings('error')
    try:
        y = y_base + np.random.normal(0., 0.2, y_base.shape)
        t = fit_SLSQPLSQFitter(large_gauss_combined_1d, x, y)
    except Warning:
        pass


def time_large_gauss_combined_2d_LevMarLSQFitter():
    warnings.filterwarnings('error')
    try:
        z = z_base + np.random.normal(0., 0.2, z_base.shape)
        t = fit_LevMarLSQFitter(large_gauss_combined_2d, x_grid, y_grid, z)
    except Warning:
        pass


def time_large_gauss_combined_2d_SLSQPLSQFitter():
    warnings.filterwarnings('error')
    try:
        z = z_base + np.random.normal(0., 0.2, z_base.shape)
        t = fit_SLSQPLSQFitter(large_gauss_combined_2d, x_grid, y_grid, z)
    except Warning:
        pass


def time_multi_model_LinearLSQFitter():
    warnings.filterwarnings('error')
    try:
        y = pixels.T
        new_model = fit_LinearLSQFitter(line, x=t, y=y)
    except Warning:
        pass


def time_physical_model_with_units_LevMarLSQFitter():
    warnings.filterwarnings('error')
    try:
        black_body_fit = fit_LevMarLSQFitter(black_body, wav, fnu)
    except Warning:
        pass


def time_uncertanty_Linear1D_LinearLSQFitter():
    warnings.filterwarnings('error')
    try:
        line_fit = fit_LinearLSQFitter(line_init, x_points, y_points, weights=1.0/y_unc)
    except Warning:
        pass

