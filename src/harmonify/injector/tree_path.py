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
        body_field = node.body
        if not (0 <= step < len(body_field)):
            raise IndexError(f"step {step} is out of range for node {ast.dump(node)}.")
        return body_field[step]
