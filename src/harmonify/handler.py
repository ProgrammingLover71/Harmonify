from .core import *
from .flow_control import *
from .func_types import *
from .patch import *
from .injector import *
from .injector.security import *
from .hook import *
import sys, inspect



class Harmonify:
    def __init__(self, target_module_name: str):
        self.target_module_name = target_module_name
        # Load the target module dynamically
        self.target_module = sys.modules.get(target_module_name)
        if not self.target_module:
            raise ImportError(f"Module '{target_module_name}' not found.")
        
    def apply_all_patches(self) -> bool:
        if not self.target_module:
            return False

        for name, obj in inspect.getmembers(self.target_module):
            if inspect.isclass(obj):
                if issubclass(obj, Patch) and obj is not Patch:
                    # Load the patch class
                    patch_class = obj()
                    # Apply the patch
                    apply(patch_class)
        return True
    
    def apply_single_patch(self, name: str) -> bool:
        if not self.target_module:
            return False

        for name, obj in inspect.getmembers(self.target_module):
            if inspect.isclass(obj) and obj.__name__ == name:
                # Load the patch class
                patch_class = obj()
                # Apply the patch
                apply(patch_class)
                return True
        return False
