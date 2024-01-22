import string
import numpy as np

from astropy.table import Table, MaskedColumn, join, hstack, vstack


class TimeTable:
    masked = False

    def setup(self):
        # Initialize table
        self.table = Table(masked=self.masked)

        # Create column with mixed types
        np.random.seed(12345)
        self.table["i"] = np.arange(1000)
        self.table["a"] = np.random.random(1000)  # float
        self.table["b"] = np.random.random(1000) > 0.5  # bool
        self.table["c"] = np.random.random((1000, 10))  # 2d column
        self.table["d"] = np.random.choice(np.array(list(string.ascii_letters)), 1000)

        self.np_table = np.array(self.table)

        self.extra_row = {"a": 1.2, "b": True, "c": np.repeat(1, 10), "d": "Z"}

        self.extra_column = np.random.randint(0, 100, 1000)

        self.row_indices = np.where(self.table["a"] > 0.9)[0]

        self.table_grouped = self.table.group_by("d")

        # Another table for testing joining
        self.other_table = Table(masked=self.masked)
        self.other_table["i"] = np.arange(1, 1000, 3)
        self.other_table["f"] = np.random.random()
        self.other_table.sort("f")

        # Another table for testing hstack
        self.other_table_2 = Table(masked=self.masked)
        self.other_table_2["g"] = np.random.random(1000)
        self.other_table_2["h"] = np.random.random((1000, 10))

        self.bool_mask = self.table["a"] > 0.6

    def time_table_slice_bool(self):
        self.table[self.bool_mask]

    def time_table_slice_int(self):
        self.table[self.row_indices]

    def time_column_slice_bool(self):
        self.table["a"][self.bool_mask]

    def time_column_slice_int(self):
        self.table["a"][self.row_indices]

    def time_column_get(self):
        self.table["c"]

    def time_column_make_bool_mask(self):
        self.table["a"] > 0.6

    def time_multi_column_get(self):
        self.table[("a", "c")]

    def time_column_set(self):
        self.table["a"] = 0.0

    def time_column_set_all(self):
        self.table["b"][:] = True

    def time_column_set_row_subset(self):
        self.table["b"][self.bool_mask] = True

    def time_column_set_row_subset_int(self):
        self.table["b"][self.row_indices] = True

    def time_row_get(self):
        self.table[300]

    def time_iter_row(self):
        for row in self.table:
            pass

    def time_read_rows(self):
        for row in self.table:
            tuple(row)

    def time_item_get_rowfirst(self):
        self.table[300]["b"]

    def time_item_get_colfirst(self):
        self.table["b"][300]

    def time_add_row(self):
        self.table.add_row(self.extra_row)

    def time_add_column(self):
        self.table["e"] = self.extra_column

    def time_init_from_np_array_no_copy(self):
        Table(self.np_table, copy=False)

    def time_init_from_np_array_copy(self):
        Table(self.np_table, copy=True)

    def time_copy_table(self):
        self.table.copy()

    def time_copy_column(self):
        self.table["a"].copy()

    def time_group(self):
        self.table.group_by("d")

    def time_aggregate(self):
        # Test aggregate with a function that supports reduceat
        self.table_grouped.groups.aggregate(np.sum)

    def time_aggregate_noreduceat(self):
        # Test aggregate with a function that doesn't support reduceat
        self.table_grouped.groups.aggregate(lambda x: np.sum(x))

    def time_sort(self):
        self.table.sort("a")

    def time_join_inner(self):
        join(self.table, self.other_table, keys="i", join_type="inner")

    def time_join_outer(self):
        join(self.table, self.other_table, keys="i", join_type="outer")

    def time_hstack(self):
        hstack([self.table, self.other_table_2])

    def time_vstack(self):
        vstack([self.table, self.table])


class TimeMaskedTable(TimeTable):
    masked = True

    def time_mask_column(self):
        self.table["a"].mask = self.bool_mask


class TimeMaskedColumn:
    def setup(self):
        self.dat = np.arange(1e7)

    def time_masked_column_init(self):
        MaskedColumn(self.dat)


class TimeTableInitWithLists:
    def setup(self):
        self.dat = list(range(100_000))

    def time_init_lists(self):
        Table([self.dat, self.dat, self.dat], names=["time", "rate", "error"])


class TimeTableInitWithMultiDimLists:
    def setup(self):
        np_data_int = np.arange(1_000_000, dtype=np.int64)
        np_data_float = np_data_int.astype(np.float64)
        np_data_str = np_data_int.astype("U")

        self.data_int_1d = np_data_int.tolist()

        self.data_int_3d = np_data_int.reshape(1000, 100, 10).tolist()

        self.data_int_masked_1d = self.data_int_1d.copy()
        self.data_int_masked_1d[-1] = np.ma.masked

        self.data_int_masked_3d = self.data_int_3d.copy()
        self.data_int_masked_3d[-1][-1][-1] = np.ma.masked

        self.data_float_1d = np_data_float.tolist()

        self.data_str_1d = np_data_str.tolist()

        self.data_str_masked_1d = self.data_str_1d.copy()
        self.data_str_masked_1d[-1] = np.ma.masked

    def time_init_int_1d(self):
        Table([self.data_int_1d])

    def time_init_int_3d(self):
        Table([self.data_int_3d])

    def time_init_int_masked_1d(self):
        Table([self.data_int_masked_1d])

    def time_init_int_masked_3d(self):
        Table([self.data_int_masked_3d])

    def time_init_float_1d(self):
        Table([self.data_float_1d])

    def time_init_str_1d(self):
        Table([self.data_str_1d])

    def time_init_str_masked_1d(self):
        Table([self.data_str_masked_1d])
