from .core import *
from .injector import *
from .hook import *


class PatchManager:
    """
    A context manager for applying patches to functions or methods.
    This class allows you to apply patches to functions or methods within a context,
    ensuring that the original functionality is restored when exiting the context.
    """

    def __init__(
            self, 
            target: types.ModuleType | type, 
            callable_name: str, 
            prefix: PrefixFnType | None = None, 
            postfix: PostfixFnType | None = None,
            replace: ReplaceFnType | None = None,
            create: ReplaceFnType | None = None
        ):
        self.target = target
        self.callable_name = callable_name
        self.prefix = prefix
        self.postfix = postfix
        self.replace = replace
        self.create = create
    
    def __enter__(self):
        if isinstance(self.target, types.ModuleType):
            patch_function(
                self.target,
                self.callable_name,
                prefix=self.prefix,
                postfix=self.postfix,
                replace=self.replace
            )
        elif isinstance(self.target, type):
            patch_method(
                self.target,
                self.callable_name,
                prefix=self.prefix,
                postfix=self.postfix,
                replace=self.replace,
                create=self.create
            )
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if isinstance(self.target, types.ModuleType):
            unpatch_function(self.target, self.callable_name)
        elif isinstance(self.target, type):
            unpatch_method(self.target, self.callable_name)



class InjectManager:
    """
    A context manager for applying dependency injection to functions or methods.
    This class allows you to inject dependencies into functions or methods within a context,
    ensuring that the original functionality is restored when exiting the context.
    """

    def __init__(
            self,
            target: types.ModuleType | type,
            callable_name: str,
            inject_after_line: int = 0,
            code_to_inject: str | None = None
        ):
        self.target = target
        self.callable_name = callable_name
        self.inject_after_line = inject_after_line
        self.code_to_inject = code_to_inject
    
    def __enter__(self):
        if isinstance(self.target, types.ModuleType):
            inject_function(
                self.target,
                self.callable_name,
                self.inject_after_line,
                self.code_to_inject
            )
        elif isinstance(self.target, type):
            inject_method(
                self.target,
                self.callable_name,
                self.inject_after_line,
                self.code_to_inject
            )
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if isinstance(self.target, types.ModuleType):
            undo_func_inject(self.target, self.callable_name)
        elif isinstance(self.target, type):
            undo_method_inject(self.target, self.callable_name)



class HookManager:
    """
    A context manager for applying hooks to functions or methods.
    This class allows you to apply hooks to functions or methods within a context,
    ensuring that the original functionality is restored when exiting the context.
    """

    def __init__(
            self,
            target: types.ModuleType | type,
            callable_name: str,
            hook_callback: typing.Callable
        ):
        self.target = target
        self.callable_name = callable_name
        self.hook_callback = hook_callback
    
    def __enter__(self):
        if isinstance(self.target, types.ModuleType):
            register_function_hook(self.target, self.callable_name, self.hook_callback)
        elif isinstance(self.target, type):
            register_method_hook(self.target, self.callable_name, self.hook_callback)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if isinstance(self.target, types.ModuleType):
            remove_function_hook(self.target, self.callable_name, self.hook_callback)
        elif isinstance(self.target, type):
            remove_method_hook(self.target, self.callable_name, self.hook_callback)
