"""Benchmarks for VOTable binary/binary2 parsing performance."""
import io
import numpy as np
from astropy.io.votable import parse, from_table
from astropy.table import Table

np.random.seed(42)

SMALL_SIZE = 1000
LARGE_SIZE = 200000

ra_data = np.random.uniform(0, 360, LARGE_SIZE).astype(np.float32)
dec_data = np.random.uniform(-90, 90, LARGE_SIZE).astype(np.float32)
mag_data = np.random.uniform(10, 25, LARGE_SIZE).astype(np.float32)
flux_data = np.random.lognormal(0, 2, LARGE_SIZE)
count_data = np.random.poisson(100, LARGE_SIZE).astype(np.int32)
id_data = np.arange(LARGE_SIZE, dtype=np.int64)
flag_data = np.random.choice([True, False], LARGE_SIZE)
quality_data = np.random.randint(0, 256, LARGE_SIZE, dtype=np.uint8)
bool_data = np.random.randint(0, 2, LARGE_SIZE).astype(bool)

short_names = np.array([f"OBJ_{i:08d}" for i in range(LARGE_SIZE)])
filter_names = np.random.choice(["u", "g", "r", "i", "z", "Y"], LARGE_SIZE)
classifications = np.random.choice(
    ["STAR", "GALAXY", "QSO", "UNKNOWN"], LARGE_SIZE)
long_descriptions = np.array(
    [
        f"Extend description about a field {i // 1000:04d}"
        for i in range(LARGE_SIZE)
    ]
)


def create_votable_bytes(
        table_data,
        format_type="binary2",
        bitarray_size=None):
    """Helper to create VOTables with a specific serialization."""
    votable = from_table(table_data)

    if bitarray_size is not None:
        first_table = votable.get_first_table()
        for field in first_table.fields:
            if field.datatype == "bit":
                field.arraysize = str(bitarray_size)

    output = io.BytesIO()
    votable.to_xml(output, tabledata_format=format_type)
    return output.getvalue()


class TimeVOTableNumeric:
    """Benchmark purely numeric fields."""

    def setup(self):
        table = Table(
            [
                ra_data[:LARGE_SIZE],
                dec_data[:LARGE_SIZE],
                mag_data[:LARGE_SIZE],
                flux_data[:LARGE_SIZE],
                count_data[:LARGE_SIZE],
                id_data[:LARGE_SIZE],
                quality_data[:LARGE_SIZE],
            ],
            names=["ra", "dec", "mag", "flux", "counts", "id", "quality"],
        )

        self.binary_data = create_votable_bytes(
            table, "binary", bitarray_size=8)
        self.binary2_data = create_votable_bytes(
            table, "binary2", bitarray_size=8)

    def time_numeric_binary(self):
        parse(io.BytesIO(self.binary_data))

    def time_numeric_binary2(self):
        parse(io.BytesIO(self.binary2_data))


class TimeVOTableShortStrings:
    """Benchmark short-length strings."""

    def setup(self):
        table = Table(
            [
                ra_data[:LARGE_SIZE],
                dec_data[:LARGE_SIZE],
                short_names[:LARGE_SIZE],
                filter_names[:LARGE_SIZE],
                classifications[:LARGE_SIZE],
                mag_data[:LARGE_SIZE],
            ],
            names=["ra", "dec", "object_id", "filter", "class", "mag"],
        )

        self.binary_data = create_votable_bytes(table, "binary")
        self.binary2_data = create_votable_bytes(table, "binary2")

    def time_short_strings_binary(self):
        parse(io.BytesIO(self.binary_data))

    def time_short_strings_binary2(self):
        parse(io.BytesIO(self.binary2_data))


class TimeVOTableLongStrings:
    """Benchmark long variable-length strings."""

    def setup(self):
        table = Table(
            [
                ra_data[:LARGE_SIZE],
                dec_data[:LARGE_SIZE],
                long_descriptions[:LARGE_SIZE],
                mag_data[:LARGE_SIZE],
            ],
            names=["ra", "dec", "description", "mag"],
        )

        self.binary_data = create_votable_bytes(table, "binary")
        self.binary2_data = create_votable_bytes(table, "binary2")

    def time_long_strings_binary(self):
        parse(io.BytesIO(self.binary_data))

    def time_long_strings_binary2(self):
        parse(io.BytesIO(self.binary2_data))


class TimeVOTableStringIntensive:
    """Benchmark table with string fields of various lengths."""

    def setup(self):
        table = Table(
            [
                short_names[:LARGE_SIZE],
                filter_names[:LARGE_SIZE],
                classifications[:LARGE_SIZE],
                np.random.choice(["A", "B", "C", "D"], LARGE_SIZE),
                np.random.choice(["HIGH", "MED", "LOW"], LARGE_SIZE),
                long_descriptions[:LARGE_SIZE],
                ra_data[:LARGE_SIZE],
                dec_data[:LARGE_SIZE],
            ],
            names=[
                "id",
                "filter",
                "class",
                "grade",
                "priority",
                "desc",
                "ra",
                "dec",
            ],
        )

        self.binary2_data = create_votable_bytes(table, "binary2")

    def time_string_intensive_binary2(self):
        parse(io.BytesIO(self.binary2_data))


