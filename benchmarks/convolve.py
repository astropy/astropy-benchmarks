import concurrent.futures

import numpy as np
from astropy.convolution import convolve, convolve_fft

# What is considered small or large in terms of kernels/arrays depends on the
# dimensionality of the kernel, so we simply parameterize as 'small' and 'large'
# and then define what this means below for each dimension. Note that large still
# needs to be fast enough to run in ~1s in the benchmarks - the idea is more to
# have one that is likely overhead-limited, and one that is computation-limited.

DIMENSIONS = [1, 2, 3]
SIZES = ["small", "large"]
BOUNDARIES = [None, "fill", "wrap", "extend"]

# None is equivalent to 'fill', and 'extend' isn't available as of astropy 7.0
BOUNDARIES_FFT = ["fill", "wrap"]
NAN_TREATMENTS = ["fill", "interpolate"]

kernel_shapes = {
    1: {"small": (3,), "large": (1431,)},
    2: {"small": (3, 3), "large": (51, 49)},
    3: {"small": (3, 3, 3), "large": (11, 9, 13)},
}


array_shapes = {
    1: {"small": (3,), "large": (10022,)},
    2: {"small": (3, 3), "large": (256, 256)},
    3: {"small": (3, 3, 3), "large": (51, 52, 55)},
}


class Convolve:
    params = (DIMENSIONS, SIZES, BOUNDARIES, NAN_TREATMENTS)
    param_names = ["ndim", "size", "boundary", "nan_treatment"]

    def setup(self, ndim, size, boundary, nan_treatment):
        np.random.seed(12345)

        self.kernel = np.random.random(kernel_shapes[ndim][size])
        self.array = np.random.random(array_shapes[ndim][size])

    def time_convolve(self, ndim, size, boundary, nan_treatment):
        convolve(
            self.array, self.kernel, boundary=boundary, nan_treatment=nan_treatment
        )

class ConvolveFFT:
    params = (DIMENSIONS, SIZES, BOUNDARIES_FFT, NAN_TREATMENTS)
    param_names = ["ndim", "size", "boundary", "nan_treatment"]

    def setup(self, ndim, size, boundary, nan_treatment):
        np.random.seed(12345)

        self.kernel = np.random.random(kernel_shapes[ndim][size])
        self.array = np.random.random(array_shapes[ndim][size])

    def time_convolve_fft(self, ndim, size, boundary, nan_treatment):
        convolve_fft(
            self.array, self.kernel, boundary=boundary, nan_treatment=nan_treatment
        )


# ConvolveThreaded measures how well ``astropy.convolution.convolve`` scales
# under a threaded executor. We submit a fixed amount of work (``NUM_CALLS``
# independent ``convolve`` calls) and vary the worker thread count: with the
# GIL held in the Cython wrapper the workers serialize and the wall-clock is
# the same regardless of ``n_threads``; with the GIL released around the C
# call the wall-clock drops roughly linearly with ``n_threads`` up to the
# available core count. The ratio of the ``n_threads=1`` to ``n_threads=4``
# rows is the measurable scaling signal.

THREAD_COUNTS = [1, 4]
NUM_CALLS = 4


class ConvolveThreaded:
    params = (DIMENSIONS, THREAD_COUNTS)
    param_names = ["ndim", "n_threads"]

    def setup(self, ndim, n_threads):
        # Use ``default_rng`` so we don't mutate the legacy global seed
        # state shared with other benchmarks running in the same process.
        rng = np.random.default_rng(12345)
        self.kernel = rng.random(kernel_shapes[ndim]["large"])
        # Distinct array per call so we measure independent convolutions
        # rather than shared-data contention.
        self.arrays = [
            rng.random(array_shapes[ndim]["large"]) for _ in range(NUM_CALLS)
        ]
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=n_threads)

    def teardown(self, ndim, n_threads):
        self.executor.shutdown()

    def time_convolve_threaded(self, ndim, n_threads):
        futures = [
            self.executor.submit(convolve, array, self.kernel)
            for array in self.arrays
        ]
        for future in futures:
            future.result()
