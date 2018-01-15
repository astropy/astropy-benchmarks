# from astropy.io import ascii
# from cStringIO import StringIO
# import numpy as np
# import pandas

# class NoStripSplitter(ascii.DefaultSplitter):
#     process_val = None

# class ComparisonSuite:
#     def setup(self):
#         self.mix_dtype = np.dtype({'names': '123456789', 'formats':
#                 ('i4', 'f4', 'S10', 'i4', 'f4', 'S10', 'i4', 'f4', 'S10')})
#         self.data = {}
#         self.tables = {}
#         self.frames = {}
#         for datatype in ('float', 'int', 'string', 'mixture'):
#             f = open('benchmarks/files/comparison/{}.txt'.format(datatype))
#             self.data[datatype] = f.read()
#             f.close()
#             self.tables[datatype] = ascii.read(StringIO(self.data[datatype]),
#                                                format='basic', guess=False)
#             self.frames[datatype] = pandas.read_csv(StringIO(
#                                     self.data[datatype]), sep=' ')
#         self.out = StringIO()

#     def time_astropy_float(self):
#         ascii.read(StringIO(self.data['float']), format='basic', guess=False)

#     def time_astropy_int(self):
#         ascii.read(StringIO(self.data['int']), format='basic', guess=False)

#     def time_astropy_string(self):
#         ascii.read(StringIO(self.data['string']), format='basic', guess=False)

#     def time_astropy_mixture(self):
#         ascii.read(StringIO(self.data['mixture']), format='basic', guess=False)

#     def time_astropy_mixture_no_strip(self):
#         ascii.read(StringIO(self.data['mixture']), format='basic',
#                    data_Splitter=NoStripSplitter, guess=False)

#     def time_astropy_write_float(self):
#         ascii.write(self.tables['float'], self.out, format='basic')

#     def time_astropy_write_int(self):
#         ascii.write(self.tables['int'], self.out, format='basic')

#     def time_astropy_write_string(self):
#         ascii.write(self.tables['string'], self.out, format='basic')

#     def time_astropy_write_mixture(self):
#         ascii.write(self.tables['mixture'], self.out, format='basic')

#     def time_numpy_loadtxt_float(self):
#         np.loadtxt(StringIO(self.data['float']), delimiter=' ')

#     def time_numpy_loadtxt_int(self):
#         np.loadtxt(StringIO(self.data['int']), delimiter=' ',
#                    dtype='i4')

#     def time_numpy_loadtxt_string(self):
#         np.loadtxt(StringIO(self.data['string']), delimiter=' ',
#                    dtype='S10')

#     def time_numpy_loadtxt_mixture(self):
#         np.loadtxt(StringIO(self.data['mixture']), delimiter=' ',
#                    dtype=self.mix_dtype)

#     def time_numpy_genfromtxt_float(self):
#         np.genfromtxt(StringIO(self.data['float']), delimiter=' ')

#     def time_numpy_genfromtxt_int(self):
#         np.genfromtxt(StringIO(self.data['int']), delimiter=' ',
#                       dtype='i4')

#     def time_numpy_genfromtxt_string(self):
#         np.genfromtxt(StringIO(self.data['string']), delimiter=' ',
#                       dtype='S10')

#     def time_numpy_genfromtxt_mixture(self):
#         # Test out genfromtxt's autoconversion
#         np.genfromtxt(StringIO(self.data['mixture']), delimiter=' ',
#                       dtype=None)

#     def time_numpy_savetxt_float(self):
#         np.savetxt(self.out, self.tables['float'])

#     def time_numpy_savetxt_int(self):
#         np.savetxt(self.out, self.tables['int'], fmt='%i')

#     def time_numpy_savetxt_string(self):
#         np.savetxt(self.out, self.tables['string'], fmt='%s')

#     def time_numpy_savetxt_mixture(self):
#         np.savetxt(self.out, self.tables['mixture'], fmt='%i %f %s ' \
#                    '%i %f %s %i %f %s')

#     def time_pandas_read_table_float(self):
#         pandas.read_table(StringIO(self.data['float']), sep=' ')

#     def time_pandas_read_table_int(self):
#         pandas.read_table(StringIO(self.data['int']), sep=' ')

#     def time_pandas_read_table_string(self):
#         pandas.read_table(StringIO(self.data['string']), sep=' ')

#     def time_pandas_read_table_mixture(self):
#         pandas.read_table(StringIO(self.data['mixture']), sep=' ')

#     def time_pandas_read_csv_float(self):
#         pandas.read_csv(StringIO(self.data['float']), sep=' ')

#     def time_pandas_read_csv_int(self):
#         pandas.read_csv(StringIO(self.data['int']), sep=' ')

#     def time_pandas_read_csv_string(self):
#         pandas.read_csv(StringIO(self.data['string']), sep=' ')

#     def time_pandas_read_csv_mixture(self):
#         pandas.read_csv(StringIO(self.data['mixture']), sep=' ')

#     def time_pandas_write_float(self):
#         self.frames['float'].to_csv(self.out, sep=' ')

#     def time_pandas_write_int(self):
#         self.frames['int'].to_csv(self.out, sep=' ')

#     def time_pandas_write_string(self):
#         self.frames['string'].to_csv(self.out, sep=' ')

#     def time_pandas_write_mixture(self):
#         self.frames['mixture'].to_csv(self.out, sep=' ')
