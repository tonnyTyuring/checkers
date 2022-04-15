import importlib
import pkgutil
import checkersanalyser.tests

modules = [i.name for i in pkgutil.iter_modules(['tests'])]
[importlib.import_module(f'checkersanalyser.tests.{m}') for m in modules]
[eval(f'checkersanalyser.tests.{m}.test()') for m in modules]
