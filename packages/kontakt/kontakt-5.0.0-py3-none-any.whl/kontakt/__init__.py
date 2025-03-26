
import importlib.resources.abc
import inspect
import textwrap
from abc import ABC, abstractmethod
from typing import Mapping

import asq
import stevedore
import stevedore.exception


__version__ = "5.0.0"
__version_info__ = tuple(__version__.split("."))


class Extension(ABC):
    """Base class for new extension types.

    Args:
        name: The name of the extension, i.e. as assigned in entry-points.
    """

    def __init__(self, name):
        self._name = name

    @classmethod
    def kind(cls) -> str:
        "The kind of the extension."
        return cls._kind()

    @classmethod
    @abstractmethod
    def _kind(cls) -> str:
        "Override in subclasses to specify the kind of the extension."
        raise NotImplementedError

    @property
    def name(self):
        "The name of the extension instance."
        return self._name

    @classmethod
    def dirpath(cls):
        """The directory path to the extension package."""
        package_name = inspect.getmodule(cls).__package__
        return importlib.resources.files(package_name)

    @classmethod
    def version(cls):
        "The version of the extension."
        return "1.0.0"  # We allow extensions to have a distinct version but don't exploit this yet

    @classmethod
    def describe(cls) -> str:
        """A description of the extension.

        By default, this is the docstring of the extension class if the docstring is defined. If
        the docstring is not defined, the default is the name of the class.

        Override it in the extension if you want something different.
        """

        if cls.__doc__ is None:
            description = cls.__name__
        else:
            description = cls.__doc__

        return _strip_lines(textwrap.dedent(description))

    @classmethod
    def new(cls, kind: str):
        """Decorator for creating new Extension subclasses.

        Use it like this:

            @Extension.new('renderer')
            class RendererExtension:
                @abstractmethod
                def render(self):
                    return NotImplementedError

            assert issubclass(RendererExtension, Extension)
            assert RendererExtension.kind() == 'renderer'

        Args:
            kind: The 'kind' string of the extension. This is just descriptive.
        """

        def decorator(decorated_cls):
            class Ext(decorated_cls, cls):
                @classmethod
                def _kind(cls):
                    return kind

            return Ext

        return decorator


class ExtensionError(Exception):
    "Base class for extension-specific exceptions."
    pass


def create_extension(namespace: str, name: str, exception_type: Exception, *args, **kwargs):
    """Create a new instance of an extension.

    Args:
        namespace (str): The namespace of the extension to create.
        name (str): The name of the extension to create.
        exception_type (Exception): Exception to raise when there are errors creating the exception.

    Raises:
        exception_type: If there is an error creating the extension.

    Returns:
        Any: Whatever type of object the extension provides. Typically this will be an Extension instance.
    """
    normal_name = _normalize_name(name)
    try:
        manager = stevedore.driver.DriverManager(
            namespace=namespace,
            name=normal_name,
            invoke_on_load=True,
            invoke_args=args,
            invoke_kwds={**kwargs, "name": normal_name},
        )
    except stevedore.exception.NoMatches as no_matches:
        names = list_extensions(namespace)
        name_list = ", ".join(names)
        raise exception_type(f"No {namespace} matching {name !r}. Available {namespace}s: {name_list}") from no_matches
    driver = manager.driver
    return driver


def describe_extension(namespace, name, exception_type=None) -> str:
    """Get the description of an extension.

    Args:
        namespace (str): The namespace of the extension to create.
        name (str): The name of the extension to create.
        exception_type (Exception): Exception to raise when there are errors creating the exception.

    Raises:
        exception_type: If there is an error creating the extension.

    Returns:
        str: Description of the plugin.
    """
    exception_type = exception_type or ExtensionError
    normal_name = _normalize_name(name)
    try:
        manager = stevedore.driver.DriverManager(
            namespace=namespace,
            name=normal_name,
            invoke_on_load=False,
        )
    except stevedore.exception.NoMatches as no_matches:
        names = list_extensions(namespace)
        name_list = ", ".join(names)
        raise exception_type(f"No {namespace} matching {name !r}. Available {namespace}s: {name_list}") from no_matches
    driver = manager.driver
    description = driver.describe()
    return description


def list_extensions(namespace):
    """List the names of the extensions available in a given namespace."""
    extensions = stevedore.ExtensionManager(
        namespace=namespace,
        invoke_on_load=False,
    )
    return extensions.names()


def list_dirpaths(namespace) -> Mapping[str, importlib.resources.abc.Traversable]:
    """A mapping of extension names to extension package paths."""
    extensions = stevedore.ExtensionManager(
        namespace=namespace,
        invoke_on_load=False,
    )
    return {name: _extension_dirpath(ext) for name, ext in extensions.items()}


def _extension_dirpath(ext: stevedore.extension.Extension) -> importlib.resources.abc.Traversable:
    """Get the directory path to an extension package.

    Args:
        ext: A stevedore.extension.Extension instance.

    Returns:
        A absolute Path to the package containing the extension.
    """
    package_name = ext.module_name.split(".")[0]
    resource = importlib.resources.files(package_name)
    return resource.resolve()


def _normalize_name(name):
    """Normalise a name (such as a master name) by converting hyphens to underscores."""
    return name.replace("-", "_")


def _strip_lines(text):
    """Remove leading and trailing blank lines."""

    def is_blank(line):
        return line.isspace() or not line

    return "\n".join(asq.query(text.splitlines()).skip_while(is_blank).reverse().skip_while(is_blank).reverse())
