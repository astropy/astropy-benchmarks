from astropy.io.ascii import sextractor
import random
try:
    from string import uppercase
except ImportError:
    from string import ascii_uppercase as uppercase

def randword():
    return ''.join([random.choice(uppercase) for i in range(10)])

class SExtractorSuite:
    def setup(self):
        self.header = sextractor.SExtractorHeader()
        self.lines = []
        i = 0
        while i < 100000:
            if i % 20 == 0 and i != 0:
                i += 4
            i += 1
            self.lines.append('# {} {} Description [pixel**2]'.format(
                                                        i, randword()))
        self.lines.append('Non-header line')

    def time_header(self):
        self.header.get_cols(self.lines)
