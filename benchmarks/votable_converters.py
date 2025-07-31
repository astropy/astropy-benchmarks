import numpy as np
import numpy.ma as ma
from astropy.io.votable.converters import bool_to_bitarray, bitarray_to_bool

SMALL_SIZE = 1000
LARGE_SIZE = 100000


class TimeBitArrayConverters:
    """Direct converter function benchmarks."""

    def setup(self):
        rng = np.random.default_rng(42)

        self.small_bool = rng.integers(0, 2, SMALL_SIZE, dtype=bool)
        self.large_bool = rng.integers(0, 2, LARGE_SIZE, dtype=bool)

        mask = rng.random(LARGE_SIZE) < 0.2
        self.masked_bool = ma.array(self.large_bool, mask=mask)

        self.small_bits = bool_to_bitarray(self.small_bool)
        self.large_bits = bool_to_bitarray(self.large_bool)

    def time_bool_to_bitarray_small(self):
        bool_to_bitarray(self.small_bool)

    def time_bool_to_bitarray_large(self):
        bool_to_bitarray(self.large_bool)

    def time_bool_to_bitarray_masked(self):
        bool_to_bitarray(self.masked_bool)

    def time_bitarray_to_bool_small(self):
        bitarray_to_bool(self.small_bits, len(self.small_bool))

    def time_bitarray_to_bool_large(self):
        bitarray_to_bool(self.large_bits, len(self.large_bool))
