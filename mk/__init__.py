import importlib


_extensions = ["tuples", "lists"]

for ext in _extensions:
    importlib.import_module("mk.ext.{}".format(ext), package=__package__)
