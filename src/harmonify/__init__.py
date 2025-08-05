from .core import *
from .flow_control import *
from .func_types import *
from .patch import *
from .injector import *
from .injector_security import *
from .hook import *
from .context import *

__version__ = "1.4.2"



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
