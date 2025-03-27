import inspect
import importlib

def printFunctionCode(func_name):
    for submodule in ["sorting"]:
        try:
            module = importlib.import_module(f"algozar.{submodule}")
            func = getattr(module, func_name, None)
            if func and callable(func):
                print(inspect.getsource(func))
                return
        except ModuleNotFoundError:
            pass

    print(f"Function '{func_name}' not found in algozar.")

class Printer:
    def __getattr__(self, name):
        return lambda: printFunctionCode(name)

algoPrint = Printer()
