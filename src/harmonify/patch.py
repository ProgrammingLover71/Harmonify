from .func_types import *
from .core import patch_method, create_method, delete_method

class Patch:
	# All patch functions
	prefix:  "PrefixFnType  | None"
	postfix: "PostfixFnType | None"
	replace: "ReplaceFnType | None"
	create:  tuple[str, "ReplaceFnType | None"]
	delete:  str | None


def apply(patch: "Patch", target_class: type, method_name: str = "__init__") -> bool:
    """
    Applies a Harmonify patch to a method of a class.
        
    Args:
        `patch`: The `Patch` that is to be applied.
        `target_class`: The class whose method is to be patched. If not provided, it defaults to "__init__".
        `method_name`: The name of the method to be patched. (as a string)
    """
    # Retrieve the patches into local variables
    patch_prefix = patch.prefix
    patch_postfix = patch.postfix
    patch_replace = patch.replace
    patch_create = patch.create
    patch_delete = patch.delete
    # Apply the main patch(es)
    patch_success = patch_method(target_class, method_name, patch_prefix, patch_postfix, patch_replace)

    create_success = True
    delete_success = True
    # Apply the creation/deletion patch(es)
    if patch_create[1]:
        create_success = create_method(target_class, patch_create[0], patch_create[1])
    if patch_delete:
        delete_success = delete_method(target_class, patch_delete)
    # Return true if all patches succeed
    return patch_success and create_success and delete_success