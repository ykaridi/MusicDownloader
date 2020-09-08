from functools import wraps
from inspect import Parameter, Signature
from typing import Tuple, Optional, Callable
from inspect import signature


class ImplicitResolution:
    """
    Implicit argument resolution decorator.
    Allows arguments of functions to be resolved on run-time according to some (implicit) resolution function.

    Example:
        @dataclass
        class Person:
            first_name: str
            surname: str

            @ImplicitResolution(fullname=lambda self, *args, **kwargs: "%s %s" % (self.first_name, self.surname))
            def greet(self, fullname: str):
                print("Hello %s!" % fullname)

    (More complex) Example:
        def resolve_separator(self, *args, **kwargs):
            if hasattr(self, 'SEPARATOR'):
                return getattr(self, 'SEPARATOR')
            elif 'SEPARATOR' in locals():
                return locals()['SEPARATOR']
            if 'SEPARATOR' in globals():
                return globals()['SEPARATOR']

        @ImplicitResolution(separator=resolve_separator)
        def parse_line(line, separator: str):
            return [int(part) for part in line.split(separator)]

        csv_parser.py
        -------------
        class CSVParser:
            SEPARATOR = ','
            parse_line = parse_line

        data_parser.py
        --------------
        SEPARATOR = '\t'
        parse_line("1   7   13")
    """

    def __init__(self, **resolvers: Callable):
        """
        Creates an ImplicitResolution instance
        :param resolvers: A resolver is a function which is passed the function arguments and should resolve
        some additional (implicit) argument
        """
        self.resolvers = resolvers

    @staticmethod
    def wrap_function(function, **resolvers: Callable):
        """Wraps a function to comply with some (implicit) resolvers"""
        # Get the signature of the function we are wrapping
        sig: Signature = signature(function)
        effective_params: Tuple[Parameter, ...] = tuple(param for name, param in sig.parameters.items()
                                                        if name != 'self')
        # Get parameters which can be resolved
        resolvable_params: Tuple[Parameter, ...] = tuple(param for param in effective_params
                                                         if param.name in resolvers)
        resolvable_param_names: Tuple[str, ...] = tuple(param.name for param in resolvable_params)
        # Check for possibly resolvable parameters which are not keyword-only
        problem: Optional[Parameter] = next((param for param in resolvable_params
                                             if param.kind != Parameter.KEYWORD_ONLY), None)
        if problem:
            # Allow possibly resolvable parameters to be keyword-only, to avoid bugs and complications
            raise Exception(f"Cannot allow implicit resolution of parameter [{problem.name}] of [{function.__name__}]"
                            f", must be keyword-only")

        resolvers = {name: resolver for name, resolver in resolvers.items()
                     if name in resolvable_param_names}

        @wraps(function)
        def wrapper(*args, **kwargs):
            for name, resolver in resolvers.items():
                # For every argument that can be resolved, and isn't already supplied
                # attempt resolving it (to a non-None value) and pass to the function
                if name not in kwargs and (resolved := resolver(*args, **kwargs)) is not None:
                    kwargs[name] = resolved

            unresolved_params: Tuple[Parameter, ...] = tuple(param for param in resolvable_params
                                                             if param.default == Parameter.empty
                                                             and param.name not in kwargs)
            if len(unresolved_params) > 0:
                raise ValueError("Failed to implicitly resolve arguments [%s] of function %s"
                                 % (", ".join(param.name for param in unresolved_params), function.__name__))

            return function(*args, **kwargs)

        return wrapper

    def __call__(self, function):
        """Decorates a function with arguments that should be resolved implicitly"""
        return self.wrap_function(function, **self.resolvers)

    def property(self, function):
        """Decorates a property with arguments that should be resolved implicitly"""
        return property(self(function))
