#coding:utf-8

import time
from modules.color import warning, info

class Benchmark:

    timestamps = {}

    def set(cls, label):
        Benchmark.timestamps[label] = time.time()

    def get(cls, start, stop=None, output_format="Elapsed time: %ts", float_length=4, float_operation="keep", return_time=False):
        if start not in Benchmark.timestamps or (stop != None and stop not in Benchmark.timestamps):
            if return_time:
                return -1
            else:
                warning("Benchmark error")
                return True
        start = Benchmark.timestamps[start]
        stop = Benchmark.timestamps[stop] if stop != None else time.time()
        elapsed = str(stop - start).split(".")
        if float_operation in "ceil" or float_operation in "ceil":
            if float_operation == "ceil":
                elapsed[0] = str(int(elapsed[0]) + 1)
            elapsed[1] = "0" * float_length
        elif float_operation in "round" and int(elapsed[1][0]) >= 5:
            elapsed[0] = str(int(elapsed[0]) + 1)
            elapsed[1] = "0" * float_length
        if float_length >= len(elapsed[1]):
            float_length = len(elapsed[1]) - 1
        elapsed[1] = elapsed[1][0:float_length]
        elapsed = ".".join(elapsed)
        if return_time:
            return float(elapsed)
        info(output_format.replace("%t", elapsed))
        return False

    mark = classmethod(set)
    elapsed_time = classmethod(get)
