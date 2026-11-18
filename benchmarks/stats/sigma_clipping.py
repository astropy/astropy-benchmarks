import numpy as np
from astropy.utils.misc import NumpyRNGContext


class SigmaClipBenchmarks:
    def setup(self):
        # Avoid top-level module import to make sure that the benchmarks are
        # compatible with versions of astropy that did not have this functionality.
        from astropy.stats import SigmaClip

        size = (4, 2048, 2048)

        with NumpyRNGContext(12345):
            self.data = np.random.normal(size=size)

            # add outliers
            nbad = 100000
            zbad = np.random.randint(low=0, high=size[0] - 1, size=nbad)
            ybad = np.random.randint(low=0, high=size[1] - 1, size=nbad)
            xbad = np.random.randint(low=0, high=size[2] - 1, size=nbad)
            self.data[zbad, ybad, xbad] = np.random.choice([-1, 1], size=nbad) * (
                10 + np.random.rand(nbad)
            )

            # The defaults use median as the cenfunc and standard
            # deviation as the stdfunc.  The default iters is 5.
            self.sigclip = SigmaClip(sigma=3)

    # pytest compat
    setup_method = setup

    def time_3d_array(self):
        self.sigclip(self.data[:, :1024, :1024])

    def time_3d_array_axis(self):
        self.sigclip(self.data, axis=0)

    def time_3d_array_axis2(self):
        self.sigclip(self.data, axis=(0, 1))

    def time_2d_array(self):
        self.sigclip(self.data[0])

    def time_2d_array_axis(self):
        self.sigclip(self.data[0], axis=0)

    def time_1d_array(self):
        self.sigclip(self.data[0][0])
