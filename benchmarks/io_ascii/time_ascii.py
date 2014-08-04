from astropy.io import ascii
try:
    from cStringIO import StringIO
    BytesIO = StringIO
except ImportError:
    from io import StringIO, BytesIO
import io


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
        with io.open('benchmarks/io_ascii/files/{}/{}.txt'.format(
                self.file_format, self.data_type), 'rb') as f:
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
    time_read = _ASCIISuite.read
    time_write = _ASCIISuite.write


class CsvInt(_ASCIISuite):
    file_format = 'csv'
    data_type = 'int'
    time_read = _ASCIISuite.read
    time_write = _ASCIISuite.write


class CsvFloat(_ASCIISuite):
    file_format = 'csv'
    data_type = 'float'
    time_read = _ASCIISuite.read
    time_write = _ASCIISuite.write


class RdbString(_ASCIISuite):
    file_format = 'rdb'
    data_type = 'string'
    time_read = _ASCIISuite.read
    time_write = _ASCIISuite.write


class RdbInt(_ASCIISuite):
    file_format = 'rdb'
    data_type = 'int'
    time_read = _ASCIISuite.read
    time_write = _ASCIISuite.write


class RdbFloat(_ASCIISuite):
    file_format = 'rdb'
    data_type = 'float'
    time_read = _ASCIISuite.read
    time_write = _ASCIISuite.write


class FixedWidthString(_ASCIISuite):
    file_format = 'fixed_width'
    data_type = 'string'
    time_read = _ASCIISuite.read
    time_write = _ASCIISuite.write


class FixedWidthInt(_ASCIISuite):
    file_format = 'fixed_width'
    data_type = 'int'
    time_read = _ASCIISuite.read
    time_write = _ASCIISuite.write


class FixedWidthFloat(_ASCIISuite):
    file_format = 'fixed_width'
    data_type = 'float'
    time_read = _ASCIISuite.read
    time_write = _ASCIISuite.write


class FixedWidthNoHeaderString(_ASCIISuite):
    file_format = 'fixed_width_no_header'
    data_type = 'string'
    time_read = _ASCIISuite.read
    time_write = _ASCIISuite.write


class FixedWidthNoHeaderInt(_ASCIISuite):
    file_format = 'fixed_width_no_header'
    data_type = 'int'
    time_read = _ASCIISuite.read
    time_write = _ASCIISuite.write


class FixedWidthNoHeaderFloat(_ASCIISuite):
    file_format = 'fixed_width_no_header'
    data_type = 'float'
    time_read = _ASCIISuite.read
    time_write = _ASCIISuite.write


class FixedWidthTwoLineString(_ASCIISuite):
    file_format = 'fixed_width_two_line'
    data_type = 'string'
    time_read = _ASCIISuite.read
    time_write = _ASCIISuite.write


class FixedWidthTwoLineInt(_ASCIISuite):
    file_format = 'fixed_width_two_line'
    data_type = 'int'
    time_read = _ASCIISuite.read
    time_write = _ASCIISuite.write


class FixedWidthTwoLineFloat(_ASCIISuite):
    file_format = 'fixed_width_two_line'
    data_type = 'float'
    time_read = _ASCIISuite.read
    time_write = _ASCIISuite.write


class TabString(_ASCIISuite):
    file_format = 'tab'
    data_type = 'string'
    time_read = _ASCIISuite.read
    time_write = _ASCIISuite.write


class TabInt(_ASCIISuite):
    file_format = 'tab'
    data_type = 'int'
    time_read = _ASCIISuite.read
    time_write = _ASCIISuite.write


class TabFloat(_ASCIISuite):
    file_format = 'tab'
    data_type = 'float'
    time_read = _ASCIISuite.read
    time_write = _ASCIISuite.write


class NoHeaderString(_ASCIISuite):
    file_format = 'no_header'
    data_type = 'string'
    time_read = _ASCIISuite.read
    time_write = _ASCIISuite.write


class NoHeaderInt(_ASCIISuite):
    file_format = 'no_header'
    data_type = 'int'
    time_read = _ASCIISuite.read
    time_write = _ASCIISuite.write


class NoHeaderFloat(_ASCIISuite):
    file_format = 'no_header'
    data_type = 'float'
    time_read = _ASCIISuite.read
    time_write = _ASCIISuite.write


class CommentedHeaderString(_ASCIISuite):
    file_format = 'commented_header'
    data_type = 'string'
    time_read = _ASCIISuite.read
    time_write = _ASCIISuite.write


class CommentedHeaderInt(_ASCIISuite):
    file_format = 'commented_header'
    data_type = 'int'
    time_read = _ASCIISuite.read
    time_write = _ASCIISuite.write


class CommentedHeaderFloat(_ASCIISuite):
    file_format = 'commented_header'
    data_type = 'float'
    time_read = _ASCIISuite.read
    time_write = _ASCIISuite.write


class BasicString(_ASCIISuite):
    file_format = 'basic'
    data_type = 'string'
    time_read = _ASCIISuite.read
    time_write = _ASCIISuite.write


class BasicInt(_ASCIISuite):
    file_format = 'basic'
    data_type = 'int'
    time_read = _ASCIISuite.read
    time_write = _ASCIISuite.write


class BasicFloat(_ASCIISuite):
    file_format = 'basic'
    data_type = 'float'
    time_read = _ASCIISuite.read
    time_write = _ASCIISuite.write


class SextractorString(_ASCIISuite):
    file_format = 'sextractor'
    data_type = 'string'
    time_read = _ASCIISuite.read


class SextractorInt(_ASCIISuite):
    file_format = 'sextractor'
    data_type = 'int'
    time_read = _ASCIISuite.read


class SextractorFloat(_ASCIISuite):
    file_format = 'sextractor'
    data_type = 'float'
    time_read = _ASCIISuite.read

class IpacString(_ASCIISuite):
    file_format = 'ipac'
    data_type = 'string'
    time_read = _ASCIISuite.read
    time_write = _ASCIISuite.write


class IpacInt(_ASCIISuite):
    file_format = 'ipac'
    data_type = 'int'
    time_read = _ASCIISuite.read
    time_write = _ASCIISuite.write


class IpacFloat(_ASCIISuite):
    file_format = 'ipac'
    data_type = 'float'
    time_read = _ASCIISuite.read
    time_write = _ASCIISuite.write


class LatexString(_ASCIISuite):
    file_format = 'latex'
    data_type = 'string'
    time_read = _ASCIISuite.read
    time_write = _ASCIISuite.write


class LatexInt(_ASCIISuite):
    file_format = 'latex'
    data_type = 'int'
    time_read = _ASCIISuite.read
    time_write = _ASCIISuite.write


class LatexFloat(_ASCIISuite):
    file_format = 'latex'
    data_type = 'float'
    time_read = _ASCIISuite.read
    time_write = _ASCIISuite.write


class AastexString(_ASCIISuite):
    file_format = 'aastex'
    data_type = 'string'
    time_read = _ASCIISuite.read
    time_write = _ASCIISuite.write


class AastexInt(_ASCIISuite):
    file_format = 'aastex'
    data_type = 'int'
    time_read = _ASCIISuite.read
    time_write = _ASCIISuite.write


class AastexFloat(_ASCIISuite):
    file_format = 'aastex'
    data_type = 'float'
    time_read = _ASCIISuite.read
    time_write = _ASCIISuite.write
