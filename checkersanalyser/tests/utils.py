import time


def test():
    pass


def timeit(test_name):
    def _timeit(test_func):
        def timed():
            t1 = time.time()
            test_func()
            tm = time.time() - t1
            print(f'{test_name} time:{tm}')

        return timed

    return _timeit
