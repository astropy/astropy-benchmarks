from astropy.io.ascii import core
import random
try:
    from itertools import izip
except ImportError:
    izip = zip
try:
    from string import uppercase
except ImportError:
    from string import ascii_uppercase as uppercase


def randword():
    return ''.join([random.choice(uppercase) for i in range(10)])


class CoreSuite:
    def setup(self):
        self.lines = []
        options = [['a b c d'], ['a b c \\', 'd'], ['a b \\', 'c \\', 'd'],
                   ['a b \\', 'c d'], ['a \\', 'b c \\', 'd']]
        for i in range(1000):
            self.lines.extend(options[i % 5])
        options = ['"a\tbc\t\td"', 'ab cd', '\tab\t\tc\td', 'a \tb \tcd']
        self.line = ''.join([options[i % 4] for i in range(1000)])
        self.vals = [randword() for i in range(1000)]
        self.csv_line = ','.join([str(x) for x in self.vals])
        lst = []
        lst.append([random.randint(-500, 500) for i in range(1000)])
        lst.append([random.random() * 500 - 500 for i in range(1000)])
        lst.append([''.join([random.choice(uppercase) for j in
                            range(6)]) for i in range(1000)])
        self.cols = [core.Column(str(i + 1)) for i in range(3)]
        for col, x in izip(self.cols, lst):
            col.str_vals = [str(s) for s in x]
    def time_continuation_inputter(self):
        core.ContinuationLinesInputter().process_lines(self.lines)
    def time_whitespace_splitter(self):
        core.WhitespaceSplitter().process_line(self.line)
    def time_default_splitter_call(self):
        core.DefaultSplitter()(self.csv_line)
    def time_default_splitter_join(self):
        core.DefaultSplitter().join(self.vals)
    def time_base_splitter(self):
        core.BaseSplitter().process_val(self.line)
    def time_convert_vals(self):
        core.TableOutputter()._convert_vals(self.cols)
