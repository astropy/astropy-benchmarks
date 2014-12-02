"""Time how long it takes to import each of the Astropy sub-packages.
"""

def _time_import(module_name, method='sys'):
	"""Time how long the import for a given module takes.

	Code suggested by @embray here:
	https://github.com/astropy/astropy-benchmarks/pull/15#issuecomment-65144632

	Parameters
	----------
	module_name : str
		Module (or package or sub-package) name
	method : {'sys', 'subprocess'}
		Method to measure the import time
	"""
	if method == 'sys':
		import sys
		try:
			del sys.modules[module_name]
		except KeyError:
			pass
		__import__(module_name)
	elif method == 'subprocess':
		import sys
		import subprocess
		# TODO: is this necessary to get the right Python executable?
		executable = sys.executable
		cmd = '{0} -c "import {1}"'.format(executable, module_name)
		subprocess.call(cmd, shell=True)
	else:
		raise ValueError('Unknown method: {0}'.format(method))


def time_import_numpy():
    # For comparison
    _time_import('numpy', method='sys')


def time_import_astropy():
    # The top-level package
    _time_import('astropy', method='sys')

def time_import_coordinates_sys():
    _time_import('astropy.coordinates', method='sys')


def time_import_coordinates_subprocess():
    _time_import('astropy.coordinates', method='subprocess')


def time_import_units():
    import astropy.units
