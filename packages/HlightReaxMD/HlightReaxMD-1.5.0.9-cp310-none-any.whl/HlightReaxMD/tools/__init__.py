import pkgutil
import importlib
for _, name, _ in pkgutil.iter_modules(__path__):
    importlib.import_module(f'.{name}', package=__name__)
