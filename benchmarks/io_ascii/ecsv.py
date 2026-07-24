"""Benchmarks for writing ECSV files.

Covers core datatypes and table structures. One datatype per table
to help isolate potential regressions.
"""

import io

import numpy as np
from astropy.coordinates import SkyCoord
from astropy.table import Column, MaskedColumn, Table
from astropy.time import Time

N = 100_000
N_COLS = 4
MASK_STEP = 10

DATA = {
    "int": np.arange(N, dtype=np.int64),
    "float": np.linspace(0.0, 1.0, N),
    "bool": (np.arange(N) % 2) == 0,
    "string": np.array([f"str_{i:06d}" for i in range(N)], dtype="U10"),
}


def write_ecsv_to_in_memory_buffer(table):
    table.write(io.StringIO(), format="ascii.ecsv")


class ECSVWrite:
    params = (list(DATA.keys()), [False, True])
    param_names = ["dtype", "masked"]

    def setup(self, dtype, masked):
        data = DATA[dtype]
        if masked:
            mask = np.zeros(N, dtype=bool)
            mask[::MASK_STEP] = True
            columns = [
                MaskedColumn(data, mask=mask, name=f"col{i}") for i in range(N_COLS)
            ]
        else:
            columns = [Column(data, name=f"col{i}") for i in range(N_COLS)]
        self.table = Table(columns)

    def time_write(self, dtype, masked):
        write_ecsv_to_in_memory_buffer(self.table)


class ECSVWriteXpSpectra:
    """Array-valued columns (BP/RP spectra) are written as JSON, not str()."""

    def setup(self):
        rng = np.random.default_rng(42)
        coeffs = rng.normal(0, 1, (N // 10, 55))  # 2D
        self.table = Table([Column(coeffs, name="bp_coefficients")])
        self.masked_table = Table(
            [
                MaskedColumn(
                    coeffs, name="bp_coefficients", mask=rng.random(coeffs.shape) < 0.05
                )
            ]
        )

    def time_write(self):
        write_ecsv_to_in_memory_buffer(self.table)

    def time_write_masked(self):
        write_ecsv_to_in_memory_buffer(self.masked_table)


class ECSVWriteMixinColumns:
    """Mixin columns go through separate serialization machinery, not str_vals."""

    def setup(self):
        self.time_table = Table([Time(np.linspace(58000, 59000, N), format="mjd")], names=["t"])
        self.skycoord_table = Table(
            [SkyCoord(ra=np.linspace(0, 360, N), dec=np.linspace(-90, 90, N), unit="deg")],
            names=["c"],
        )

    def time_write_time(self):
        write_ecsv_to_in_memory_buffer(self.time_table)

    def time_write_skycoord(self):
        write_ecsv_to_in_memory_buffer(self.skycoord_table)
