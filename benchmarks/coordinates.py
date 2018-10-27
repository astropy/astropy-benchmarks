import numpy as np
from astropy.coordinates import (SkyCoord, FK5, Latitude, Angle, ICRS,
                                 concatenate, UnitSphericalRepresentation,
                                 CartesianRepresentation, CartesianDifferential)
from astropy import units as u
from astropy.time import Time


def time_latitude():
    Latitude(3.2, u.degree)


ANGLES = Angle(np.ones(10000), u.deg)
J2010 = Time('J2010')
fk5_J2010 = FK5(equinox=J2010)
rnd = np.random.RandomState(seed=42)


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

        self.icrs_scalar = ICRS(ra=1*u.deg, dec=2*u.deg)
        self.icrs_array = ICRS(ra=rnd.random(10000)*u.deg,
                               dec=rnd.random(10000)*u.deg)

        self.scalar_rep = CartesianRepresentation([1, 2, 3.] * u.kpc)
        self.scalar_dif = CartesianDifferential([1, 2, 3.] * u.km/u.s)

        # Some points to use for benchmarking coordinate matching.
        # These were motivated by some tests done in astropy/astropy#7324:
        # https://github.com/astropy/astropy/pull/7324#issuecomment-392382719
        xyz_uniform1 = rnd.uniform((10000, 3))
        xyz_uniform2 = rnd.uniform((10000, 3))
        self.icrs_uniform1 = ICRS(xyz_uniform1,
                                  representation_type=CartesianRepresentation)
        self.icrs_uniform2 = ICRS(xyz_uniform2,
                                  representation_type=CartesianRepresentation)

        phi = rnd.uniform(0, 2*np.pi, size=10000)
        theta = np.arccos(2*rnd.uniform(size=10000) - 1)
        xyz_uniform_sph1 = np.vstack((np.cos(phi)*np.sin(theta),
                                      np.sin(phi)*np.sin(theta),
                                      np.cos(theta))).T

        phi = rnd.uniform(0, 2*np.pi, size=10000)
        theta = np.arccos(2*rnd.uniform(size=10000) - 1)
        xyz_uniform_sph2 = np.vstack((np.cos(phi)*np.sin(theta),
                                      np.sin(phi)*np.sin(theta),
                                      np.cos(theta))).T
        self.icrs_uniform_sph1 = ICRS(
            xyz_uniform_sph1, representation_type=CartesianRepresentation)
        self.icrs_uniform_sph2 = ICRS(
            xyz_uniform_sph2, representation_type=CartesianRepresentation)

        xyz0 = rnd.uniform(-100, 100, size=(8, 3))
        xyz_clustered1 = np.vstack(rnd.normal(xyz0, size=(10000, 8, 3)))
        xyz_clustered2 = np.vstack(rnd.normal(xyz0, size=(10000, 8, 3)))
        self.icrs_clustered1 = ICRS(
            xyz_clustered1, representation_type=CartesianRepresentation)
        self.icrs_clustered2 = ICRS(
            xyz_clustered2, representation_type=CartesianRepresentation)

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

    def time_coord_match_uniform(self):
        self.icrs_uniform1.match_to_catalog_sky(self.icrs_uniform2)

    def time_coord_match_sphere(self):
        self.icrs_uniform_sph1.match_to_catalog_sky(self.icrs_uniform_sph2)

    def time_coord_match_clusters(self):
        self.icrs_clustered1.match_to_catalog_sky(self.icrs_clustered2)


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

        self.array_q_ra = rnd.rand(int(1e6)) * 360 * u.deg
        self.array_q_dec = (rnd.rand(int(1e6)) * 180 - 90) * u.deg

        self.scalar_repr = UnitSphericalRepresentation(lat=self.scalar_q_dec,
                                                       lon=self.scalar_q_ra)
        self.array_repr = UnitSphericalRepresentation(lat=self.array_q_dec,
                                                      lon=self.array_q_ra)

    def time_init_scalar(self):
        SkyCoord(1, 2, unit='deg', frame='icrs')

    def time_init_array(self):
        SkyCoord(self.lon_1e6, self.lat_1e6, unit='deg', frame='icrs')

    def time_init_quantity_scalar_positional(self):
        SkyCoord(self.scalar_q_ra, self.scalar_q_dec)

    def time_init_quantity_array_positional(self):
        SkyCoord(self.array_q_ra, self.array_q_dec)

    def time_init_quantity_scalar_positional_fk5_kwarg(self):
        SkyCoord(self.scalar_q_ra, self.scalar_q_dec,
                 frame='fk5', equinox=J2010)

    def time_init_quantity_scalar_positional_fk5_frame(self):
        SkyCoord(self.scalar_q_ra, self.scalar_q_dec,
                 frame=fk5_J2010)

    def time_init_quantity_scalar_positional_fk5_frame_extra_kwargs(self):
        SkyCoord(self.scalar_q_ra, self.scalar_q_dec,
                 frame=fk5_J2010, obstime=J2010)

    def time_init_quantity_scalar_keyword(self):
        SkyCoord(ra=self.scalar_q_ra, dec=self.scalar_q_dec)

    def time_init_quantity_array_keyword(self):
        SkyCoord(ra=self.array_q_ra, dec=self.array_q_dec)

    def time_init_repr_scalar(self):
        SkyCoord(self.scalar_repr)

    def time_init_repr_array(self):
        SkyCoord(self.array_repr)

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
