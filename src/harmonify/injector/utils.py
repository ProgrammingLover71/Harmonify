import ast
from .tree_path import *


class CodeInjectorLineNumber(ast.NodeTransformer):
    """
    A class to inject code into a function at a specific line number.
    """
    def __init__(self, code_to_inject: str, insert_after_line: int):
        super().__init__()
        self.code_to_inject = code_to_inject
        self.insert_after_line = insert_after_line

    def visit_FunctionDef(self, node):
        new_node = self.generic_visit(node)

        if self.code_to_inject:
            target_line = self.insert_after_line + 1
            insert_index = 0

            # Find starting place based on the line number
            for index, statement in enumerate(node.body):
                if hasattr(statement, "lineno") and statement.lineno <= target_line:
                    insert_index = index + 1
                
            # Inject the code snippet
            injected_code = ast.parse(self.code_to_inject).body
            new_node.body[insert_index:insert_index] = injected_code
            
        return new_node


### New classes for injection based on tree paths ###


class InjectType:
    """
    Enum-like class to define types of injection.
    """
    BEFORE_TARGET = -1
    REPLACE_TARGET = 0
    AFTER_TARGET = 1


class CodeInjectorTreePath(ast.NodeTransformer):
    """
    A class to inject code into a function at a specific AST node path.
    """
    def __init__(self, path: TreePath, typ: InjectType, code_to_inject: str):
        super().__init__()
        self.path = path
        self.typ = typ
        self.code_to_inject = code_to_inject

    def visit_FunctionDef(self, node):
        new_node = self.generic_visit(node)

        if self.path:
            target_stmt = self.path.walk(new_node)
            ln = target_stmt.lineno
            # Modify the line number based on the injection type
            if self.typ != InjectType.REPLACE_TARGET:
                if self.typ == InjectType.BEFORE_TARGET: ln -= 1
                elif self.typ == InjectType.AFTER_TARGET: pass
                # Use the line number injector to inject the code
                injector = CodeInjectorLineNumber(self.code_to_inject, ln)
                new_node = injector.visit(new_node)
            else:
                # Replace the target statement with the injected code
                if self.code_to_inject:
                    injected_code = ast.parse(self.code_to_inject).body
                    # Get the index of the target statement -- default to the first one
                    try:
                        insert_index = new_node.body.index(target_stmt)
                        new_node.body.remove(target_stmt)
                    except ValueError:
                        insert_index = 0
                    # Inject the code snippet at the target index
                    new_node.body[insert_index:insert_index] = injected_code
            
        return new_node