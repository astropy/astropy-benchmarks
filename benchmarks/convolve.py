import numpy as np
from astropy.convolution import convolve, convolve_fft

# What is considered small or large in terms of kernels/arrays depends on the
# dimensionality of the kernel, so we simply parameterize as 'small' and 'large'
# and then define what this means below for each dimension. Note that large still
# needs to be fast enough to run in ~1s in the benchmarks - the idea is more to
# have one that is likely overhead-limited, and one that is computation-limited.

DIMENSIONS = [1, 2, 3]
SIZES = ['small', 'large']
BOUNDARIES = [None, 'fill', 'wrap', 'extend']
NAN_TREATMENTS = ['fill', 'interpolate']

kernel_shapes = {
    1: {'small': (3,), 'large': (1431,)},
    2: {'small': (3, 3), 'large': (51, 49)},
    3: {'small': (3, 3, 3), 'large': (11, 9, 13)},
}


array_shapes = {
    1: {'small': (3,), 'large': (10022,)},
    2: {'small': (3, 3), 'large': (256, 256)},
    3: {'small': (3, 3, 3), 'large': (51, 52, 55)},
}


class Convolve:

    params = (DIMENSIONS, SIZES, BOUNDARIES, NAN_TREATMENTS)
    param_names = ['ndim', 'size', 'boundary', 'nan_treatment']

    def setup(self, ndim, size, boundary, nan_treatment):

        print(ndim, size, boundary, nan_treatment)

        np.random.seed(12345)

        self.kernel = np.random.random(kernel_shapes[ndim][size])
        self.array = np.random.random(array_shapes[ndim][size])

    def time_convolve(self, ndim, size, boundary, nan_treatment):
        convolve(self.array, self.kernel,
                 boundary=boundary, nan_treatment=nan_treatment)
