import numpy as np

from astropy.table import MaskedColumn
from astropy.time import Time
from astropy.timeseries import TimeSeries, aggregate_downsample
import astropy.units as u
from astropy.utils.masked import Masked


class TimeSeriesBenchmarks:
    def setup(self):
        num_samples = 1000
        time_diff = np.linspace(1, num_samples, num=num_samples)

        ts = TimeSeries(time=Time(2450000 + time_diff, format="jd"))

        # Columns with various column types
        np.random.seed(12345)

        ts["a"] = np.random.random(num_samples)  # plain Column

        ts["a_mc"] = MaskedColumn(ts["a"].value, mask=False)
        ts["a_mc"][1] = True  # just to ensure some value is masked

        ts["a_q"] = ts["a"] * u.dimensionless_unscaled  # Quantity

        ts["a_mq"] = Masked(ts["a_q"])  # MaskedQuantity
        ts["a_mq"][1] = True  # just to ensure some value is masked

        self.ts = ts

    def _do_time_aggregate_downsample(self, aggregate_func):
        aggregate_downsample(
            self.ts, time_bin_size=5 * u.d, aggregate_func=aggregate_func
        )

    def time_aggregate_downsample_default(self):
        # case default aggregate_func (optimized in v7.1.0+)
        self._do_time_aggregate_downsample(None)

    def time_aggregate_downsample_np_nanmean(self):
        # case non-optimized aggregate_func
        self._do_time_aggregate_downsample(np.nanmean)

    # FIXME: it hits the known issue in astropy/utils/masked/core.py
    #   NotImplementedError: masked instances cannot yet deal with 'reduceat' or 'at'.
    #   relevant PR: https://github.com/astropy/astropy/pull/17875
    # def time_aggregate_downsample_np_add(self):
    #     # case aggregate_func is optimized (with `.reduceat`)
    #     self._do_time_aggregate_downsample(np.add)
