from astropy import table
from astropy.io.ascii import core
try:
    from itertools import izip
except ImportError:
    izip = zip
import random
try:
    from string import uppercase
except ImportError:
    from string import ascii_uppercase as uppercase


class TableSuite:
    def setup(self):
        self.lst = []
        self.lst.append([random.randint(-500, 500) for i in range(1000)])
        self.lst.append([random.random() * 500 - 500 for i in range(1000)])
        self.lst.append([''.join([random.choice(uppercase) for j in
                            range(6)]) for i in range(1000)])
        self.cols = [core.Column(str(i + 1)) for i in range(3)]
        for col, x in izip(self.cols, self.lst):
            col.data = x
        self.table_cols = [table.Column(x) for x in self.lst]
        self.outputter = core.TableOutputter()
        self.table = table.Table()
    def time_table_outputter(self):
        self.outputter(self.cols, {'table': {}})
    def mem_table_outputter(self):
        return self.outputter(self.cols, {'table': {}})
    def time_str_vals_int(self):
        self.table_cols[0].iter_str_vals()
    def time_str_vals_float(self):
        self.table_cols[1].iter_str_vals()
    def time_str_vals_str(self):
        self.table_cols[2].iter_str_vals()
    def time_table_init_from_list(self):
        self.table._init_from_list(self.table_cols, ['1', '2', '3'],
                                   [None, None, None], 3, True)
    def mem_table_init(self):
        return table.Table(self.lst)
