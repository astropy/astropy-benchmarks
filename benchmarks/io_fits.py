from io import BytesIO
from tempfile import mktemp

import numpy as np
from astropy.table import Table
from astropy.io import fits

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
        fits.BinTableHDU.from_columns(array)


def make_header(ncards=1000):
    cards = {'INT%d' % i: i for i in range(ncards)}
    cards.update({'FLT%d' % i: (i + i/10) for i in range(ncards)})
    cards.update({'STR%d' % i: 'VALUE %d' % i for i in range(ncards)})
    cards.update({'HIERARCH FOO BAR %d' % i: i for i in range(ncards)})
    return fits.Header(cards)


class FITSHeader:
    """
    Tests of the Header interface
    """

    def setup(self):
        self.hdr = make_header()
        self.hdr_string = self.hdr.tostring()

    def time_get_int(self):
        self.hdr.get('INT999')

    def time_get_float(self):
        self.hdr.get('FLT999')

    def time_get_str(self):
        self.hdr.get('STR999')

    def time_get_hierarch(self):
        self.hdr.get('HIERARCH FOO BAR 999')

    def time_tostring(self):
        self.hdr.tostring()

    def time_fromstring(self):
        fits.Header.fromstring(self.hdr_string)


class FITSHDUList:
    """
    Tests of the HDUList interface
    """

    def setup(self):
        self.filename = mktemp(suffix='.fits')
        hdr = make_header()
        hdul = fits.HDUList([fits.PrimaryHDU(header=hdr)] +
                            [fits.ImageHDU(header=hdr) for _ in range(100)])
        hdul.writeto(self.filename)

    def time_getheader(self):
        fits.getheader(self.filename)

    def time_getheader_ext50(self):
        fits.getheader(self.filename, ext=50)

    def time_len(self):
        with fits.open(self.filename) as hdul:
            len(hdul)
