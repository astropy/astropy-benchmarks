import numpy as np

from astropy.modeling import models, fitting
from astropy import units as u


def time_init_LevMarLSQFitter():
    fit = fitting.LevMarLSQFitter()


def time_init_SLSQPLSQFitter():
    fit = fitting.SLSQPLSQFitter()


def time_init_SimplexLSQFitter():
    fit = fitting.SimplexLSQFitter()


def time_init_LinearLSQFitter():
    fit = fitting.LinearLSQFitter()

