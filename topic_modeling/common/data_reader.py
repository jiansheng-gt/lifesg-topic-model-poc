import os

class DataReader(object):
    def __init__(self, dirname):
        self.dirname = dirname
        self.filenames = sorted(os.listdir(self.dirname))

    def __iter__(self):
        for fname in self.filenames:
            yield open(os.path.join(self.dirname, fname)).read()

    def get_filenames(self):
        return self.filenames