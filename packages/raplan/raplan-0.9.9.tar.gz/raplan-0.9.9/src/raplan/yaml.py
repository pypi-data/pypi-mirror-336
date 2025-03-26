"""RaPlan input/output module"""

from pathlib import Path
from typing import Any, TypeVar

import serde.yaml

T = TypeVar("T")

__all__ = ["to_yaml", "from_yaml"]


def to_yaml(obj: Any, path: str | Path | None = None) -> str | None:
    """Save an object to a YAML file.

    Arguments:
        obj: Any object from the `raplan.classes` or `raplan.distributions` modules.
        path: Path to YAML file to export to.

    Note:
        If you wish to serialize to a YAML string instead, see `raplan.io.to_yaml`, which is an
        alias of the excellent `serde.yaml.to_yaml`.
    """

    ser = serde.yaml.to_yaml(obj)
    if path is None:
        return ser
    else:
        Path(path).write_text(ser, encoding="utf-8")


def from_yaml(cls: type[T], path: str | Path) -> T:
    """Load any supported object from a YAML file.

    Arguments:
        cls: Class or type of object to import.
        path: Path to the YAML file.

    Returns:
        An instance of type `cls`.

    Note:
        If you wish to import from a YAML string instead, see `raplan.io.from_yaml`, which is an
        alias of the excellent `serde.yaml.from_yaml`
    """

    ser = Path(path).read_text(encoding="utf-8")
    return serde.yaml.from_yaml(cls, ser)
