import numpy as np
from astropy.coordinates import (SkyCoord, FK5, Latitude, Angle, ICRS,
                                 concatenate)
from astropy import units as u


def time_latitude():
    Latitude(3.2, u.degree)


ANGLES = Angle(np.ones(10000), u.deg)


def time_angle_array_repr():
    # Prior to Astropy 3.0, this was very inefficient
    repr(ANGLES)


def time_angle_array_str():
    # Prior to Astropy 3.0, this was very inefficient
    str(ANGLES)


def time_angle_array_repr_latex():
    # Prior to Astropy 3.0, this was very inefficient
    ANGLES._repr_latex_()


class FrameBenchmarks:

    def setup(self):

        self.scalar_ra = 3.2 * u.deg
        self.scalar_dec = 2.2 * u.deg

        self.array_ra = np.linspace(0., 360., 1000) * u.deg
        self.array_dec = np.linspace(-90., 90., 1000) * u.deg

        self.icrs_scalar = ICRS(ra=1*u.deg, dec=2*u.deg)
        self.icrs_array = ICRS(ra=np.random.random(10000)*u.deg,
                               dec=np.random.random(10000)*u.deg)

    def time_init_nodata(self):
        FK5()

    def time_init_scalar(self):
        FK5(self.scalar_ra, self.scalar_dec)

    def time_init_array(self):
        FK5(self.array_ra, self.array_dec)

    def time_concatenate_scalar(self):
        concatenate((self.icrs_scalar, self.icrs_scalar))

    def time_concatenate_array(self):
        concatenate((self.icrs_array, self.icrs_array))


class SkyCoordBenchmarks:

    def setup(self):

        self.coord_scalar = SkyCoord(1, 2, unit='deg', frame='icrs')

        lon, lat = np.ones(1000), np.ones(1000)
        self.coord_array_1 = SkyCoord(lon, lat, unit='deg', frame='icrs')

        lon, lat = np.ones(1000000), np.ones(1000000)
        self.coord_array_2 = SkyCoord(lon, lat, unit='deg', frame='icrs')

    def time_init_scalar(self):
        SkyCoord(1, 2, unit='deg', frame='icrs')

    def time_init_array(self):
        N = int(1e6)
        lon, lat = np.ones(N), np.ones(N)
        SkyCoord(lon, lat, unit='deg', frame='icrs')

    def time_repr_scalar(self):
        repr(self.coord_scalar)

    def time_repr_array(self):
        repr(self.coord_array_1)

    def time_icrs_to_galactic_scalar(self):
        self.coord_scalar.transform_to('galactic')

    def time_icrs_to_galactic_array(self):
        self.coord_array_2.transform_to('galactic')

    def time_iter_array(self):
        for c in self.coord_array_1:
            pass
