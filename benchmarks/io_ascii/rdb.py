import os

from astropy.io.ascii import basic

HERE = os.path.abspath(os.path.dirname(__file__))


class RDBSuite:
    def setup(self):
        self.header = basic.RdbHeader()
        self.header.splitter.delimiter = "\t"
        f = open(os.path.join(HERE, "files", "rdb", "string.txt"))
        self.lines = f.read().split("\n")
        f.close()

    def time_get_cols(self):
        self.header.get_cols(self.lines)
