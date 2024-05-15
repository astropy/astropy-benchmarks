import numpy as np
from numpy.random import Generator, PCG64
from astropy.wcs import WCS

wcs = WCS(naxis=2)
wcs.wcs.ctype = "RA---TAN", "DEC--TAN"
wcs.wcs.crval = 30.0, 40.0
wcs.wcs.crpix = 10.0, 12.0
wcs.wcs.cdelt = 0.01, 0.01


class WCSTransformations:
    params = [1, 1_000, 1_000_000]

    def setup(self, size):
        np.random.seed(12345)
        gen = Generator(PCG64())
        self.px = gen.uniform(0, 20, size)
        self.py = gen.uniform(0, 20, size)
        self.pxy = np.vstack([self.px, self.py])
        self.wx, self.wy = wcs.wcs_pix2world(self.px, self.py, 0)
        self.wxy = np.vstack([self.wx, self.wy])
        self.coord = wcs.pixel_to_world(self.px, self.py)

    def time_pix2world_x_y_0(self, size):
        wcs.wcs_pix2world(self.px, self.py, 0)

    def time_pix2world_x_y_1(self, size):
        wcs.wcs_pix2world(self.px, self.py, 1)

    def time_world2pix_x_y_0(self, size):
        wcs.wcs_world2pix(self.wx, self.wy, 0)

    def time_world2pix_x_y_1(self, size):
        wcs.wcs_world2pix(self.wx, self.wy, 1)

    def time_ape14_pixel_to_world(self, size):
        wcs.pixel_to_world(self.px, self.py)

    def time_ape14_world_to_pixel(self, size):
        wcs.world_to_pixel(self.coord)
