import ast
from platform import node


class TreePath:
    """
    A class to represent a path through the AST.
    The path is defined by a starting index and a series of steps.
    Each step is an index into the body of the current node. <br>

    This class allows for flexible navigation through the AST,
    and is primarily used for locating specific nodes when injecting code.
    """
    def __init__(self, start, *steps):
        self.start = start
        self.steps = steps
    
    def _get_body_field(self, node: ast.stmt):
        """
        Returns the body field of the node if it exists.
        If the node does not have a body field, it raises an AttributeError.
        """
        SUPPORTED_BODY_FIELDS = {"body", "orelse", "finalbody", "handlers"}
        for field in SUPPORTED_BODY_FIELDS:
            value = getattr(node, field, None)
            if isinstance(value, list):
                return value
        raise AttributeError(f"Node {ast.dump(node)} ({type(node).__name__}) has no supported body field.")

    def walk(self, root: ast.stmt) -> ast.stmt:
        """
        Walk through the AST node and return the target node based on the path.
        """
        current = self.walk_step(root, self.start)
        for step in self.steps:
            current = self.walk_step(current, step)
        return current
    
    def walk_step(self, node: ast.stmt, step: int) -> ast.stmt:
        """
        Walk one step in the AST node based on the step index.
        Raises IndexError if the step is out of range.
        """
        body_field = self._get_body_field(node)
        if not (0 <= step < len(body_field)):
            raise IndexError(f"step {step} is out of range for node {ast.dump(node)}.")
        return body_field[step]
