import types

class Harmonify:
    _patches = {} # To store original methods and their patches

    @staticmethod
    def patch(target_class, method_name, prefix=None, postfix=None, replace=None):
        """
        Patches a method of a class.

        Args:
            target_class: The class whose method is to be patched.
            method_name: The name of the method to be patched (as a string).
            prefix: A function to run *before* the original method. (optional)
            postfix: A function to run *after* the original method. (optional)
            replace: A function to completely *replace* the original method. (optional)
        """
        original_method = getattr(target_class, method_name)

        if not callable(original_method):
            raise TypeError(f"'{method_name}' is not a callable method on {target_class.__name__}")

        # Store the original method so we can restore it later
        # We'll use a unique key for each patched method
        patch_key = (target_class, method_name)
        if patch_key not in Harmonify._patches:
            Harmonify._patches[patch_key] = original_method

        def patched_method(instance, *args, **kwargs):
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
                # Prefix can modify arguments or even return a result to skip original
                # For simplicity here, we'll just call it.
                # In a more advanced library, prefix could return special values to control flow.
                bound_prefix = types.MethodType(prefix, instance)
                bound_prefix(*args, **kwargs)

            # Call the original method
            # We use the stored original_method
            result = types.MethodType(original_method, instance)(*args, **kwargs)

            # Call the postfix function if it exists
            if postfix:
                # Pass instance, original method, and result to postfix
                # Postfix can modify the result
                bound_postfix = types.MethodType(postfix, instance)
                modified_result = bound_postfix(result, *args, **kwargs)
                return modified_result
            
            return result

        # Replace the original method on the class
        setattr(target_class, method_name, patched_method)
        print(f"Patched '{method_name}' on {target_class.__name__}")

    @staticmethod
    def unpatch(target_class, method_name):
        """
        Restores a patched method to its original state.
        """
        patch_key = (target_class, method_name)
        if patch_key in Harmonify._patches:
            original_method = Harmonify._patches.pop(patch_key)
            setattr(target_class, method_name, original_method)
            print(f"Unpatched '{method_name}' on {target_class.__name__}")
        else:
            print(f"No patch found for '{method_name}' on {target_class.__name__}")
