class PatchInfo:
    """Holds informathion about a patch."""
    def __init__(self, parent, target, patch_index: int, original):
        self.parent = parent
        self.target = target
        self.patch_index = patch_index
        self.original = original