class TimeVOTableBooleanFields:
    """Benchmark boolean/bit fields specifically."""

    def setup(self):
        table = Table(
            [
                ra_data[:LARGE_SIZE],
                dec_data[:LARGE_SIZE],
                np.random.choice([True, False], LARGE_SIZE),
                np.random.choice([True, False], LARGE_SIZE),
                np.random.choice([True, False], LARGE_SIZE),
                np.random.choice([True, False], LARGE_SIZE),
                np.random.choice([True, False], LARGE_SIZE),
                np.random.choice([True, False], LARGE_SIZE),
                np.random.choice([True, False], LARGE_SIZE),
                np.random.choice([True, False], LARGE_SIZE),
            ],
            names=[
                "ra",
                "dec",
                "saturated",
                "flagged",
                "edge_pixel",
                "cosmic_ray",
                "variable",
                "extended",
                "public",
                "calibrated",
            ],
        )

        self.binary_data = create_votable_bytes(table, "binary")
        self.binary2_data = create_votable_bytes(table, "binary2")

    def time_booleans_binary(self):
        parse(io.BytesIO(self.binary_data))

    def time_booleans_binary2(self):
        parse(io.BytesIO(self.binary2_data))


class TimeVOTableBitArrayOptimization:
    """Benchmark BitArray columns in Binary/Binary2 VOTables."""

    def setup(self):
        table = Table(
            [
                ra_data[:LARGE_SIZE],
                dec_data[:LARGE_SIZE],
                mag_data[:LARGE_SIZE],
                np.random.randint(0, 2, LARGE_SIZE).astype(bool),
                np.random.randint(0, 2, LARGE_SIZE).astype(bool),
                np.random.randint(0, 2, LARGE_SIZE).astype(bool),
                np.random.randint(0, 2, LARGE_SIZE).astype(bool),
            ],
            names=[
                "ra",
                "dec",
                "mag",
                "detected",
                "saturated",
                "edge_pixel",
                "cosmic_ray",
            ],
        )

        self.binary_bitarray_8_data = create_votable_bytes(
            table, "binary", "8")
        self.binary_bitarray_16_data = create_votable_bytes(
            table, "binary", "16")
        self.binary2_bitarray_8_data = create_votable_bytes(
            table, "binary2", "8")
        self.binary2_bitarray_16_data = create_votable_bytes(
            table, "binary2", "16")

    def time_bitarray_8bit_binary(self):
        """Parse BitArray with 8-bit arraysize."""
        parse(io.BytesIO(self.binary_bitarray_8_data))

    def time_bitarray_16bit_binary(self):
        """Parse BitArray with 16-bit arraysize."""
        parse(io.BytesIO(self.binary_bitarray_16_data))

    def time_bitarray_8bit_binary2(self):
        """Parse binary2 BitArray with 8-bit arraysize."""
        parse(io.BytesIO(self.binary2_bitarray_8_data))

    def time_bitarray_16bit_binary2(self):
        """Parse binary2 BitArray with 16-bit arraysize."""
        parse(io.BytesIO(self.binary2_bitarray_16_data))


class TimeVOTableMixed:
    """Benchmark for a table with mixed fields types."""

    def setup(self):
        table = Table(
            [
                ra_data[:LARGE_SIZE],
                dec_data[:LARGE_SIZE],
                short_names[:LARGE_SIZE],
                mag_data[:LARGE_SIZE],
                flux_data[:LARGE_SIZE],
                filter_names[:LARGE_SIZE],
                classifications[:LARGE_SIZE],
                count_data[:LARGE_SIZE],
                quality_data[:LARGE_SIZE],
                flag_data[:LARGE_SIZE],
            ],
            names=[
                "ra",
                "dec",
                "id",
                "mag",
                "flux",
                "filter",
                "class",
                "counts",
                "quality",
                "detected",
            ],
        )

        self.binary_data = create_votable_bytes(table, "binary")
        self.binary2_data = create_votable_bytes(table, "binary2")

    def time_mixed_binary(self):
        parse(io.BytesIO(self.binary_data))

    def time_mixed_binary2(self):
        parse(io.BytesIO(self.binary2_data))


class TimeVOTableSmallOverhead:
    """Measure parsing overhead with small tables."""

    def setup(self):
        table = Table(
            [
                ra_data[:SMALL_SIZE],
                dec_data[:SMALL_SIZE],
                mag_data[:SMALL_SIZE],
            ],
            names=["ra", "dec", "mag"],
        )

        self.binary_data = create_votable_bytes(table, "binary")
        self.binary2_data = create_votable_bytes(table, "binary2")

    def time_small_binary(self):
        parse(io.BytesIO(self.binary_data))

    def time_small_binary2(self):
        parse(io.BytesIO(self.binary2_data))
