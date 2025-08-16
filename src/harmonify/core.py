from .flow_control import FlowControlError, CONTINUE_EXEC, CONTINUE_WITHOUT_POSTFIX, STOP_EXEC
from .func_types import *
import sys, inspect, types
from .info_utils import *



_method_patches = {}   # To store original methods and their patches
_function_patches = {}

n = 0
def new_id():
	global n
	n += 1
	return n


def patch_method(
	target_class: type, 
	method_name: str = "__init__", 
	prefix:  "PrefixFnType  | None" = None, 
	postfix: "PostfixFnType | None" = None, 
	replace: "ReplaceFnType | None" = None
) -> tuple[bool, int]:
	"""
	Patches a method of a class.

	Args:
		`target_class`: The class whose method is to be patched.
		`method_name`: The name of the method to be patched (as a string). If not provided, it defaults to "__init__".
		`prefix`: A function to run *before* the original method. (optional)
		`postfix`: A function to run *after* the original method. (optional)
		`replace`: A function to completely *replace* the original method. (optional)
	"""
	original_method = getattr(target_class, method_name, None)
	if not callable(original_method):
		return False

	# Store the original method so we can restore it later
	# We'll use a unique key for each patched method
	patch_key = (target_class, method_name, new_id())
	if patch_key not in _method_patches:
		_method_patches[patch_key] = original_method

	def patched_method(instance, *args, **kwds):
		flow_state = CONTINUE_EXEC   # Assume that we're continuing the execution
		result = None

		new_args, new_kwds = args, kwds

		# This is the new method that will replace the original
		# It will handle calling prefix, original, and postfix

		# If 'replace' function is provided, it completely takes over
		if replace:
			# We need to bind 'replace' to the instance so it acts like a method
			# This makes 'self' work inside the replacement function
			bound_replace = types.MethodType(replace, instance)
			return bound_replace(*args, **kwds)

		# Call the prefix function if it exists
		if prefix:
			# Pass instance, original method, and arguments to prefix
			# Prefix can modify arguments or even return a result to skip the original or both original and postfix.
			bound_prefix = types.MethodType(prefix, instance)
			result, new_args, new_kwds, flow_state = bound_prefix(*args, **kwds)

		if flow_state != STOP_EXEC:
			# Call the original method
			# We use the stored original_method
			result = types.MethodType(original_method, instance)(*new_args, **new_kwds)

		# Call the postfix function if it exists
		if postfix and flow_state == CONTINUE_EXEC:
			# Pass instance, original method, and result to postfix
			# Postfix can modify the result
			bound_postfix = types.MethodType(postfix, instance)
			modified_result = bound_postfix(result, *args, **kwds)
			return modified_result

		raise FlowControlError(flow_state)

	# Replace the original method on the class
	setattr(target_class, method_name, patched_method)
	return True, patch_key[2]
	


def patch_function(
	target_module: types.ModuleType,
	function_name: str,
	prefix:  "PrefixFnType  | None" = None,
	postfix: "PostfixFnType | None" = None,
	replace: "ReplaceFnType | None" = None
) -> tuple[bool, int]:
	"""
	Patches a standalone function in a module.

	Args:
		`target_module`: The module object where the function is defined.
		`function_name`: The name of the function to patch.
		`prefix`: A function to run *before* the original function.
		`postfix`: A function to run *after* the original function.
		`replace`: A function to completely *replace* the original function.
	"""
	original_function = getattr(target_module, function_name, None)
	if not callable(original_function):
		return False

	patch_key = (target_module, function_name, new_id())
	if patch_key not in _function_patches:
		_function_patches[patch_key] = original_function

	def patched_function(*args, **kwds):
		flow_state = CONTINUE_EXEC
		result = None

		if replace:
			return replace(*args, **kwds)
		# Call the prefix
		if prefix:
			result, new_args, new_kwds, flow_state = prefix(*args, **kwds)
		# Call the original
		if flow_state != STOP_EXEC:
			result = original_function(*new_args, **new_kwds)
		# Call the postfix
		if postfix and flow_state == CONTINUE_EXEC:
			modified_result = postfix(result, *args, **kwds)
			return modified_result
		
		raise FlowControlError(flow_state)

	setattr(target_module, function_name, patched_function)
	return True, patch_key[2]



