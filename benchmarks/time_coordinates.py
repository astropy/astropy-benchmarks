import numpy as np
from astropy import coordinates
from astropy import units


def time_latitude():
    coordinates.Latitude(3.2, units.degree)


class SkyCoordBenchmarks:
    def setup(self):
        N = int(1e6)
        lon, lat = np.ones(N), np.ones(N)
        self.coord = coordinates.SkyCoord(lon, lat, unit='deg', frame='icrs')

    def time_repr(self):
        repr(self.coord)

    def time_icrs_to_galactic(self):
        self.coord.transform_to('galactic')
