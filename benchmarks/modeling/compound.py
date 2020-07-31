import numpy as np
from astropy.modeling import models
from astropy import units as u


x_no_units_scalar = 5
x_no_units_small = np.linspace(-4, 3, 50)
x_no_units_medium = np.linspace(-40, 300, 2000)
x_no_units_big = np.linspace(-4, 300, 5000000)


def time_init_7_no_units():
    m = (models.Shift(-10.5) & models.Shift(-13.2) |
         models.AffineTransformation2D(matrix=[[1, 0], [0, 1]],
                                       translation=[0, 0]) |
         models.Scale(.01) & models.Scale(.04) |
         models.Pix2Sky_TAN() |
         models.RotateNative2Celestial(5.6, -72.05, 180))


def time_init_7_with_units():
    aff = models.AffineTransformation2D(matrix=[[1, 0], [0, 1]]*u.arcsec,
                                        translation=[0, 0]*u.arcsec)
    aff.input_units_equivalencies = {'x': u.pixel_scale(1*u.arcsec/u.pix),
                                     'y': u.pixel_scale(1*u.arcsec/u.pix)}
    m = (models.Shift(-10.5*u.pix) & models.Shift(-13.2*u.pix) |
         aff |
         models.Scale(.01*u.arcsec) & models.Scale(.04*u.arcsec) |
         models.Pix2Sky_TAN() |
         models.RotateNative2Celestial(5.6*u.deg, -72.05*u.deg, 180*u.deg))


class EvaluateCompoundModelNoUnits:
    def setup(self):
        aff = models.AffineTransformation2D(matrix=[[1, 0], [0, 1]],
                                            translation=[0, 0])
        self.model = (models.Shift(-10.5) & models.Shift(-13.2) | aff |
                      models.Scale(.01) & models.Scale(.04) |
                      models.Pix2Sky_TAN() |
                      models.RotateNative2Celestial(5.6, -72.05, 180))

    def time_scalar(self):
        r, d = self.model(x_no_units_scalar, x_no_units_scalar)

    def time_small(self):
        r, d = self.model(x_no_units_small, x_no_units_small)

    def time_medium(self):
        r, d = self.model(x_no_units_medium, x_no_units_medium)

    def time_big(self):
        r, d = self.model(x_no_units_big, x_no_units_big)


class EvaluateCompoundModelWithUnits:
    def setup(self):
        aff = models.AffineTransformation2D(matrix=[[1, 0], [0, 1]] * u.arcsec,
                                            translation=[0, 0] * u.arcsec)
        aff.input_units_equivalencies = {'x': u.pixel_scale(1 * u.arcsec/u.pix),
                                         'y': u.pixel_scale(1 * u.arcsec/u.pix)}
        self.model = (models.Shift(-10.5 * u.pix) & models.Shift(-13.2 * u.pix) |
                      aff |
                      models.Scale(.01 * u.arcsec) & models.Scale(.04 * u.deg) |
                      models.Pix2Sky_TAN() |
                      models.RotateNative2Celestial(5.6 * u.deg, -72.05 * u.deg, 180 * u.deg))

    def time_scalar(self):
        r, d = self.model(x_no_units_scalar * u.pix, x_no_units_scalar * u.pix)

    def time_small(self):
        r, d = self.model(x_no_units_small * u.pix, x_no_units_small * u.pix)

    def time_medium(self):
        r, d = self.model(x_no_units_medium * u.pix, x_no_units_medium * u.pix)

    def time_big(self):
        r, d, = self.model(x_no_units_big * u.pix, x_no_units_big * u.pix)
