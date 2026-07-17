"""Benchmarks for writing ECSV files.

Modelled on a Gaia archive query result, since saving a catalog query to ECSV is
a common way to keep it. Dtypes and null fractions follow gaiadr3.gaia_source.
How the table was obtained decides which path the writer takes: via astroquery
(i.e. VOTable) every column is a MaskedColumn, even ones with no nulls, whereas
a FITS download only masks columns that have nulls and gives bytes strings.
"""

import io

import numpy as np
from astropy.table import Column, MaskedColumn, Table

N = 20_000
rng = np.random.default_rng(42)

source_ids = rng.integers(4_295_806_720, 6_917_528_997_577_384_320, N, dtype=np.int64)

# name, data, fraction missing in DR3
GAIA_SOURCE = [
    ("source_id", source_ids, 0.0),
    ("designation", np.array([f"Gaia DR3 {s}" for s in source_ids]), 0.0),
    ("ra", rng.uniform(0, 360, N), 0.0),
    ("dec", rng.uniform(-90, 90, N), 0.0),
    ("astrometric_n_obs_al", rng.integers(50, 500, N, dtype=np.int16), 0.0),
    ("parallax", rng.normal(1, 2, N), 0.19),  # 2-parameter sources have none
    ("parallax_error", rng.lognormal(-2, 1, N).astype("f4"), 0.19),
    ("pmra", rng.normal(0, 10, N), 0.19),
    ("pmdec", rng.normal(0, 10, N), 0.19),
    ("ruwe", rng.normal(1, 0.2, N).astype("f4"), 0.19),
    ("phot_g_mean_mag", rng.uniform(3, 21, N).astype("f4"), 0.003),
    ("bp_rp", rng.normal(1, 0.8, N).astype("f4"), 0.15),
    ("radial_velocity", rng.normal(0, 40, N), 0.98),
    ("teff_gspphot", rng.uniform(3000, 10000, N).astype("f4"), 0.74),
    ("phot_variable_flag", rng.choice(["NOT_AVAILABLE", "VARIABLE"], N), 0.0),
    ("has_xp_continuous", rng.random(N) < 0.12, 0.0),
]

MASKS = {name: rng.random(N) < fraction for name, _, fraction in GAIA_SOURCE}


def write_ecsv_to_in_memory_buffer(table):
    table.write(io.StringIO(), format="ascii.ecsv")


class ECSVWriteGaiaSource:
    def setup(self):
        # As returned by astroquery.gaia
        self.table_with_all_masked_cols = Table(
            [MaskedColumn(d, name=n, mask=MASKS[n]) for n, d, _ in GAIA_SOURCE]
        )
        # As read back from a FITS download; masked columns iff nulls
        self.fits_table = Table(
            [
                (
                    MaskedColumn(d, name=n, mask=MASKS[n])
                    if MASKS[n].any()
                    else Column(d.astype("S") if d.dtype.kind == "U" else d, name=n)
                )
                for n, d, _ in GAIA_SOURCE
            ]
        )
        # Built by hand from arrays, or put through Table.filled()
        self.unmasked_table = Table([Column(d, name=n) for n, d, _ in GAIA_SOURCE])

    def time_write(self):
        write_ecsv_to_in_memory_buffer(self.table_with_all_masked_cols)

    def time_write_from_fits(self):
        write_ecsv_to_in_memory_buffer(self.fits_table)

    def time_write_unmasked(self):
        write_ecsv_to_in_memory_buffer(self.unmasked_table)


class ECSVWriteGaiaXpSpectra:
    """Array-valued columns (BP/RP spectra) are written as JSON, not str()."""

    def setup(self):
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
