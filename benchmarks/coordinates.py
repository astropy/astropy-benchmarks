import numpy as np
from astropy.coordinates import (SkyCoord, FK5, Latitude, Angle, ICRS,
                                 concatenate, UnitSphericalRepresentation,
                                 CartesianRepresentation, CartesianDifferential)
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


class RepresentationBenchmarks:

    def setup(self):

        self.scalar_rep = CartesianRepresentation([1., 2, 3] * u.kpc)
        self.scalar_dif = CartesianDifferential([1, 2, 3.] * u.km/u.s)

        self.array_rep = CartesianRepresentation(np.ones((3, 1000)) * u.kpc)
        self.array_dif = CartesianDifferential(np.ones((3, 1000)) * u.km/u.s)

    def time_with_differentials_scalar(self):
        self.scalar_rep.with_differentials(self.scalar_dif)

    def time_with_differentials_array(self):
        self.array_rep.with_differentials(self.array_dif)


class FrameBenchmarks:

    def setup(self):

        self.scalar_ra = 3.2 * u.deg
        self.scalar_dec = 2.2 * u.deg

        self.scalar_pmra = 3.2 * u.mas/u.yr
        self.scalar_pmdec = 2.2 * u.mas/u.yr

        self.array_ra = np.linspace(0., 360., 1000) * u.deg
        self.array_dec = np.linspace(-90., 90., 1000) * u.deg

        np.random.seed(12345)
        self.icrs_scalar = ICRS(ra=1*u.deg, dec=2*u.deg)
        self.icrs_array = ICRS(ra=np.random.random(10000)*u.deg,
                               dec=np.random.random(10000)*u.deg)

        self.scalar_rep = CartesianRepresentation([1., 2, 3] * u.kpc)
        self.scalar_dif = CartesianDifferential([1, 2, 3.] * u.km/u.s)

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

    def time_init_scalar_diff(self):
        FK5(self.scalar_ra, self.scalar_dec,
            pm_ra_cosdec=self.scalar_pmra,
            pm_dec=self.scalar_pmdec)


class SkyCoordBenchmarks:

    def setup(self):

        self.coord_scalar = SkyCoord(1, 2, unit='deg', frame='icrs')

        lon, lat = np.ones((2, 1000))
        self.coord_array_1e3 = SkyCoord(lon, lat, unit='deg', frame='icrs')

        self.lon_1e6, self.lat_1e6 = np.ones((2, int(1e6)))
        self.coord_array_1e6 = SkyCoord(self.lon_1e6, self.lat_1e6,
                                        unit='deg', frame='icrs')

        self.scalar_q_ra = 1 * u.deg
        self.scalar_q_dec = 2 * u.deg

        np.random.seed(12345)
        self.array_q_ra = np.random.rand(int(1e6)) * 360 * u.deg
        self.array_q_dec = (np.random.rand(int(1e6)) * 180 - 90) * u.deg

        self.scalar_repr = UnitSphericalRepresentation (lat=self.scalar_q_dec,
                                                        lon=self.scalar_q_ra)
        self.array_repr = UnitSphericalRepresentation (lat=self.array_q_dec,
                                                        lon=self.array_q_ra)

    def time_init_scalar(self):
        SkyCoord(1, 2, unit='deg', frame='icrs')

    def time_init_array(self):
        SkyCoord(self.lon_1e6, self.lat_1e6, unit='deg', frame='icrs')

    def time_init_quantity_scalar(self):
        SkyCoord(self.scalar_q_ra, self.scalar_q_dec, frame='icrs')

    def time_init_quantity_array(self):
        SkyCoord(self.array_q_ra, self.array_q_dec, frame='icrs')

    def time_init_repr_scalar(self):
        SkyCoord(self.scalar_repr, frame='icrs')

    def time_init_repr_array(self):
        SkyCoord(self.array_repr, frame='icrs')

    def time_repr_scalar(self):
        repr(self.coord_scalar)

    def time_repr_array(self):
        repr(self.coord_array_1e3)

    def time_icrs_to_galactic_scalar(self):
        self.coord_scalar.transform_to('galactic')

    def time_icrs_to_galactic_array(self):
        self.coord_array_1e6.transform_to('galactic')

    def time_iter_array(self):
        for c in self.coord_array_1e3:
            pass
