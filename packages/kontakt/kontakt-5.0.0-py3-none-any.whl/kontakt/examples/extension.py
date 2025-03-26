"""Examples of how to use the kontakt extension system.

These serve both as a concrete example of how to use kontakt
as well as for use in the tests.
"""

import kontakt


# First we define a new kind of extension, 'example-extension', of which we'll create different implementations below.
@kontakt.Extension.new('example-extension')
class ExampleExtension:
    def __init__(self, flavor, size, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.flavor = flavor
        self.size = size


class ExampleExtensionError(kontakt.ExtensionError):
    pass


# Here's the first implementation of ExampleExtension. This would be registered as an entry point in setup.py something like this:
#
#    entry_points = {
#        "my_app.examples": [ "blue = my_app.examples.blue.Blue", . . .]
#    }
class Blue(ExampleExtension):
    pass

# This second one would be registered something like this: "green = my_app.examples.red.Red"
class Red(ExampleExtension):
    "Red extension"
    pass


class Green(ExampleExtension):
    @classmethod
    def describe(cls):
        return "description of the Green extension"
        
# Then you'd probably have a function like this for constructing the ExampleExtension subclasses

def get_example_extension(name):
    return kontakt.create_extension(
        namespace='my_app.examples',
        name=name, # e.g. blue, red, etc...whatever names you used in entry_points.my_app.examples
        exception_type=ExampleExtensionError
    )
