import numpy as np

from astropy.table import Column, MaskedColumn
from astropy.time import Time
from astropy.timeseries import TimeSeries, aggregate_downsample
import astropy.units as u
from astropy.utils.masked import Masked

from asv_runner.benchmarks.mark import skip_for_params


class TimeSeriesBenchmarks:
    params = [
        [  # col_type, for column type
            "col",  # plain column
            "mcol",  # MaskedColumn
            "qty",  # Quantity
            "mqty",  # MaskedQuantity
        ],
        [  # aggregate_func to be used
            None,  # default, optimized in astropy v7.1.0+
            np.nanmean,  # non-optimized
            np.add,  # optimized (with np.add.reduceat)
        ],
    ]

    param_names = ["col_type", "aggregate_func"]  # for ASV UI

    def setup(self, col_type, aggregate_func):
        num_samples = 1000
        time_diff = np.linspace(1, num_samples, num=num_samples)

        ts = TimeSeries(time=Time(2450000 + time_diff, format="jd"))

        # Columns with various column types
        np.random.seed(12345)

        vals = np.random.random(num_samples)
        vals[1] = np.nan  # some nan values

        if col_type == "col":  # plain Column
            ts["a"] = Column(vals)
        elif col_type == "mcol":  # MaskedColumn
            ts["a"] = MaskedColumn(vals, mask=False)
            ts["a"].mask[2] = True  # some value masked
        elif col_type == "qty":  # Quantity
            ts["a"] = vals * u.dimensionless_unscaled
        elif col_type == "mqty":  # MaskedQuantity
            ts["a"] = Masked(vals * u.dimensionless_unscaled)
            ts["a"].mask[2] = True  # some value masked
        else:
            raise ValueError(f"Unsupported col_type: {col_type}")

        self.ts = ts

    # FIXME: for case MaskedQuantity with np.add,
    # it hits the known issue in astropy/utils/masked/core.py
    #   NotImplementedError: masked instances cannot yet deal with 'reduceat' or 'at'.
    # tracked at the meta-issue  https://github.com/astropy/astropy/issues/11539
    @skip_for_params(
        [
            ("mqty", np.add),
        ]
    )
    def time_aggregate_downsample(self, col_type, aggregate_func):
        aggregate_downsample(
            self.ts, time_bin_size=5 * u.d, aggregate_func=aggregate_func
        )
