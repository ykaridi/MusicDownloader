from traceback import walk_stack

from utils import ImplicitResolution


class ScopeResolver(ImplicitResolution):
    """
    Resolves parameters by scope, the first of the following will be used
    - First parameter contains an attribute with the name of the parameter it will be used
    - One of the local contexts (reverse call-stack order) contains a variable with the name of the parameter
    - One of the global contexts (call-stack order) contains a VARIABLE with the name of the parameter
    """

    @staticmethod
    def resolver(param: str):
        param = param.lower()

        def resolve(self=None, *args, **kwargs):
            if hasattr(self, param):
                return getattr(self, param)

            for frame in tuple(frame for frame, _ in walk_stack(None))[2:]:
                if param in frame.f_locals:
                    return frame.f_locals[param]

            for frame in reversed(tuple(frame for frame, _ in walk_stack(None))[2:]):
                if param.upper() in frame.f_globals:
                    return frame.f_globals[param.upper()]

            return None

        return resolve

    def __init__(self, *parameters: str):
        super(ScopeResolver, self).__init__(**{parameter: self.resolver(parameter) for parameter in parameters})
        object.__setattr__(self, 'parameters', parameters)
