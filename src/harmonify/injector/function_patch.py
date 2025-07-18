import ast
import inspect
import textwrap
import types

_injections = {}


def inject_function(
    target_module: types.ModuleType,
    function_name: str,
    insert_after_line: int = 0,
    code_to_inject: str | None = None
):
    """
    Inject the specified code snippet in the targeted function's source (at runtime).
    
    Args:
        `target_module`: The module in which the targeted function exists.
        `function_name`: The name of the targeted function.
        `insert_after_line`: The line number (relative to the function definition) after which the code will be injected.
        `code_to_inject`: The code snippet that will be injected.
    """
    target_function = getattr(target_module, function_name)
    function_source = textwrap.dedent(inspect.getsource(target_function))
    function_ast = ast.parse(function_source)

    class CodeInjector(ast.NodeTransformer):
        def visit_FunctionDef(self, node):
            new_node = self.generic_visit(node)

            if code_to_inject:
                target_line = insert_after_line
                insert_index = 0

                # Find starting place based on the line number
                for index, statement in enumerate(node.body):
                    if hasattr(statement, "lineno") and statement.lineno <= target_line:
                        insert_index = index + 1
                
                # Inject the code snippet
                injected_code = ast.parse(code_to_inject).body
                new_node.body[insert_index:insert_index] = injected_code
            
            return new_node
    
    # Transform the function's AST
    injector = CodeInjector()
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
    if inject_key not in _injections:
        _injections[inject_key] = inject_value

    # Replace the function in its original spot
    setattr(target_module, function_name, new_function)



def inject_method(
    target_class: type,
    method_name: str = "__init__",
    insert_after_line: int = 0,
    code_to_inject: str | None = None
):
    """
    Inject the specified code snippet in the targeted method's source (at runtime).
    
    Args:
        `target_module`: The module in which the targeted method exists.
        `method_name`: The name of the targeted method.
        `insert_after_line`: The line number (relative to the method definition) after which the code will be injected.
        `code_to_inject`: The code snippet that will be injected.
    """
    target_method = getattr(target_class, method_name)

    # Handle method wrappers
    is_classmethod = isinstance(inspect.getattr_static(target_class, method_name), classmethod)
    is_staticmethod = isinstance(inspect.getattr_static(target_class, method_name), staticmethod)


    method_source = textwrap.dedent(inspect.getsource(target_method))
    method_ast = ast.parse(method_source)

    class CodeInjector(ast.NodeTransformer):
        def visit_FunctionDef(self, node):
            new_node = self.generic_visit(node)

            if code_to_inject:
                target_line = insert_after_line
                insert_index = 0

                # Find starting place based on the line number
                for index, statement in enumerate(node.body):
                    if hasattr(statement, "lineno") and statement.lineno <= target_line:
                        insert_index = index + 1
                
                # Inject the code snippet
                injected_code = ast.parse(code_to_inject).body
                new_node.body[insert_index:insert_index] = injected_code
            
            return new_node
    
    # Transform the method's AST
    injector = CodeInjector()
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
    if inject_key not in _injections:
        _injections[inject_key] = inject_value

    # Replace the method in its original spot
    setattr(target_class, method_name, new_method)
