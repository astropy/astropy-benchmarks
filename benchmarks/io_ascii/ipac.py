import os

from astropy.io import ascii
from astropy.io.ascii.ipac import Ipac

HERE = os.path.abspath(os.path.dirname(__file__))


class IPACSuite:
    def setup(self):
        self.vals = [str(i + 1) for i in range(1000)]
        self.widths = [i + 1 for i in range(1000)]
        f = open(os.path.join(HERE, "files", "ipac", "string.txt"))
        self.lines = f.read().split("\n")
        f.close()
        self.table = ascii.read(
            os.path.join(HERE, "files", "ipac", "string.txt"),
            format="ipac",
            guess=False,
        )
        self.reader = Ipac()
        self.header = self.reader.header
        self.data = self.reader.data
        self.splitter = self.reader.data.splitter
        self.header.cols = list(self.table.columns.values())
        self.data.cols = list(self.table.columns.values())
        self.data._set_fill_values(self.data.cols)

    # pytest compat
    setup_method = setup

    def time_splitter(self):
        self.splitter.join(self.vals, self.widths)

    def time_get_cols(self):
        self.header.get_cols(self.lines)

    def time_header_str_vals(self):
        self.header.str_vals()

    def time_data_str_vals(self):
        self.data.str_vals()
