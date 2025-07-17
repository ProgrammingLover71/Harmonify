import types
from typing import Callable, Any


class Harmonify:
    _patches = {} # To store original methods and their patches


    @staticmethod
    def patch(
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

        def patched_method(instance, *args, **kwargs):
            flow_state = Harmonify.FlowControl.CONTINUE_EXEC   # Assume that we're continuing the execution
            result = None

            # This is the new method that will replace the original
            # It will handle calling prefix, original, and postfix

            # If 'replace' function is provided, it completely takes over
            if replace:
                # We need to bind 'replace' to the instance so it acts like a method
                # This makes 'self' work inside the replacement function
                bound_replace = types.MethodType(replace, instance)
                return bound_replace(*args, **kwargs)

            # Call the prefix function if it exists
            if prefix:
                # Pass instance, original method, and arguments to prefix
                # Prefix can modify arguments or even return a result to skip the original or both original and postfix.
                bound_prefix = types.MethodType(prefix, instance)
                result, flow_state = bound_prefix(*args, **kwargs)

            if flow_state != Harmonify.FlowControl.STOP_EXEC:
                # Call the original method
                # We use the stored original_method
                result = types.MethodType(original_method, instance)(*args, **kwargs)

            # Call the postfix function if it exists
            if postfix and flow_state == Harmonify.FlowControl.CONTINUE_EXEC:
                # Pass instance, original method, and result to postfix
                # Postfix can modify the result
                bound_postfix = types.MethodType(postfix, instance)
                modified_result = bound_postfix(result, *args, **kwargs)
                return modified_result
            
            return result

        # Replace the original method on the class
        setattr(target_class, method_name, patched_method)
        return True
    
    ##===========================================================================================##

    @staticmethod
    def create_method(target_class: type, method_name: str, body: "Harmonify.ReplaceFnType") -> bool:
        """
        Creates and binds a new method on a class.
        
        Args:
            `target_class`: The class that the method is being added on.
            `method_name`: The name of the method that is being added.
            `body`: The body of the method.
        """
        bound_method = types.MethodType(body, target_class)
        setattr(target_class, method_name, bound_method)
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
        patch_prefix = patch.prefix
        patch_postfix = patch.postfix
        patch_replace = patch.replace
        return Harmonify.patch(target_class, method_name, patch_prefix, patch_postfix, patch_replace)


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
    
    ##===========================================================================================##

    # Function type defnitions: prefix, postfix and replace.
    type PrefixFnType = Callable[..., tuple[Any, Any]]
    type PostfixFnType = Callable[..., Any]
    type ReplaceFnType = Callable[..., Any]
