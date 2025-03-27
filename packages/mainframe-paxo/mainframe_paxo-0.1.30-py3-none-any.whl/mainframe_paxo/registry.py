from __future__ import annotations

import contextlib
import ntpath
import winreg
from typing import Any, Iterator, Optional, Tuple, Union
from winreg import HKEYType

"""helper classes for registry operations"""

# map the winreg root key constants to their names
root_keys: dict[int, str] = {}
for key, val in winreg.__dict__.items():
    if key.startswith("HKEY_"):
        root_keys[val] = key


def handle_to_str(handle: int) -> str:
    """Converts a handle to a string"""
    try:
        return root_keys[handle]
    except KeyError:
        return repr(handle)


def join_names(*names: str) -> str:
    """Joins the names together, removing any empty strings"""
    return ntpath.join(*names)


class Key:
    """A key in the registry.  This is a wrapper around the winreg module."""

    @classmethod
    def _create_root_key(cls, root: int, *args, **kwargs):
        """Creates a key object for a root key"""
        if args:
            return cls(root, *args, **kwargs)
        key = cls(root, "", **kwargs)
        key._handle = root
        key.name = ""
        assert key.is_root()
        return key

    @classmethod
    def classes_root(cls, *args, **kwargs):
        """Returns a key object for HKEY_CLASSES_ROOT"""
        return cls._create_root_key(winreg.HKEY_CLASSES_ROOT, *args, **kwargs)

    @classmethod
    def current_user(cls, *args, **kwargs):
        """Returns a key object for HKEY_CURRENT_USER"""
        return cls._create_root_key(winreg.HKEY_CURRENT_USER, *args, **kwargs)

    @classmethod
    def local_machine(cls, *args, **kwargs):
        """Returns a key object for HKEY_LOCAL_MACHINE"""
        return cls._create_root_key(winreg.HKEY_LOCAL_MACHINE, *args, **kwargs)

    @classmethod
    def users(cls, *args, **kwargs):
        """Returns a key object for HKEY_USERS"""
        return cls._create_root_key(winreg.HKEY_USERS, *args, **kwargs)

    @classmethod
    def current_config(cls, *args, **kwargs):
        """Returns a key object for HKEY_CURRENT_CONFIG"""
        return

    def __init__(
        self,
        parent: Union[Key, int],
        *names: str,
        **kwargs,
    ) -> None:
        """Create a new key object.  The key is not opened or created."""
        self._parent = parent
        assert names
        self.name = ntpath.join(*names)
        self._handle: Optional[Union[HKEYType, int]] = None
        self._kwargs = kwargs  # passed to an implicit open() in context manager

    def _hkey_name(self) -> Tuple[Any, str]:
        """returns a handle and name for the key.  Used internally."""
        if isinstance(self._parent, Key):
            if self._parent.is_open():
                return self._parent._handle, self.name
            h, n = self._parent._hkey_name()
            return h, join_names(n, self.name)
        return self._parent, self.name

    def _hkey_fullname(self) -> Tuple[Any, str]:
        """returns a top level handle and full name for the key.  Used internally."""
        if isinstance(self._parent, Key):
            h, n = self._parent._hkey_fullname()
            return h, join_names(n, self.name)
        return self._parent, self.name

    def __repr__(self) -> str:
        """Returns a string representation of the key"""
        h, n = self._hkey_fullname()
        return f"Key<{handle_to_str(h)}:{n!r}>"

    def open(
        self,
        *subkeys: str,
        create: bool = False,
        write: Optional[bool] = None,
        check: bool = True,
    ) -> Optional[Key]:
        """Opens an existing key"""
        if subkeys:
            return self.subkey(*subkeys).open(create=create, write=write, check=check)
        assert self._handle is None
        handle, name = self._hkey_name()
        try:
            # create defaults for true if create is true, false otherwise
            write = write if write is not None else create
            access: int = winreg.KEY_READ
            if write:
                access |= winreg.KEY_WRITE
            func = winreg.CreateKeyEx if create else winreg.OpenKeyEx
            self._handle = func(handle, name, access=access)
        except FileNotFoundError as e:
            if check:
                raise ValueError(f"Key {self.name!r} not found") from e
            return None
        return self

    def create(self, *subkeys: str, **kwargs) -> Optional[Key]:
        """Opens or creates a key.  Alias for open(... create=True)"""
        kwargs["create"] = True
        return self.open(*subkeys, **kwargs)

    def subkey(self, *subkeys: str, **kwargs) -> Key:
        """Returns a subkey object"""
        return Key(self, *subkeys, **kwargs)

    def __call__(self, *subkeys: str, **kwargs) -> Key:
        """Returns a subkey object"""
        return self.subkey(*subkeys, **kwargs)

    def exists(self) -> bool:
        """checks if the key exists"""
        if self.is_open():
            return True
        if self.open(check=False) is None:
            return False
        self.close()
        return True

    def is_open(self) -> bool:
        """Checks if the key is opened"""
        return self._handle is not None

    def is_root(self) -> bool:
        """Checks if the key is a root key"""
        return self._parent == self._handle

    def close(self) -> None:
        """Closes the key."""
        # close if open and if not a root key
        if self.is_open() and not self.is_root():
            handle, self._handle = self._handle, None
            assert handle is not None
            winreg.CloseKey(handle)

    # iterating over the key/value pairs (items) in the key, similar to a dict.

    def items_t(self) -> Iterator[tuple[str, tuple[Any, int]]]:
        """Iterates over the values in the key, returning (name, (value, type)) tuples."""
        assert self._handle is not None
        for i in range(1000):
            try:
                name, value, type = winreg.EnumValue(self._handle, i)
                yield (name, (value, type))
            except OSError:
                break

    def items(self) -> Iterator[tuple[str, Any]]:
        """Iterates over the values in the key, returning (name, value) typles"""
        for name, (value, _) in self.items_t():
            yield (name, value)

    def keys(self) -> Iterator[str]:
        """iterates of the item names in the key"""
        for itemname, _ in self.items_t():
            yield itemname

    def values(self) -> Iterator[Any]:
        """iterates of the item values in the key"""
        for _, (value, _) in self.items_t():
            yield value

    def values_t(self):  # -> Iterator[tuple[Any, int]]:
        """iterates of the item values in the key, returning (value, type) tuples."""
        for _, value in self.items_t():
            yield value

    def subkeys(self) -> Iterator[Key]:
        """Iterates over the subkeys in the key"""
        assert self._handle is not None
        for i in range(1000):
            try:
                name = winreg.EnumKey(self._handle, i)
                yield Key(self, name)
            except OSError:
                break

    def value_get(self, name: str, default: Any = None) -> tuple[Any, int]:
        """Gets a value from the key, returning the value and a type."""
        assert self._handle is not None
        try:
            return winreg.QueryValueEx(self._handle, name)
        except FileNotFoundError as e:
            raise KeyError(name) from e

    def value_set(self, name: str, value: Any, type=winreg.REG_SZ) -> None:
        """Sets a value in the key, along with its type."""
        assert self._handle is not None
        winreg.SetValueEx(self._handle, name, 0, type, value)

    def value_del(self, name: str) -> None:
        assert self._handle is not None
        winreg.DeleteValue(self._handle, name)

    def get(self, name: str, default: Any = None) -> Any:
        """Gets a value from the key"""
        try:
            return self[name]
        except KeyError:
            return default

    def __getitem__(self, name: str) -> Tuple[Any, int]:
        """Get a value from the key"""
        assert self._handle is not None
        try:
            v, t = winreg.QueryValueEx(self._handle, name)
            if t == winreg.REG_BINARY and v is None:
                v = b""
            return v
        except FileNotFoundError as e:
            raise KeyError(name) from e

    def __setitem__(self, name: str, value: Any) -> None:
        """Sets a value in the key. We assume a string"""
        if isinstance(value, tuple):
            return self.value_set(name, *value)
        elif isinstance(value, int):
            return self.value_set(name, value, winreg.REG_DWORD)
        elif isinstance(value, bytes):
            return self.value_set(name, value, winreg.REG_BINARY)
        elif value is None:
            return self.value_set(name, None, winreg.REG_NONE)
        # default handling
        return self.value_set(name, value, winreg.REG_SZ)

    def __delitem__(self, name: str) -> None:
        """Deletes a value from the key"""
        assert self._handle is not None
        try:
            winreg.DeleteValue(self._handle, name)
        except FileNotFoundError as e:
            raise KeyError(name) from e

    def __enter__(self) -> Optional[Key]:
        """Context manager: opens the key if required"""
        if not self.is_open():
            return self.open(**self._kwargs)
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.close()

    @contextlib.contextmanager
    def opened(self, *args, **kwargs):
        """Context manager: opens the key if required"""
        if args or not self.is_open():
            with self.open(*args, **kwargs) as key:
                yield key
        else:
            yield self

    def delete(self, tree: bool = False, missing_ok=True) -> None:
        """Deletes the key, optionally recursively."""
        if self.is_open():
            raise ValueError("Cannot delete open key")
        if missing_ok and not self.exists():
            return
        if tree:
            with self.opened():
                for subkey in list(self.subkeys()):
                    subkey.delete(tree=True)
        h, n = self._hkey_name()
        winreg.DeleteKey(h, n)

    def copy(self) -> Key:
        """Returns a fresh, un-opened copy of the key"""
        return Key(self._parent, self.name)

    def print(self, tree=False, indent=4, level=0):
        """Prints the key to stdout"""
        print(" " * level * indent + f"key: '{self.name}'")
        with self.opened() as key:
            for name, value in key.items():
                print(" " * (level + 1) * indent + f"val: '{name}' = {value})")
            if not tree:
                for sub in key.subkeys():
                    print(" " * (level + 1) * indent + f"key: '{sub.name}'")
            else:
                for sub in key.subkeys():
                    sub.print(tree=True, indent=indent, level=level + 1)

    def as_dict(self):
        """Returns the key and subkeys as a dictionary"""
        with self.opened() as key:
            return {
                "keys": {sub.name: sub.as_dict() for sub in key.subkeys()},
                "values": {name: value for name, value in key.items()},
            }

    def from_dict(self, data, remove: bool = False):
        """Sets the key and subkeys from a dictionary"""
        with self.opened(create=True) as key:
            for name, value in data["values"].items():
                if isinstance(value, tuple):
                    key.set_value(name, *value)
                else:
                    key[name] = value
            for subname, subdata in data["keys"].items():
                key.create(subname).from_dict(subdata, remove=remove)

            if remove:
                for sub in key.subkeys():
                    if sub.name not in data["keys"]:
                        sub.delete(tree=True)
                for name in key.keys():
                    if name not in data["values"]:
                        del key[name]
