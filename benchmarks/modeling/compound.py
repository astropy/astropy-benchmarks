import functools
import numpy as np
from astropy import units as u
from astropy.modeling.models import (Shift, Scale, AffineTransformation2D, Pix2Sky_TAN,
                                     RotateNative2Celestial, Rotation2D, Mapping, Identity,
                                     Polynomial2D, Polynomial1D)


xscalar, yscalar = 1, 2
x1d = np.linspace(-5, 5, 50)
y1d = np.linspace(-1, 9, 50)
yy, xx = np.mgrid[:1024, :1024]


def time_initialize_no_units():
    aff = AffineTransformation2D(matrix=[[1, 0], [0, 1]], translation=[0, 0])
    model = (Shift(-10.5) & Shift(-13.2) | aff |
             Scale(.01) & Scale(.04) | Pix2Sky_TAN() |
             RotateNative2Celestial(5.6, -72.05, 180))


def time_initialize_with_units():
    aff = AffineTransformation2D(matrix=[[1, 0], [0, 1]]*u.arcsec,
                                 translation=[0, 0]*u.arcsec)
    aff.input_units_equivalencies = {'x': u.pixel_scale(1*u.arcsec/u.pix),
                                     'y': u.pixel_scale(1*u.arcsec/u.pix)}
    model = (Shift(-10.5 * u.pix) & Shift(-13.2 * u.pix) | aff |
             Scale(.01) & Scale(.04) | Pix2Sky_TAN() |
             RotateNative2Celestial(5.6*u.deg, -72.05*u.deg, 180*u.deg))


class CompoundModelNoUnits:
    def setup(self):
        aff = AffineTransformation2D(matrix=[[1, 0], [0, 1]], translation=[0, 0])
        self.model = (Shift(-10.5) & Shift(-13.2) | aff |
                      Scale(.01) & Scale(.04) | Pix2Sky_TAN() |
                      RotateNative2Celestial(5.6, -72.05, 180))

    def time_scalar(self):
        r, d = self.model(xscalar, yscalar)

    def time_50(self):
        r, d = self.model(x1d, y1d)

    def time_million(self):
        r, d = self.model(xx, yy)


class CompoundModelWithUnits:
    def setup(self):
        aff = AffineTransformation2D(matrix=[[1, 0], [0, 1]] * u.arcsec,
                                     translation=[0, 0] * u.arcsec)
        aff.input_units_equivalencies = {'x': u.pixel_scale(1 * u.arcsec/u.pix),
                                         'y': u.pixel_scale(1 * u.arcsec/u.pix)}
        self.model = (Shift(-10.5 * u.pix) & Shift(-13.2 * u.pix) | aff |
                      Scale(.01 * u.arcsec) & Scale(.04 * u.deg) | Pix2Sky_TAN() |
                      RotateNative2Celestial(5.6 * u.deg, -72.05 * u.deg, 180 * u.deg))

    def time_scalar(self):
        r, d = self.model(xscalar*u.pix, yscalar*u.pix)

    def time_50(self):
        r, d = self.model(x1d * u.pix, y1d * u.pix)

    def time_million(self):
        r, d = self.model(xx * u.pix, yy * u.pix)


class Compound50:
    def create_models(degree):
        p21 = Polynomial2D(degree)
        coeffs = np.random.randn(len(p21.param_names))
        p21.parameters = coeffs
        p22 = p21.copy()
        model = (Shift(1) & Shift(2) | Mapping((0, 1, 0, 1)) | p21 & p22 |
                 Shift(-1) & Shift(-2) | Rotation2D(12) |
                 Identity(1) & Polynomial1D(1, c0=1, c1=1.2))
        return model

    def setup(self):
        models = []
        for i in range(1, 6):
            models.append(create_models(degree=i))
        self.model = functools.reduce(lambda x, y: x | y, models)

    def time_50(self):
        self.model(x1d, y1d)
