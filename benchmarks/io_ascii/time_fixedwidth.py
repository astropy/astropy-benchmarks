from astropy.io import ascii

class FixedWidthSuite:
    def setup(self):
        self.header = ascii.FixedWidthHeader()
        self.header.start_line = 0
        self.header.col_starts = None
        self.header.col_ends = None
        self.splitter = ascii.FixedWidthSplitter()
        f = open('benchmarks/io_ascii/files/fixed_width/string.txt')
        self.lines = f.read().split('\n')
        f.close()
        self.header.get_cols(self.lines)
        self.splitter.cols = self.header.cols
        self.data = ascii.FixedWidthData()
    def time_splitter(self):
        self.splitter(self.lines[1:])
    def time_header(self):
        self.header.get_cols(self.lines)
