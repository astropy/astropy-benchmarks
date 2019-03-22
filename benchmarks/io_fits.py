from io import BytesIO

import numpy as np
from astropy.table import Table
from astropy.io.fits import BinTableHDU, Header

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


class FITSHeader:
    """
    Tests of the Header interface
    """

    def setup(self):
        cards = {'INT%d' % i: i for i in range(1000)}
        cards.update({'FLT%d' % i: (i + i/10) for i in range(1000)})
        cards.update({'STR%d' % i: 'VALUE %d' % i for i in range(1000)})
        cards.update({'HIERARCH FOO BAR %d' % i: i for i in range(1000)})
        self.hdr = Header(cards)

    def time_get_int(self):
        self.hdr.get('INT999')

    def time_get_float(self):
        self.hdr.get('FLT999')

    def time_get_str(self):
        self.hdr.get('STR999')

    def time_get_hierarch(self):
        self.hdr.get('HIERARCH FOO BAR 999')
