from astropy.io import ascii
from astropy.io.ascii.ipac import IpacHeader, IpacHeaderSplitter, IpacData


class IPACSuite:
    def setup(self):
        self.header = IpacHeader()
        self.data = IpacData()
        self.header.data = self.data
        self.splitter = IpacHeaderSplitter()
        self.vals = [str(i + 1) for i in range(1000)]
        self.widths = [i + 1 for i in range(1000)]
        f = open('benchmarks/io_ascii/files/ipac/string.txt')
        self.lines = f.read().split('\n')
        f.close()
        self.table = ascii.read('benchmarks/io_ascii/files/ipac/string.txt',
                                format='ipac', guess=False)

    def time_splitter(self):
        self.splitter.join(self.vals, self.widths)

    def time_get_cols(self):
        self.header.get_cols(self.lines)

    def time_header_str_vals(self):
        header = IpacHeader()
        header.cols = list(self.table.columns.values())
        header.DBMS = False
        header.str_vals()

    def time_data_str_vals(self):
        data = IpacData()
        data.cols = list(self.table.columns.values())
        data.str_vals()
