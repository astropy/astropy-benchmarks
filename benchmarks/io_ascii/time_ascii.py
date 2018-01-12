import os

from astropy.io import ascii
try:
    from cStringIO import StringIO
    BytesIO = StringIO
except ImportError:
    from io import StringIO, BytesIO
import io


HERE = os.path.abspath(os.path.dirname(__file__))


class _ASCIISuite:
    def setup(self):
        self.tables = {}
        self.data = {}
        self.output = StringIO()
        self.writers = {
            'csv': ascii.Csv,
            'rdb': ascii.Rdb,
            'fixed_width': ascii.FixedWidth,
            'fixed_width_no_header': ascii.FixedWidthNoHeader,
            'fixed_width_two_line': ascii.FixedWidthTwoLine,
            'tab': ascii.Tab,
            'no_header': ascii.NoHeader,
            'commented_header': ascii.CommentedHeader,
            'basic': ascii.Basic,
            'ipac': ascii.Ipac,
            'latex': ascii.Latex,
            'aastex': ascii.AASTex
            }
        with io.open(os.path.join(HERE, 'files', self.file_format, '{0}.txt'.format(self.data_type)), 'rb') as f:
            self.data = f.read()
        if self.file_format != 'sextractor':
            self.table = self.read()

    def read(self):
        return ascii.read(BytesIO(self.data), format=self.file_format, guess=False)

    def write(self):
        ascii.write(self.table, self.output, Writer=self.writers[self.file_format])


class CsvString(_ASCIISuite):
    file_format = 'csv'
    data_type = 'string'

    def time_read(self):
        return self.read()

    def time_write(self):
        return self.write()


class CsvInt(_ASCIISuite):
    file_format = 'csv'
    data_type = 'int'

    def time_read(self):
        return self.read()

    def time_write(self):
        return self.write()


class CsvFloat(_ASCIISuite):
    file_format = 'csv'
    data_type = 'float'

    def time_read(self):
        return self.read()

    def time_write(self):
        return self.write()


class RdbString(_ASCIISuite):
    file_format = 'rdb'
    data_type = 'string'

    def time_read(self):
        return self.read()

    def time_write(self):
        return self.write()


class RdbInt(_ASCIISuite):
    file_format = 'rdb'
    data_type = 'int'

    def time_read(self):
        return self.read()

    def time_write(self):
        return self.write()


class RdbFloat(_ASCIISuite):
    file_format = 'rdb'
    data_type = 'float'

    def time_read(self):
        return self.read()

    def time_write(self):
        return self.write()


class FixedWidthString(_ASCIISuite):
    file_format = 'fixed_width'
    data_type = 'string'

    def time_read(self):
        return self.read()

    def time_write(self):
        return self.write()


class FixedWidthInt(_ASCIISuite):
    file_format = 'fixed_width'
    data_type = 'int'

    def time_read(self):
        return self.read()

    def time_write(self):
        return self.write()


class FixedWidthFloat(_ASCIISuite):
    file_format = 'fixed_width'
    data_type = 'float'

    def time_read(self):
        return self.read()

    def time_write(self):
        return self.write()


class FixedWidthNoHeaderString(_ASCIISuite):
    file_format = 'fixed_width_no_header'
    data_type = 'string'

    def time_read(self):
        return self.read()

    def time_write(self):
        return self.write()


class FixedWidthNoHeaderInt(_ASCIISuite):
    file_format = 'fixed_width_no_header'
    data_type = 'int'

    def time_read(self):
        return self.read()

    def time_write(self):
        return self.write()


class FixedWidthNoHeaderFloat(_ASCIISuite):
    file_format = 'fixed_width_no_header'
    data_type = 'float'

    def time_read(self):
        return self.read()

    def time_write(self):
        return self.write()


class FixedWidthTwoLineString(_ASCIISuite):
    file_format = 'fixed_width_two_line'
    data_type = 'string'

    def time_read(self):
        return self.read()

    def time_write(self):
        return self.write()


class FixedWidthTwoLineInt(_ASCIISuite):
    file_format = 'fixed_width_two_line'
    data_type = 'int'

    def time_read(self):
        return self.read()

    def time_write(self):
        return self.write()


class FixedWidthTwoLineFloat(_ASCIISuite):
    file_format = 'fixed_width_two_line'
    data_type = 'float'

    def time_read(self):
        return self.read()

    def time_write(self):
        return self.write()


