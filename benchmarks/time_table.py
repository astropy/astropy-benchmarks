import string
import numpy as np

from astropy.table import Table, join, hstack, vstack


class TimeTable:

    masked = False

    def setup(self):

        # Initialize table
        self.table = Table(masked=self.masked)

        # Create column with mixed types
        np.random.seed(12345)
        self.table['i'] = np.arange(1000)
        self.table['a'] = np.random.random(1000)  # float
        self.table['b'] = np.random.random(1000) > 0.5  # bool
        self.table['c'] = np.random.random((1000,10))  # 2d column
        self.table['d'] = np.random.choice(np.array(list(string.ascii_letters)),1000)

        self.extra_row = {'a':1.2, 'b':True, 'c':np.repeat(1, 10), 'd': 'Z'}

        self.extra_column = np.random.randint(0, 100, 1000)

        self.row_indices = np.where(self.table['a'] > 0.9)[0]

        self.table_grouped = self.table.group_by('d')

        # Another table for testing joining
        self.other_table = Table(masked=self.masked)
        self.other_table['i'] = np.arange(1,1000,3)
        self.other_table['f'] = np.random.random()
        self.other_table.sort('f')

        # Another table for testing hstack
        self.other_table_2 = Table(masked=self.masked)
        self.other_table_2['g'] = np.random.random(1000)
        self.other_table_2['h'] = np.random.random((1000, 10))

        self.bool_mask = self.table['a'] > 0.6

    def time_table_slice_bool(self):
        table_subset = self.table[self.bool_mask]

    def time_table_slice_int(self):
        table_subset = self.table[self.row_indices]

    def time_column_slice_bool(self):
        col_subset = self.table['a'][self.bool_mask]

    def time_column_slice_int(self):
        col_subset = self.table['a'][self.row_indices]

    def time_column_get(self):
        self.table['c']

    def time_column_make_bool_mask(self):
        self.table['a'] > 0.6

    def time_multi_column_get(self):
        self.table[('a','c')]

    def time_column_set(self):
        self.table['a'] = 0.

    def time_column_set_all(self):
        self.table['b'][:] = True

    def time_column_set_row_subset(self):
        self.table['b'][self.bool_mask] = True

    def time_column_set_row_subset_int(self):
        self.table['b'][self.row_indices] = True

    def time_row_get(self):
        self.table[300]

    def time_iter_row(self):
        for row in self.table:
            pass

    def time_item_get_rowfirst(self):
        self.table[300]['b']

    def time_item_get_colfirst(self):
        self.table['b'][300]

    def time_add_row(self):
        self.table.add_row(self.extra_row)
    time_add_row.number = 1
    time_add_row.repeat = 1

    def time_remove_row(self):
        self.table.remove_row(6)
    time_remove_row.number = 1
    time_remove_row.repeat = 1

    def time_remove_rows(self):
        self.table.remove_rows(self.row_indices)
    time_remove_rows.number = 1
    time_remove_rows.repeat = 1

    def time_add_column(self):
        self.table['e'] = self.extra_column
    time_add_column.number = 1
    time_add_column.repeat = 1

    def time_remove_column(self):
        self.table.remove_column('a')
    time_remove_column.number = 1
    time_remove_column.repeat = 1

    def time_copy_table(self):
        self.table.copy()

    def time_copy_column(self):
        self.table['a'].copy()

    def time_group(self):
        self.table.group_by('d')

    def time_aggregate(self):
        # Test aggregate with a function that supports reduceat
        self.table_grouped.groups.aggregate(np.sum)

    def time_aggregate_noreduceat(self):
        # Test aggregate with a function that doesn't support reduceat
        self.table_grouped.groups.aggregate(lambda x: np.sum(x))

    def time_sort(self):
        self.table.sort('a')

    def time_join_inner(self):
        join(self.table, self.other_table, keys="i", join_type='inner')

    def time_join_outer(self):
        join(self.table, self.other_table, keys="i", join_type='outer')

    def time_hstack(self):
        hstack([self.table, self.other_table_2])

    def time_vstack(self):
        vstack([self.table, self.table])


class TimeMaskedTable(TimeTable):

    masked = True

    def time_mask_column(self):
        self.table['a'].mask = self.bool_mask
