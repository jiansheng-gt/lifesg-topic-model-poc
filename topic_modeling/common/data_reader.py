import os

class DataReader(object):
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        for fname in os.listdir(self.dirname):
            yield open(os.path.join(self.dirname, fname)).read()
