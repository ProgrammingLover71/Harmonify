import functools, types



class HarmonifyDecorator:
    """
    Base Harmonify decorator class.<br>
    Extended by `no_inject` and `allow_inject`.
    """
    def __init__(self, func):
        self.func = func
        # Copy metadata from the original function
        functools.update_wrapper(self, func)

    def __call__(self, *args, **kwds):
        return self.func(*args, **kwds)

    # Implement _get_ for methods (when the decorator is applied to a method)
    # This allows the decorated method to be bound correctly to its instance.
    def __get__(self, instance, owner):
        if instance is None:
            return self # Accessing the decorator directly from the class
        
        # Return a bound method that refers to our wrapped function
        return types.MethodType(self, instance)



class no_inject(HarmonifyDecorator):
    """
    Class-based decorator to mark a function or method as not allowing Harmonify injection.
    """
    def __init__(self, func):
        super().__init__(func)

        

class allow_inject(HarmonifyDecorator):
    """
    Class-based decorator to mark a function or method as allowing Harmonify injection.
    """
    def __init__(self, func):
        super().__init__(func)

