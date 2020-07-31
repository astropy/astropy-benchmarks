import numpy as np

from astropy.modeling import models
from astropy import units as u


gauss1d_no_units = models.Gaussian1D(amplitude=10, mean=5, stddev=1.2)
gauss1d_with_units = models.Gaussian1D(amplitude=10*u.Hz, mean=5*u.m, stddev=1.2*u.cm)

x_no_units_scalar = 5
x_no_units_small = np.linspace(-4, 3, 50)
x_no_units_medium = np.linspace(-40, 300, 2000)
x_no_units_big = np.linspace(-4, 300, 5000000)

x_with_units_scalar = 5*u.m
x_with_units_small = np.linspace(-4, 3, 50) * u.m
x_with_units_medium = np.linspace(-40, 300, 2000)* u.m
x_with_units_big = np.linspace(-4, 300, 5000000)* u.m


def time_model_init():
    m = models.Shift(2)

def time_model_init_2():
    m = models.Polynomial1D(1, c0=.2, c1=3.4)


def time_init_gaussian_no_units():
    m = models.Gaussian1D(amplitude=10, mean=5, stddev=1.2)

    
def time_init_gaussian_with_units():
    m = models.Gaussian1D(amplitude=10*u.Hz, mean=5*u.m, stddev=1.2*u.cm)

    
def time_eval_gaussian_no_units_scalar():
    gauss1d_no_units(x_no_units_scalar)

    
def time_eval_gaussian_no_units_small():
    gauss1d_no_units(x_no_units_small)

def time_eval_gaussian_no_units_medium():
    gauss1d_no_units(x_no_units_medium)

def time_eval_gaussian_no_units_big():
    gauss1d_no_units(x_no_units_big)


def time_eval_gaussian_with_units_scalar():
    gauss1d_with_units(x_with_units_scalar)

    
def time_eval_gaussian_with_units_small():
    gauss1d_with_units(x_with_units_small)

def time_eval_gaussian_with_units_medium():
    gauss1d_with_units(x_with_units_medium)

def time_eval_gaussian_with_units_big():
    gauss1d_with_units(x_with_units_big)
