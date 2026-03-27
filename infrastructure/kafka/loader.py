import importlib
import pkgutil
import app.consumers


def load_consumers():
    package = app.consumers
    for _, module_name, _ in pkgutil.iter_modules(package.__path__):
        module = f"app.consumers.{module_name}"
        importlib.import_module(module)
        print(f"Loaded consumer module: {module}")