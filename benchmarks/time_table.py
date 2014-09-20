import string
import numpy as np

from astropy.table import Table


class TimeTable:

    def setup(self):

        # Initialize table
        self.table = Table()

        # Create column with mixed types
        np.random.seed(12345)
        self.table['a'] = np.random.random(1000)  # float
        self.table['b'] = np.random.random(1000) > 0.5  # bool
        self.table['c'] = np.random.random((1000,10))  # 2d column
        self.table['d'] = np.random.choice(np.array(list(string.ascii_letters)),1000)

        self.extra_row = {'a':1.2, 'b':True, 'c':np.repeat(1, 10), 'd': 'Z'}

        self.extra_column = np.random.randint(0, 100, 1000)

    def time_column_access(self):
        self.table['c']

    def time_row_access(self):
        self.table[300]

    def time_iter_row(self):
        for row in self.table:
            pass

    def time_add_row(self):
        self.table.add_row(self.extra_row)

    def time_add_column(self):
        self.table['e'] = self.extra_column
