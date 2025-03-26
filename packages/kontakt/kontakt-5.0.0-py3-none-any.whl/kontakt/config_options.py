"""Support for defining configurable options and building default configs from them.

There are two related ideas here. The first is of a *configurable options*, a description of
a single option in a *configuration*. A configuration, then, is just a tree - modeled as
dicts-of-dicts - where the leaf values are the options. So an option describes a path through
the tree to a leaf, a description of the option, and a default value for the leaf.
"""

from abc import abstractmethod
from dataclasses import dataclass
import copy
from typing import Any, Iterable, Mapping, Tuple

from dendrodict import DeepDict

from . import Extension


@dataclass
class Option:
    """Description of a single configurable option.

    Fields:
        path: Path to the option in the config.
        description: Description of the option.
        default: Default value of the option.
    """

    path: Tuple[str]
    description: str
    default: Any

    def __post_init__(self):
        if len(self.path) < 1:
            raise ValueError("Path must have at least one element")

    @property
    def name(self):
        "The name of the option."
        return self.path[-1]


class ConfigurableExtension(Extension):
    @abstractmethod
    def construct(self, extension_config, *args, **kwargs):
        """Construct the object that the extension provides.

        This method can use config values in `extension_config` as well as
        values from *args and **kwargs to build the object.

        Args:
            extension_config (dict): Config dict for the extension. It should
                have value for each of the extension's ``Option``\s.

        Returns:
            Any: The object provided by this extension.
        """
        return NotImplementedError

    def config_options(self) -> Iterable[Option]:
        """The configuration options used by this extension.

        Returns:
            Iterable[Option]: An iterable of ``Option``\s describing the
                configuration options used by the extension.
        """
        return ()


def build_default_config(options) -> dict:
    """Build a default config from an iterable of options."""
    return DeepDict({option.path: option.default for option in options}).to_dict()


def merge_configs(dest, src):
    """Merge two config dicts.

    Merging can't happen if the dictionaries are incompatible. This happens when the same path in `src` exists in `dest`
    and one points to a `dict` while another points to a non-`dict`.

    Returns: A new `dict` with the contents of `src` merged into `dest`.

    Raises:
        ValueError: If the two dicts are incompatible.
    """
    dest = copy.deepcopy(dest)

    for src_name, src_val in src.items():
        if isinstance(src_val, Mapping):
            dest_val = dest.get(src_name, {})
            if not isinstance(dest_val, Mapping):
                raise ValueError("Incompatible config structures")

            dest[src_name] = merge_configs(dest_val, src_val)
        else:
            try:
                if isinstance(dest[src_name], Mapping):
                    raise ValueError("Incompatible config structures")
            except KeyError:
                pass
            dest[src_name] = src_val

    return dest