class TabString(_ASCIISuite):
    file_format = 'tab'
    data_type = 'string'

    def time_read(self):
        return self.read()

    def time_write(self):
        return self.write()


class TabInt(_ASCIISuite):
    file_format = 'tab'
    data_type = 'int'

    def time_read(self):
        return self.read()

    def time_write(self):
        return self.write()


class TabFloat(_ASCIISuite):
    file_format = 'tab'
    data_type = 'float'

    def time_read(self):
        return self.read()

    def time_write(self):
        return self.write()


class NoHeaderString(_ASCIISuite):
    file_format = 'no_header'
    data_type = 'string'

    def time_read(self):
        return self.read()

    def time_write(self):
        return self.write()


class NoHeaderInt(_ASCIISuite):
    file_format = 'no_header'
    data_type = 'int'

    def time_read(self):
        return self.read()

    def time_write(self):
        return self.write()


class NoHeaderFloat(_ASCIISuite):
    file_format = 'no_header'
    data_type = 'float'

    def time_read(self):
        return self.read()

    def time_write(self):
        return self.write()


class CommentedHeaderString(_ASCIISuite):
    file_format = 'commented_header'
    data_type = 'string'

    def time_read(self):
        return self.read()

    def time_write(self):
        return self.write()


class CommentedHeaderInt(_ASCIISuite):
    file_format = 'commented_header'
    data_type = 'int'

    def time_read(self):
        return self.read()

    def time_write(self):
        return self.write()


class CommentedHeaderFloat(_ASCIISuite):
    file_format = 'commented_header'
    data_type = 'float'

    def time_read(self):
        return self.read()

    def time_write(self):
        return self.write()


class BasicString(_ASCIISuite):
    file_format = 'basic'
    data_type = 'string'

    def time_read(self):
        return self.read()

    def time_write(self):
        return self.write()


class BasicInt(_ASCIISuite):
    file_format = 'basic'
    data_type = 'int'

    def time_read(self):
        return self.read()

    def time_write(self):
        return self.write()


class BasicFloat(_ASCIISuite):
    file_format = 'basic'
    data_type = 'float'

    def time_read(self):
        return self.read()

    def time_write(self):
        return self.write()


class SextractorString(_ASCIISuite):
    file_format = 'sextractor'
    data_type = 'string'

    def time_read(self):
        return self.read()


class SextractorInt(_ASCIISuite):
    file_format = 'sextractor'
    data_type = 'int'

    def time_read(self):
        return self.read()


class SextractorFloat(_ASCIISuite):
    file_format = 'sextractor'
    data_type = 'float'

    def time_read(self):
        return self.read()


class IpacString(_ASCIISuite):
    file_format = 'ipac'
    data_type = 'string'

    def time_read(self):
        return self.read()

    def time_write(self):
        return self.write()


class IpacInt(_ASCIISuite):
    file_format = 'ipac'
    data_type = 'int'

    def time_read(self):
        return self.read()

    def time_write(self):
        return self.write()


class IpacFloat(_ASCIISuite):
    file_format = 'ipac'
    data_type = 'float'

    def time_read(self):
        return self.read()

    def time_write(self):
        return self.write()


class LatexString(_ASCIISuite):
    file_format = 'latex'
    data_type = 'string'

    def time_read(self):
        return self.read()

    def time_write(self):
        return self.write()


class LatexInt(_ASCIISuite):
    file_format = 'latex'
    data_type = 'int'

    def time_read(self):
        return self.read()

    def time_write(self):
        return self.write()


class LatexFloat(_ASCIISuite):
    file_format = 'latex'
    data_type = 'float'

    def time_read(self):
        return self.read()

    def time_write(self):
        return self.write()


class AastexString(_ASCIISuite):
    file_format = 'aastex'
    data_type = 'string'

    def time_read(self):
        return self.read()

    def time_write(self):
        return self.write()


class AastexInt(_ASCIISuite):
    file_format = 'aastex'
    data_type = 'int'

    def time_read(self):
        return self.read()

    def time_write(self):
        return self.write()


class AastexFloat(_ASCIISuite):
    file_format = 'aastex'
    data_type = 'float'

    def time_read(self):
        return self.read()

    def time_write(self):
        return self.write()
