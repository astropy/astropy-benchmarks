from io import BytesIO

import numpy as np
from astropy.table import Table
from astropy.io.fits import BinTableHDU

# Note that we use BytesIO here to avoid being sensitive to disk access times


class FITSHighLevelTableBenchmarks:
    """
    Tests of the Table I/O interface
    """

    def setup(self):

        N = 2_000_000

        self.table_bytes = BytesIO()

        t = Table()
        t['floats'] = np.random.random(N)
        t['ints'] = np.random.randint(0, 100, N)
        t['strings'] = b'some strings'
        t['booleans'] = t['floats'] > 0.5
        t.write(self.table_bytes, format='fits')

    def time_read_nommap(self):
        self.table_bytes.seek(0)
        try:
            Table.read(self.table_bytes, format='fits', memmap=False)
        except TypeError:
            Table.read(self.table_bytes, format='fits')

    def time_write(self):
        N = 1_000_000
        table_bytes = BytesIO()
        t = Table()
        t['floats'] = np.random.random(N)
        t['ints'] = np.random.randint(0, 100, N)
        t['strings'] = b'some strings'
        t['booleans'] = t['floats'] > 0.5
        t.write(table_bytes, format='fits')


class FITSBinTableHDU:

    def time_from_columns_bytes(self):
        x = np.repeat(b'a', 2_000_000)
        array = np.array(x, dtype=[('col', 'S1')])
        BinTableHDU.from_columns(array)
