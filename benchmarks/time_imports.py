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
		try:
			__import__(module_name)
		except ImportError as e:
			print(e)
	elif method == 'subprocess':
		import sys
		import subprocess
		# TODO: is this necessary to get the right Python executable?
		executable = sys.executable
		cmd = '{0} -c "import {1}"'.format(executable, module_name)
		subprocess.call(cmd, shell=True)
	else:
		raise ValueError('Unknown method: {0}'.format(method))


# Save some boilerplate code by generating the `time_*` functions dynamically
MODULES = ['subprocess', 'numpy', 'astropy',
		   'astropy.config',
		   'astropy.constants',
		   'astropy.convolution',
		   'astropy.coordinates',
		   'astropy.cosmology',
		   'astropy.erfa',
		   'astropy.io.ascii',
		   'astropy.io.fits',
		   'astropy.io.votable',
		   'astropy.modeling',
		   'astropy.nddata',
		   'astropy.stats',
		   'astropy.table',
		   'astropy.time',
		   'astropy.units',
		   'astropy.vo',
		   'astropy.wcs'
           ]
METHODS = ['sys', 'subprocess']

from functools import partial
for module in MODULES:
	for method in METHODS:
		function_name = 'time_import_{0}_{1}'.format(module.replace('.', '_'), method)
		globals()[function_name] = partial(_time_import, module_name=module, method=method)

if __name__ == '__main__':
	import time
	for module in MODULES:
		print()
		for method in METHODS:
			function_name = 'time_import_{0}_{1}'.format(module.replace('.', '_'), method)
			t = time.time()
			globals()[function_name]()
			t = time.time() - t
			print('{0:>50s} : {1:12.3f} ms'.format(function_name, 1e3 * t))

