# SPDX-License-Identifier: BSD-2-Clause
# Code imported from:
# https://github.com/sphinx-doc/sphinx/blob/master/sphinx/ext/autodoc/mock.py

from importlib.abc import Loader, MetaPathFinder
from importlib.machinery import ModuleSpec
import os
import sys
from types import ModuleType
from typing import Any, Iterator, Sequence


class _MockObject:
    """Used by autodoc_mock_imports."""

    __display_name__ = "_MockObject"
    __name__ = ""
    __sphinx_mock__ = True
    __sphinx_decorator_args__: tuple[Any, ...] = ()

    def __new__(cls, *args: Any, **kwargs: Any) -> Any:
        if len(args) == 3 and isinstance(args[1], tuple):
            superclass = args[1][-1].__class__
            if superclass is cls:
                # subclassing MockObject
                return _make_subclass(
                    args[0],
                    superclass.__display_name__,
                    superclass=superclass,
                    attributes=args[2],
                )

        return super().__new__(cls)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.__qualname__ = self.__name__

    def __len__(self) -> int:
        return 0

    def __contains__(self, key: str) -> bool:
        return False

    def __iter__(self) -> Iterator:
        return iter([])

    def __mro_entries__(self, bases: tuple) -> tuple:
        return (self.__class__,)

    def __getitem__(self, key: Any) -> "_MockObject":
        return _make_subclass(str(key), self.__display_name__)()

    def __getattr__(self, key: str) -> "_MockObject":
        return _make_subclass(key, self.__display_name__)()

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        call = self.__class__()
        call.__sphinx_decorator_args__ = args
        return call

    def __repr__(self) -> str:
        return self.__display_name__


def _make_subclass(
    name: str,
    module: str,
    superclass: Any = _MockObject,
    attributes: Any = None,
    decorator_args: tuple = (),
) -> Any:
    attrs = {
        "__module__": module,
        "__display_name__": module + "." + name,
        "__name__": name,
        "__sphinx_decorator_args__": decorator_args,
    }
    attrs.update(attributes or {})

    return type(name, (superclass,), attrs)


class _MockModule(ModuleType):
    """Used by autodoc_mock_imports."""

    __file__ = os.devnull
    __sphinx_mock__ = True

    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.__all__: list[str] = []
        self.__path__: list[str] = []

    def __getattr__(self, name: str) -> _MockObject:
        return _make_subclass(name, self.__name__)()

    def __repr__(self) -> str:
        return self.__name__


class MockLoader(Loader):
    """A loader for mocking."""

    def __init__(self, finder: "MockFinder") -> None:
        super().__init__()
        self.finder = finder

    def create_module(self, spec: ModuleSpec) -> ModuleType:
        self.finder.mocked_modules.append(spec.name)
        return _MockModule(spec.name)

    def exec_module(self, module: ModuleType) -> None:
        pass  # nothing to do


class MockFinder(MetaPathFinder):
    """A finder for mocking."""

    def __init__(self, modnames: list[str]) -> None:
        super().__init__()
        self.modnames = modnames
        self.loader = MockLoader(self)
        self.mocked_modules: list[str] = []

    def find_spec(
        self,
        fullname: str,
        path: Sequence[bytes | str] | None,
        target: ModuleType | None = None,
    ) -> ModuleSpec | None:
        for modname in self.modnames:
            # check if fullname is (or is a descendant of) one of our targets
            if modname == fullname or fullname.startswith(modname + "."):
                return ModuleSpec(fullname, self.loader)

        return None

    def invalidate_caches(self) -> None:
        """Invalidate mocked modules on sys.modules."""
        for modname in self.mocked_modules:
            sys.modules.pop(modname, None)
