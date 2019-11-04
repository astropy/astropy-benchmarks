import copy

import numpy as np
from astropy import units as u


# Unit tests

def time_unit_compose():
    u.Ry.compose()


def time_unit_to():
    u.m.to(u.pc)


def time_unit_parse():
    u.Unit('1e-07 kg m2 / s2')


def time_simple_unit_parse():
    u.Unit('1 d')


def time_very_simple_unit_parse():
    u.Unit('d')


def mem_unit():
    return u.erg


def time_compose_to_bases():
    x = copy.copy(u.Ry)
    x.cgs


def time_compose_complex():
    # Composing a complex unit can be very inefficient
    (u.kg / u.s ** 3 * u.au ** 2.5 / u.yr ** 0.5 / u.sr ** 2).compose()


# Quantity tests

a = np.arange(100000.)
b1 = [1., 2., 3.]
b2 = np.asarray(b1)
q0 = u.Quantity(1., u.s)
q1 = u.Quantity(a, u.m)
q2 = u.Quantity(a[:10000], u.deg)


def time_quantity_creation():
    u.Quantity(a, u.m)


def time_quantity_creation_nocopy():
    u.Quantity(a, u.m, copy=False)


def time_quantity_view():
    q1.view(u.Quantity)


def time_quantity_init_scalar():
    3. * u.m / u.s


def time_quantity_init_array():
    a * u.m / u.s


def time_quantity_init_small_list():
    """
    https://github.com/astropy/astropy/issues/7546 reported high overhead
    for small list.
    """
    b1 * u.m / u.s


def time_quantity_init_small_array():
    """
    https://github.com/astropy/astropy/issues/7546 reported high overhead
    for small array.
    """
    b2 * u.m / u.s


def time_quantity_scalar_conversion():
    (3. * u.m / u.s).to(u.km / u.hour)


def time_quantity_array_conversion():
    (a * u.m / u.s).to(u.km / u.hour)


def time_quantity_times_unit():
    q1 * u.m


def time_quantity_times_quantity():
    q1 * q0


def time_quantity_ufunc_sin():
    np.sin(q2)


class TimeQuantityOpSmallArray:
    """
    Operator benchmarks from https://github.com/astropy/astropy/issues/7546
    for a small Numpy array.
    """
    def setup(self):
        data = np.array([1., 2., 3.])
        self.data = data * u.g
        self.out_sq = data * u.g ** 2
        self.out_sqrt = data * u.g ** 0.5

    def time_quantity_square(self):
        self.data ** 2

    def time_quantity_np_square(self):
        np.power(self.data, 2)

    def time_quantity_np_square_out(self):
        np.power(self.data, 2, out=self.out_sq)

    def time_quantity_sqrt(self):
        self.data ** 0.5

    def time_quantity_np_sqrt(self):
        np.sqrt(self.data)

    def time_quantity_np_sqrt_out(self):
        np.sqrt(self.data, out=self.out_sqrt)


class TimeQuantityOpLargeArray(TimeQuantityOpSmallArray):
    """
    Like :class:`TimeQuantityOpSmallArray` but for a large Numpy array.
    """
    def setup(self):
        data = np.arange(1e6) + 1
        self.data = data * u.g
        self.out_sq = data * u.g ** 2
        self.out_sqrt = data * u.g ** 0.5


class TimeQuantityOpSmallArrayDiffUnit:
    """
    Operator benchmarks from https://github.com/astropy/astropy/issues/7546
    for small Numpy arrays with different units.
    """
    def setup(self):
        data = np.array([1., 2., 3.])
        self.data = data * u.g

        # A different but dimensionally compatible unit
        self.data2 = 0.001 * data * u.kg

    def time_quantity_equal(self):
        # Same as operator.eq
        self.data == self.data2

    def time_quantity_np_equal(self):
        np.equal(self.data, self.data2)

    def time_quantity_truediv(self):
        # Since benchmark is PY3 only, this is always true divide.
        # Same as operator.truediv
        self.data / self.data2

    def time_quantity_np_truediv(self):
        np.true_divide(self.data, self.data2)

    def time_quantity_mul(self):
        # Same as operator.mul
        self.data * self.data2

    def time_quantity_np_multiply(self):
        np.multiply(self.data, self.data2)

    def time_quantity_sub(self):
        # Same as operator.sub
        self.data - self.data2

    def time_quantity_np_subtract(self):
        np.subtract(self.data, self.data2)

    def time_quantity_add(self):
        # Same as operator.add
        self.data + self.data2

    def time_quantity_np_add(self):
        np.add(self.data, self.data2)


class TimeQuantityOpSmallArraySameUnit(TimeQuantityOpSmallArrayDiffUnit):
    """
    Operator benchmarks from https://github.com/astropy/astropy/issues/7546
    for small Numpy arrays with same units.
    """
    def setup(self):
        data = np.array([1., 2., 3.])
        self.data = data * u.g
        self.data2 = self.data.copy()


class TimeQuantityOpLargeArrayDiffUnit(TimeQuantityOpSmallArrayDiffUnit):
    """
    Like :class:`TimeQuantityOpSmallArrayDiffUnit` but for large Numpy arrays.
    """
    def setup(self):
        data = np.arange(1e6) + 1
        self.data = data * u.g

        # A different but dimensionally compatible unit
        self.data2 = 0.001 * data * u.kg


class TimeQuantityOpLargeArraySameUnit(TimeQuantityOpSmallArrayDiffUnit):
    """
    Like :class:`TimeQuantityOpSmallArraySameUnit` but for large Numpy arrays.
    """
    def setup(self):
        data = np.arange(1e6) + 1
        self.data = data * u.g
        self.data2 = self.data.copy()
