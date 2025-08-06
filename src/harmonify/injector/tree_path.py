import ast


class TreePath:
    def __init__(self, *branches):
        self.branches = branches
    
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
        current = root
        for branch in self.branches:
            body_field = self._get_body_field(current)
            if not (0 <= branch < len(body_field)):
                raise IndexError(f"Branch {branch} is out of range for node {ast.dump(current)}.")
            current = body_field[branch]
        return current
