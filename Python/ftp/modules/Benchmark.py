#coding:utf-8

import time

class Benchmark:

    timestamps = {}

    def set(cls, label):
        Benchmark.timestamps[label] = time.time()

    def get(cls, start, stop=None):
        if start not in Benchmark.timestamps or (stop != None and stop not in Benchmark.timestamps):
            return -1
        if stop == None:
            return time.time() - Benchmark.timestamps[start]
        return Benchmark.timestamps[stop] - Benchmark.timestamps[start]

    mark = classmethod(set)
    elapsed_time = classmethod(get)
