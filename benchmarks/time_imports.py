"""Time how long it takes to import each of the Astropy sub-packages.
"""


def time_import_astropy():
    # The top-level package
    import astropy


def time_import_numpy():
    # For comparison
    import numpy


def time_import_coordinates():
    import astropy.coordinates


def time_import_units():
    import astropy.units
