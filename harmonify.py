import inspect
import sys
import types
from typing import Callable, Any


class Harmonify:
    _patches = {}   # To store original methods and their patches


    @staticmethod
    def patch_method(
        target_class: type, 
        method_name: str = "__init__", 
        prefix:  "Harmonify.PrefixFnType  | None" = None, 
        postfix: "Harmonify.PostfixFnType | None" = None, 
        replace: "Harmonify.ReplaceFnType | None" = None
    ) -> bool:
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
        patch_key = (target_class, method_name)
        if patch_key not in Harmonify._patches:
            Harmonify._patches[patch_key] = original_method

        def patched_method(instance, *args, **kwds):
            flow_state = Harmonify.FlowControl.CONTINUE_EXEC   # Assume that we're continuing the execution
            result = None

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
                result, flow_state = bound_prefix(*args, **kwds)

            if flow_state != Harmonify.FlowControl.STOP_EXEC:
                # Call the original method
                # We use the stored original_method
                result = types.MethodType(original_method, instance)(*args, **kwds)

            # Call the postfix function if it exists
            if postfix and flow_state == Harmonify.FlowControl.CONTINUE_EXEC:
                # Pass instance, original method, and result to postfix
                # Postfix can modify the result
                bound_postfix = types.MethodType(postfix, instance)
                modified_result = bound_postfix(result, *args, **kwds)
                return modified_result
            
            return result

        # Replace the original method on the class
        setattr(target_class, method_name, patched_method)
        return True
    
    ##===========================================================================================##

    @staticmethod
    def patch_function(
        target_module: Any,
        function_name: str,
        prefix:  "Harmonify.PrefixFnType  | None" = None,
        postfix: "Harmonify.PostfixFnType | None" = None,
        replace: "Harmonify.ReplaceFnType | None" = None
    ) -> bool:
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

        patch_key = (target_module, function_name)
        if patch_key not in Harmonify._patches:
            Harmonify._patches[patch_key] = original_function

        def patched_function(*args, **kwds):
            flow_state = Harmonify.FlowControl.CONTINUE_EXEC
            result = None

            if replace:
                return replace(*args, **kwds)
            # Call the prefix
            if prefix:
                result, flow_state = prefix(*args, **kwds)
            # Call the original
            if flow_state != Harmonify.FlowControl.STOP_EXEC:
                result = original_function(*args, **kwds)
            # Call the postfix
            if postfix and flow_state == Harmonify.FlowControl.CONTINUE_EXEC:
                modified_result = postfix(result, *args, **kwds)
                return modified_result

            return result

        setattr(target_module, function_name, patched_function)
        return True


    ##===========================================================================================##

    @staticmethod
    def create_method(target_class: type, method_name: str, body: "Harmonify.ReplaceFnType") -> bool:
        """
        Creates a new method on a class.
        
        Args:
            `target_class`: The class that the method is being added on.
            `method_name`: The name of the method that is being added.
            `body`: The body of the method.
        """
        # No need to actually do any bounding to classes (not that we have anything to bound *to* XD)
        # A normal setattr() works too!
        setattr(target_class, method_name, body)
        return True
    

    @staticmethod
    def delete_method(target_class: type, method_name: str) -> bool:
        """
        Deletes a method on a class.
        
        Args:
            `target_class`: The class that the method is being deleted from.
            `method_name`: The name of the method that is being deleted.
        """
        # deleting is as simple as a delattr() call
        delattr(target_class, method_name)
        return True
    
    ##===========================================================================================##

    @staticmethod
    def apply(patch: "Harmonify.Patch", target_class: type, method_name: str = "__init__") -> bool:
        """
        Applies a Harmonify patch to a method of a class.
        
        Args:
            `patch`: The `Harmonify.Patch` that is to be applied.
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
        patch_success = Harmonify.patch_method(target_class, method_name, patch_prefix, patch_postfix, patch_replace)

        create_success = True
        delete_success = True
        # Apply the creation/deletion patch(es)
        if patch_create[1]:
            create_success = Harmonify.create_method(target_class, patch_create[0], patch_create[1])
        if patch_delete:
            delete_success = Harmonify.delete_method(target_class, patch_delete)
        # Return true if all patches succeed
        return patch_success and create_success and delete_success


    @staticmethod
    def unpatch(target_class: type, method_name: str = "__init__") -> bool:
        """
        Restores a patched method to its original state.
        """
        patch_key = (target_class, method_name)
        if patch_key in Harmonify._patches:
            original_method = Harmonify._patches.pop(patch_key)
            setattr(target_class, method_name, original_method)
        return True
    
    ##===========================================================================================##

    class FlowControl:
        # Continue executing original & postfix
        CONTINUE_EXEC = "continue"
        # Continue executing original, but not postfix
        CONTINUE_WITHOUT_POSTFIX = "continue_npf"
        # Don't execute anything else
        STOP_EXEC = "stop"
    
    ##===========================================================================================##

    class Patch:
        # All patch functions
        prefix:  "Harmonify.PrefixFnType  | None"
        postfix: "Harmonify.PostfixFnType | None"
        replace: "Harmonify.ReplaceFnType | None"
        create:  tuple[str, "Harmonify.ReplaceFnType | None"]
        delete:  str | None
    
    ##===========================================================================================##

    # Function type defnitions: prefix, postfix and replace.
    type PrefixFnType = Callable[..., tuple[Any, Any]]
    type PostfixFnType = Callable[..., Any]
    type ReplaceFnType = Callable[..., Any]

    ##===========================================================================================##

    @staticmethod
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

