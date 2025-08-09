import ast


class InsertType:
    """
    Enum-like class to define positions (before, after and replace) of injection.
    """
    BEFORE_TARGET = -1
    REPLACE_TARGET = 0
    AFTER_TARGET = 1



class CodeInjector(ast.NodeTransformer):
    """
    A class to inject code into a function at a specific line number.
    Replace injection works only if the code to inject is a single statement.
    """
    def __init__(self, target_code: str, insert_line: int, insert_type: int):
        super().__init__()
        self.target_code = target_code
        self.insert_line = insert_line
        self.insert_type = insert_type

    def visit_FunctionDef(self, node):
        new_node = self.generic_visit(node)

        if self.target_code:
            target_line = self.insert_line + 1
            insert_index = 0

            # Find starting place based on the line number
            for index, statement in enumerate(node.body):
                if hasattr(statement, "lineno") and statement.lineno <= target_line:
                    insert_index = index + 1
            
            # Inject the code snippet
            injected_code = ast.parse(self.target_code).body
            if self.insert_type != InsertType.REPLACE_TARGET:
                insert_index += self.insert_type
                new_node.body[insert_index:insert_index] = injected_code
            else:
                new_node.body[insert_index] = injected_code[0]

    
        return new_node