def create_method(target_class: type, method_name: str, body: Callable[..., Any]) -> bool:
	"""
	Creates a new method on a class.
	
	Args:
		`target_class`: The class that the method is being added on.
		`method_name`: The name of the method that is being added.
		`body`: The body of the method.
	"""
	# No need to actually do any bounding to classes (not that we have any instance to bound to anyways :D)
	# A normal setattr() works too!
	if target_class is None: return False
	setattr(target_class, method_name, body)
	return True



def create_function(target_module: type, function_name: str, body: Callable[..., Any]) -> bool:
	"""
	Creates a new function on a module.
	
	Args:
		`target_module`: The module that the method is being added on.
		`function_name`: The name of the function that is being added.
		`body`: The body of the function.
	"""
	# A normal setattr() works too!
	if target_module is None: return False
	setattr(target_module, function_name, body)
	return True
	


def delete_method(target_class: type, method_name: str) -> bool:
	"""
	Deletes a method on a class.
	
	Args:
		`target_class`: The class that the method is being deleted from.
		`method_name`: The name of the method that is being deleted.
	"""
	# deleting is as simple as a delattr() call
	if target_class is None: return False
	delattr(target_class, method_name)
	return True



def delete_function(target_module: types.ModuleType, function_name: str) -> bool:
	"""
	Deletes a function from a module.

	Args:
		`target_module`: The module that the function is being deleted from.
		`function_name`: The name of the function that is being deleted.
	"""
	# deleting is as simple as a delattr() call
	if target_module is None: return False
	delattr(target_module, function_name)
	return True



def unpatch_method(target_class: type, method_name: str, index: int = 1) -> bool:
	"""
	Restores a patched method to its original state.
	"""
	patch_key = (target_class, method_name, index)
	if patch_key in _method_patches:
		original_method = _method_patches.pop(patch_key)
		setattr(target_class, method_name, original_method)
		return True
	return False



def unpatch_function(target_module: types.ModuleType, method_name: str, index: int = 1) -> bool:
	"""
	Restores a patched method to its original state.
	"""
	patch_key = (target_module, method_name, index)
	if patch_key in _function_patches:
		original_method = _function_patches.pop(patch_key)
		setattr(target_module, method_name, original_method)
		return True
	return False



def get_current_module() -> types.ModuleType | None:
    """
    Returns the module object of the immediate caller (i.e., the module from which this function is called).<br>
    Returns `None` if not possible.
    """
    frame = inspect.currentframe()
    if frame is None:
        return None

    try:
        caller_frame = frame.f_back
        module_name = caller_frame.f_globals.get("__name__")
        if module_name:
            return sys.modules.get(module_name)
        return None
    finally:
        # Clean up frame references to avoid reference cycles
        del frame
        del caller_frame



def get_function_patches() -> list[PatchInfo]:
	"""
	Returns a list containing all applied patches for functions.<br>
	Returns an empty list (i.e. `[]`) if no patches have been applied yet.
	"""
	patches = []
	for patch_key, original in _function_patches.items():
		(target_mod, func_name, patch_idx) = patch_key
		patches.append(PatchInfo(target_mod, func_name, patch_idx, original))
	return patches



def get_method_patches() -> list[PatchInfo]:
	"""
	Returns a list containing all applied patches for methods.<br>
	Returns an empty list (i.e. `[]`) if no patches have been applied yet.
	"""
	patches = []
	for patch_key, original in _method_patches.items():
		(target_cls, method_name, patch_idx) = patch_key
		patches.append(PatchInfo(target_cls, method_name, patch_idx, original))
	return patches
