import ast
import inspect
import textwrap
import types

from .injector.utils import *
from . import injector_security as sec

_func_injections = {}
_method_injections = {}


def inject_function(
    target_module: types.ModuleType,
    function_name: str,
    insert_after_line: int = 0,
    code_to_inject: str | None = None
):
    """
    Inject the specified code snippet in the targeted function's source (at runtime).<br>
    If the function has a "no_inject" attribute set to True, then this will not do anything.<br>
    **Note**: This is very dangerous and allows programmmers to run *unsandboxed code*!
    
    Args:
        `target_module`: The module in which the targeted function exists.
        `function_name`: The name of the targeted function.
        `insert_after_line`: The line number (relative to the function definition) after which the code will be injected.
        `code_to_inject`: The code snippet that will be injected.
    """
    target_function = getattr(target_module, function_name)
    if isinstance(target_function, sec.no_inject):
        return False
    
    if isinstance(target_function, sec.allow_inject):
        target_function = target_function.func
    
    function_source = textwrap.dedent(inspect.getsource(target_function))
    function_ast = ast.parse(function_source)
    
    # Transform the function's AST
    injector = CodeInjectorLineNumber(insert_after_line=insert_after_line, code_to_inject=code_to_inject)
    new_ast = injector.visit(function_ast)
    ast.fix_missing_locations(new_ast)   # Fix the AST's line numbers and positions

    # Compile the new function and rebind it
    compiled_func = compile(new_ast, filename=target_module.__name__, mode="exec")
    namespace = target_function.__globals__.copy()
    exec(compiled_func, namespace)

    new_function = namespace[function_name]

    # Keep track of the injection
    inject_key = (target_module, function_name)
    inject_value = (target_function, new_function)
    if inject_key not in _func_injections:
        _func_injections[inject_key] = inject_value

    # Replace the function in its original spot
    setattr(target_module, function_name, new_function)
    return True



def undo_func_inject(
    target_module: types.ModuleType,
    function_name: str
):
    """
    Revert the injected function back to its original code.

    Args:
        `target_module`: The module where the targeted function exists.
        `function_name`: The name of the targeted function.
    """
    inject_key = (target_module, function_name)
    if inject_key in _func_injections:
        original_function = _func_injections[inject_key][0]
        setattr(target_module, function_name, original_function)
    return True



def inject_method(
    target_class: type,
    method_name: str = "__init__",
    insert_after_line: int = 0,
    code_to_inject: str | None = None
):
    """
    Inject the specified code snippet in the targeted method's source (at runtime).<br>
    If the function has a "no_inject" attribute set to True, then this will not do anything.<br>
    **Note**: This is very dangerous and allows programmmers to run *unsandboxed code*!
    
    Args:
        `target_module`: The module in which the targeted method exists.
        `method_name`: The name of the targeted method.
        `insert_after_line`: The line number (relative to the method definition) after which the code will be injected.
        `code_to_inject`: The code snippet that will be injected.
    """
    target_method = getattr(target_class, method_name)
    if isinstance(target_method, sec.no_inject):
        return False
    
    if isinstance(target_method, sec.allow_inject):
        target_method = target_method.func

    # Handle method wrappers
    is_classmethod = isinstance(inspect.getattr_static(target_class, method_name), classmethod)
    is_staticmethod = isinstance(inspect.getattr_static(target_class, method_name), staticmethod)


    method_source = textwrap.dedent(inspect.getsource(target_method))
    method_ast = ast.parse(method_source)
    
    # Transform the method's AST
    injector = CodeInjectorLineNumber(insert_after_line=insert_after_line, code_to_inject=code_to_inject)
    new_ast = injector.visit(method_ast)
    ast.fix_missing_locations(new_ast)   # Fix the AST's line numbers and positions

    # Compile the new method and rebind it
    compiled_func = compile(new_ast, filename=target_class.__module__, mode="exec")
    namespace = target_method.__globals__.copy()
    exec(compiled_func, namespace)

    new_method = namespace[method_name]

    # Re-wrap if needed
    if is_classmethod: new_method = classmethod(new_method)
    elif is_staticmethod: new_method = staticmethod(new_method)

    # Keep track of the injection
    inject_key = (target_class, method_name)
    inject_value = (target_method, new_method)
    if inject_key not in _method_injections:
        _method_injections[inject_key] = inject_value

    # Replace the method in its original spot
    setattr(target_class, method_name, new_method)
    return True



def undo_method_inject(
    target_class: type,
    method_name: str
):
    """
    Revert the injected method back to its original code.

    Args:
        `target_class`: The class where the targeted method exists.
        `method_name`: The name of the targeted method.
    """
    inject_key = (target_class, method_name)
    if inject_key in _method_injections:
        original_method = _method_injections[inject_key][0]
        setattr(target_class, method_name, original_method)
    return True


