from io import BytesIO
from tempfile import NamedTemporaryFile

import numpy as np
from astropy.io import fits
from astropy.table import Table

# Note that we use BytesIO here to avoid being sensitive to disk access times


class FITSHighLevelTableBenchmarks:
    """
    Tests of the Table I/O interface
    """

    def setup(self):
        rng = np.random.default_rng(01337)
        N_1mil = 1_000_000
        N_2mil = 2_000_000

        with NamedTemporaryFile(delete=False) as temp:
            self.table_file = temp.name
            t = Table()
            t["floats"] = rng.random(N_2mil)
            t["ints"] = rng.integers(low=0, high=100, size=N_2mil)
            t["strings"] = b"some strings"
            t["booleans"] = t["floats"] > 0.5
            t.write(temp, format="fits")

        self.out_t = Table()
        self.out_t["floats"] = rng.random(N_1mil)
        self.out_t["ints"] = rng.integers(low=0, high=100, size=N_1mil)
        self.out_t["strings"] = b"some strings"
        self.out_t["booleans"] = self.out_t["floats"] > 0.5

    def time_read_nommap(self):
        try:
            Table.read(self.table_file, format="fits", memmap=False)
        except TypeError:
            Table.read(self.table_file, format="fits")

    def time_write(self):
        table_bytes = BytesIO()
        self.out_t.write(table_bytes, format="fits")


class FITSBinTableHDU:
    def setup(self):
        x = np.repeat(b"a", 2_000_000)
        self.array = np.array(x, dtype=[("col", "S1")])

    def time_from_columns_bytes(self):
        fits.BinTableHDU.from_columns(self.array)


def make_header(ncards=1000):
    cards = {"INT%d" % i: i for i in range(ncards)}
    cards.update({"FLT%d" % i: (i + i / 10) for i in range(ncards)})
    cards.update({"STR%d" % i: "VALUE %d" % i for i in range(ncards)})
    cards.update({"HIERARCH FOO BAR %d" % i: i for i in range(ncards)})
    return fits.Header(cards)


class FITSHeader:
    """
    Tests of the Header interface
    """

    def setup(self):
        self.hdr = make_header()
        self.hdr_string = self.hdr.tostring()

    def time_get_int(self):
        self.hdr.get("INT999")

    def time_get_float(self):
        self.hdr.get("FLT999")

    def time_get_str(self):
        self.hdr.get("STR999")

    def time_get_hierarch(self):
        self.hdr.get("HIERARCH FOO BAR 999")

    def time_tostring(self):
        self.hdr.tostring()

    def time_fromstring(self):
        fits.Header.fromstring(self.hdr_string)


class FITSHDUList:
    """
    Tests of the HDUList interface
    """

    filename = "many_hdu.fits"

    def setup_cache(self):
        hdr = make_header()
        hdul = fits.HDUList(
            [fits.PrimaryHDU(header=hdr)]
            + [fits.ImageHDU(header=hdr) for _ in range(30)]
        )
        hdul.writeto(self.filename)

    def time_getheader(self):
        fits.getheader(self.filename)

    def time_getheader_ext50(self):
        fits.getheader(self.filename, ext=20)

    def time_len(self):
        with fits.open(self.filename) as hdul:
            len(hdul)
