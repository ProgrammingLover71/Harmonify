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
            replace: ReplaceFnType | None = None
        ):
        self.target = target
        self.callable_name = callable_name
        self.prefix = prefix
        self.postfix = postfix
        self.replace = replace
    
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
                replace=self.replace
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
            insert_line: int,
            insert_type: int,
            code_to_inject: str | None = None
        ):
        self.target = target
        self.callable_name = callable_name
        self.insert_line = insert_line
        self.insert_type = insert_type
        self.code_to_inject = code_to_inject
    
    def __enter__(self):
        if isinstance(self.target, types.ModuleType):
            inject_function(
                self.target,
                self.callable_name,
                self.insert_line,
                self.insert_type,
                self.code_to_inject
            )
        elif isinstance(self.target, type):
            inject_method(
                self.target,
                self.callable_name,
                self.insert_line,
                self.insert_type,
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
            hook_callback: typing.Callable,
            hook_id: str
        ):
        self.target = target
        self.callable_name = callable_name
        self.hook_callback = hook_callback
        self.hook_id = hook_id
    
    def __enter__(self):
        if isinstance(self.target, types.ModuleType):
            register_function_hook(self.target, self.callable_name, self.hook_callback, self.hook_id)
        elif isinstance(self.target, type):
            register_method_hook(self.target, self.callable_name, self.hook_callback, self.hook_id)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if isinstance(self.target, types.ModuleType):
            remove_function_hook(self.target, self.callable_name, self.hook_callback, self.hook_id)
        elif isinstance(self.target, type):
            remove_method_hook(self.target, self.callable_name, self.hook_callback, self.hook_id)



def apply_patch(
    target: types.ModuleType | type,
    callable_name: str,
    prefix: PrefixFnType | None = None,
    postfix: PostfixFnType | None = None,
    replace: ReplaceFnType | None = None
) -> PatchManager:
    return PatchManager(
        target,
        callable_name,
        prefix=prefix,
        postfix=postfix,
        replace=replace
    )


def apply_inject(
    target: types.ModuleType | type,
    callable_name: str,
    insert_line: int,
    insert_type: int,
    code_to_inject: str | None = None
) -> InjectManager:
    return InjectManager(
        target,
        callable_name,
        insert_line=insert_line,
        insert_type=insert_type,
        code_to_inject=code_to_inject
    )


def add_hook(
    target: types.ModuleType | type,
    callable_name: str,
    hook_callback: typing.Callable,
    hook_id: str
) -> HookManager:
    return HookManager(
        target,
        callable_name,
        hook_callback,
        hook_id
    )
