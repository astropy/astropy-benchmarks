"""Benchmarks for import timing for astropy and its subpackages."""


# https://github.com/airspeed-velocity/asv/pull/832
def timeraw_import_astropy():
    return """
    import astropy
    """


def timeraw_import_astropy_config():
    return """
    from astropy import config
    """


def timeraw_import_astropy_constants():
    return """
    from astropy import constants
    """


def timeraw_import_astropy_convolution():
    return """
    from astropy import convolution
    """


def timeraw_import_astropy_coordinates():
    return """
    from astropy import coordinates
    """


def timeraw_import_astropy_cosmology():
    return """
    from astropy import cosmology
    """


def timeraw_import_astropy_io():
    return """
    from astropy import io
    """


def timeraw_import_astropy_io_ascii():
    return """
    from astropy.io import ascii
    """


def timeraw_import_astropy_io_fits():
    return """
    from astropy.io import fits
    """


def timeraw_import_astropy_io_votable():
    return """
    from astropy.io import votable
    """


def timeraw_import_astropy_io_misc():
    return """
    from astropy.io import misc
    """


def timeraw_import_astropy_io_misc_hdf5():
    return """
    from astropy.io.misc import hdf5
    """


def timeraw_import_astropy_io_misc_yaml():
    return """
    from astropy.io.misc import yaml
    """


def timeraw_import_astropy_io_misc_asdf():
    return """
    from astropy.io.misc import asdf
    """


def timeraw_import_astropy_io_misc_pandas():
    return """
    from astropy.io.misc import pandas
    """


def timeraw_import_astropy_logger():
    return """
    from astropy import logger
    """


def timeraw_import_astropy_modeling():
    return """
    from astropy import modeling
    """


def timeraw_import_astropy_nddata():
    return """
    from astropy import nddata
    """


def timeraw_import_astropy_samp():
    return """
    from astropy import samp
    """


def timeraw_import_astropy_stats():
    return """
    from astropy import stats
    """


def timeraw_import_astropy_table():
    return """
    from astropy import table
    """


def timeraw_import_astropy_tests():
    return """
    from astropy import tests
    """


def timeraw_import_astropy_tests_runner():
    return """
    from astropy.tests import runner
    """


def timeraw_import_astropy_time():
    return """
    from astropy import time
    """


def timeraw_import_astropy_timeseries():
    return """
    from astropy import timeseries
    """


def timeraw_import_astropy_timeseries_io():
    return """
    from astropy.timeseries import io
    """


def timeraw_import_astropy_timeseries_periodograms():
    return """
    from astropy.timeseries import periodograms
    """


def timeraw_import_astropy_uncertainty():
    return """
    from astropy import uncertainty
    """


def timeraw_import_astropy_units():
    return """
    from astropy import units
    """


def timeraw_import_astropy_units_quantity():
    return """
    from astropy.units import quantity
    """


def timeraw_import_astropy_utils():
    return """
    from astropy import utils
    """


def timeraw_import_astropy_utils_iers():
    return """
    from astropy.utils import iers
    """


def timeraw_import_astropy_visualization():
    return """
    from astropy import visualization
    """


def timeraw_import_astropy_visualization_wcsaxes():
    return """
    from astropy.visualization import wcsaxes
    """


def timeraw_import_astropy_wcs():
    return """
    from astropy import wcs
    """


def timeraw_import_astropy_wcs_wcsapi():
    return """
    from astropy.wcs import wcsapi
    """
