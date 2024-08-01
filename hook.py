from __future__ import annotations

import sys
from types import ModuleType


class ModuleWrapper(ModuleType):
    def __init__(self, module: ModuleType):
        self._module = module
        super().__init__(module.__name__, module.__doc__)

    def __getattr__(self, name: str):
        module = object.__getattribute__(self, "_module")
        if "__all__" in module.__dict__:
            if name in module.__all__:
                return getattr(module, name)
            raise AttributeError(f"Module '{module.__name__}' does not export '{name}'")
        return getattr(module, name)


class WrapperFinder:
    def __init__(self):
        self.original_import = __import__

    def strict_import(self, fullname: str, *args, **kwargs):
        if fullname in sys.modules:
            return sys.modules[fullname]

        module = self.original_import(fullname, *args, **kwargs)
        wrapped = ModuleWrapper(module)
        sys.modules[fullname] = wrapped
        return wrapped


def enable_strict_imports():
    finder = WrapperFinder()
    __builtins__["__import__"] = finder.strict_import
    sys.meta_path.insert(0, finder)
