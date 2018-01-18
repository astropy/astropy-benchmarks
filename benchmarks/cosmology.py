import numpy as np
from astropy import units as u
from astropy.cosmology import FlatLambdaCDM, LambdaCDM


class LambdaCDMBenchmarks:
    H0 = 65 * u.km / u.s / u.Mpc
    TCMB0 = 2.7 * u.K
    params = [
        LambdaCDM(H0, 0.6, 0.7, 0),
        LambdaCDM(H0, 0.25, 0.65, TCMB0, 3.04),
        LambdaCDM(H0, 0.6, 0.7, TCMB0, 4),
        LambdaCDM(H0, 0.4, 0.2, TCMB0, 3.04),
        FlatLambdaCDM(H0, 0.25, 0),
        FlatLambdaCDM(H0, 0.25, TCMB0, 3.04),
        FlatLambdaCDM(H0, 0.25, TCMB0, 3.04,
                      [0.05, 0.1, 0.15] * u.eV)
    ]

    def setup(self, cosmo):
        self.cosmology = cosmo
        self.test_zs = np.linspace(0.1, 5.0, 200)

    def teardown(self, cosmo):
        del self.cosmology
        del self.test_zs

    def time_lumdist(self, cosmo):
        self.cosmology.luminosity_distance(self.test_zs)

    def time_age(self, cosmo):
        self.cosmology.age(self.test_zs)
