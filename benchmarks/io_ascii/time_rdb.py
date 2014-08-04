from astropy.io.ascii import basic

class RDBSuite:
    def setup(self):
        self.header = basic.RdbHeader()
        self.header.splitter.delimiter = '\t'
        f = open('benchmarks/io_ascii/files/rdb/string.txt')
        self.lines = f.read().split('\n')
        f.close()
    def time_get_cols(self):
        self.header.get_cols(self.lines)
