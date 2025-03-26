"""Example of how to create a ConfigurableExtension."""

from dataclasses import dataclass
from kontakt.config_options import ConfigurableExtension, Option
from kontakt import ExtensionError

KIND = "renderer"


@ConfigurableExtension.new(KIND)
class RendererExtension(ConfigurableExtension):
    pass


class RendererExtensionError(ExtensionError):
    pass


class PrinterExtension(RendererExtension):
    def config_options(self):
        return (Option(("font", "size"), "Font size", 42), Option(("font", "family"), "Font family", "serif"))

    def construct(self, extension_config, *args, **kwargs):
        return Printer(
            font_size=extension_config["font"]["size"], font_family=extension_config["font"]["family"], *args, **kwargs
        )


@dataclass
class Printer:
    font_size: int
    font_family: str
    model: str
