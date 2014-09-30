import numpy as np
from astropy import coordinates as coords
from astropy import units as u


def time_latitude():
    coords.Latitude(3.2, u.degree)


class FrameBenchmarks:

    def setup(self):

        self.scalar_ra = 3.2 * u.deg
        self.scalar_dec = 2.2 * u.deg

        self.array_ra = np.linspace(0., 360., 1000) * u.deg
        self.array_dec = np.linspace(-90., 90., 1000) * u.deg

    def time_init_nodata(self):
        coords.FK5()

    def time_init_scalar(self):
        coords.FK5(self.scalar_ra, self.scalar_dec)

    def time_init_array(self):
        coords.FK5(self.array_ra, self.array_dec)


class SkyCoordBenchmarks:

    def setup(self):
        N = int(1e6)
        lon, lat = np.ones(N), np.ones(N)
        self.coord = coords.SkyCoord(lon, lat, unit='deg', frame='icrs')

    def time_repr(self):
        repr(self.coord)

    def time_icrs_to_galactic(self):
        self.coord.transform_to('galactic')
