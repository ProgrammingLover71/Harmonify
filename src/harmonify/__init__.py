from harmonify.core import *
from harmonify.flow_control import *
from harmonify.func_types import *
from harmonify.patch import *
from harmonify.injector import *
from harmonify.injector.security import *
from harmonify.hook import *
from harmonify.context import *

import harmonify.old_injector as old_injector   # For backward compatibility

__version__ = "2.0.0rc1"



def apply_patch(
    target: types.ModuleType | type,
    callable_name: str,
    prefix: PrefixFnType | None = None,
    postfix: PostfixFnType | None = None,
    replace: ReplaceFnType | None = None,
    create: ReplaceFnType | None = None
) -> bool:
    return PatchManager(
        target,
        callable_name,
        prefix=prefix,
        postfix=postfix,
        replace=replace,
        create=create
    )


def apply_inject(
    target: types.ModuleType | type,
    callable_name: str,
    inject_after_line: int = 0,
    code_to_inject: str | None = None
) -> bool:
    return InjectManager(
        target,
        callable_name,
        inject_after_line=inject_after_line,
        code_to_inject=code_to_inject
    )


def add_hook(
    target: types.ModuleType | type,
    callable_name: str,
    hook_callback: typing.Callable
) -> bool:
    return HookManager(
        target,
        callable_name,
        hook_callback
    )
