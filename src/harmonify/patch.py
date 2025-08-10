from .func_types import *
from .core import patch_method, create_method, delete_method
from .injector import *
import types


class Patch():
	"""A base class for creating patches to modify methods in classes."""

	# Decorators for indicating the patch target location
	@staticmethod
	def target(target_class: type, target_name: str):
		"""
		Decorator to specify the target class and method for the patch.
		Args:
			`target_class`: The class whose method is to be patched.
			`target_name`: The name of the method to be patched.
		"""
		def decorator(cls):
			cls._target_class = target_class
			cls._target_name = target_name
			return cls
		return decorator

	# All patch functions
	def prefix(self, *args, **kwds) -> tuple[Any, list, dict, str]:
		"""
		Prefix function to be called before the main method execution.
		Args:
			`self`: The instance of the class (if applicable).
			`args`: Positional arguments passed to the method.
			`kwds`: Keyword arguments passed to the method.

		Returns
			A tuple containing:
				- The return value of the prefix function (if any).
				- The modified args list.
				- The modified kwds dictionary.
				- A string indicating the flow control action (e.g., CONTINUE_EXEC, CONTINUE_WITHOUT_POSTFIX, STOP_EXEC)."""
		return None, args, kwds, 'continue'

	def postfix(self, call_result, *args, **kwds) -> Any:
		"""
		Postfix function to be called after the main method execution.
		Args:
			`self`: The instance of the class (if applicable).
			`call_result`: The result of the main method execution.
			`args`: Positional arguments passed to the method.
			`kwds`: Keyword arguments passed to the method.
		
		Returns
			The modified call result, which can be of any type.
		"""
		return call_result
	
	def replace(self, *args, **kwds) -> Any:
		"""
		Replacement function to be called instead of the main method.
		Args:
			`self`: The instance of the class (if applicable).
			`args`: Positional arguments passed to the method.
			`kwds`: Keyword arguments passed to the method.
		"""
		pass

	def create(self) -> tuple[str, "ReplaceFnType"]:
		"""
		Creates a new method to be added to the class.
		Returns:
			A tuple containing
				- The name of the new method to be created.
				- The function that will be used as the new method.
		"""
		pass

	def delete(self) -> str:
		"""
		Deletes a method from the class.
		Returns:
			The name of the deleted method.
		"""
		pass

	def inject(self) -> tuple[types.ModuleType | type, str, int, int, str]:
		"""
		Injects code into a target module or class.
		Returns:
			A tuple containing
				- The target module or class.
				- The name of the target method or function.
				- The line number to insert the code at.
				- The type of insertion (e.g., before/after).
				- The code to inject.
		"""
		return None, "", 0, 0, ""
	


def apply(patch: "Patch") -> bool:
	"""
	Applies a Harmonify patch to a method of a class.
		
	Args:
		`patch`: The `Patch` that is to be applied.
		`target`: The class whose method is to be patched. If not provided, it defaults to "__init__".
		`target_name`: The name of the method to be patched. (as a string)
	"""
	target = patch._target_class
	target_name = patch._target_name

	# Retrieve the patches into local variables
	patch_prefix = patch.prefix
	patch_postfix = patch.postfix
	patch_replace = patch.replace
	patch_create = patch.create()
	patch_delete = patch.delete()
	patch_inject = patch.inject()
	# Apply the main patch(es)
	# If the `replace` patch is marked as valid, it will be applied
	if patch.replace_valid:
		patch_success = patch_method(target, target_name, replace=patch_replace)
	else:
		patch_success = patch_method(target, target_name, patch_prefix, patch_postfix)

	create_success = True
	delete_success = True
	# Apply the creation/deletion patch(es)
	if patch_create[1]:
		create_success = create_method(target, patch_create[0], patch_create[1])
	if patch_delete:
		delete_success = delete_method(target, patch_delete)

	# Apply the injection patch
	inject_success = True
	if isinstance(patch_inject[0], types.ModuleType):
		inject_success = inject_function(patch_inject[0], patch_inject[1], patch_inject[2], patch_inject[3], patch_inject[4])
	elif isinstance(patch_inject[0], type):
		inject_success = inject_method(patch_inject[0], patch_inject[1], patch_inject[2], patch_inject[3], patch_inject[4])
	else:
		raise TypeError("Invalid target for injection, must be a module or class.")

	# Return true if all patches succeed
	return patch_success and create_success and delete_success and inject_success
