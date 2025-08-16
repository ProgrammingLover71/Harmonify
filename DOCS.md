# Harmonify - Documentation (3.1.2)
This document will provide users with detailed explanations on every public Harmonify function/class.
Harmonify is a Python library that allows users to change the behavior of classes at runtime, with nothing more than a few function calls.
Inspired by Harmony (the *very* popular C# library that also allows runtime behavior modification), Harmonify is flexible and uses a simple system based on monkey-patching.

# Module - `harmonify.core`

### Function: `harmonify.core.patch_method(...)`

- Arguments:
    - `target_class` (`type`): The class the contains the target method. For example, if the user wants to patch `Foo.bar()`, then `target_class = Foo`
    - `method_name` (`str`): The name of the target method. In the previous example, `target_method = "bar"`
    - `prefix` (`PrefixFnType`*): The prefix function that will be applied (can be `None`). After the call to `patch_method`, this function will be called before the original method executes
    - `postfix` (`PostfixFnType`*): The postfix function that will be applied (can be `None`). After the call to `patch_method`, this function will be called after the original method executes
    - `replace` (`ReplaceFnType`*): A new method that can be provided to replace the old one entirely. If given, the `prefix` and `postfix` arguments are not considered <br>

\* These types will be explained in the `harmonify.func_types` module.

- Returns: A `tuple[bool, int]` describing whether the operation was successful (if the patch could be applied) and the index of the patch (which is required for unpatching)

```python
class Player:
    def __init__(self, age: int):
        self.age = age
        self.hp = 100
        self.dmg = 5
    
    def is_adult(self):
        return self.age > 21

import harmonify

# This will be called after `Player.__init__()`
def init_postfix(obj_self, call_result, *args, **kwds):
    obj_self.hp *= 1.2      # Add a 20% HP boost
    obj_self.dmg = 3        # Subtract 40% from damage
    return obj_self   # This is what __init__ returns. Yes, you can use patches to change what __init__ returns!

_, pid1 = harmonify.patch_method(
    target_class = Player,
    method_name = "__init__",
    postfix = init_postfix
)

# This will replace the is_adult method entirely
def is_adult_rep(obj_self, *args, **kwds):
    return obj_self.age > 18   # Maybe the player is european!

_, pid2 = harmonify.patch_method(
    target_class = Player,
    method_name = "is_adult",
    postfix = is_adult_rep
)
```

<br>
<br>

### Function: `harmonify.core.patch_function(...)`

- Arguments:
    - `target_module` (`types.ModuleType`): The module the contains the target function. For example, if the user wants to patch `builtins.print(...)`, then `target_module = builtins`
    - `function_name` (`str`): The name of the target function. In the previous example, `target_function = "print"`
    - `prefix` (`PrefixFnType`): The prefix function that will be applied (can be `None`). After the call to `patch_function`, this function will be called before the original function executes
    - `postfix` (`PostfixFnType`): The postfix function that will be applied (can be `None`). After the call to `patch_function`, this function will be called after the original function executes
    - `replace` (`ReplaceFnType`*): A new method that can be provided to replace the old one entirely. If given, the `prefix` and `postfix` arguments are not considered <br>

\* These types will be explained in the `harmonify.func_types` module.

- Returns: A `tuple[bool, int]` describing whether the operation was successful (if the patch could be applied) and the index of the patch (which is required for unpatching)

```python
## In math_lib.py
def get_sqrt(x: float) -> float:
    # Use Hero's Algorithm to approximate sqrt(x) to 9 digits
    x0 = x
    x1 = x0
    while (abs(x1 - x0) > 1e-9):
        x1 = (x0 + (x / x0)) / 2
        x0 = x1
    return x1

import harmonify
import math_lib

# Use the way simpler method of calculating square roots: fractional powers
def new_sqrt(x: float) -> float:
    return x ** (1 / 2.0)

harmonify.patch_function(
    target_module = math_lib,
    function_name = "sqrt",
    replace = new_sqrt
)

# Now math_lib.sqrt(...) is way faster!
```

<br>
<br>

### Function: `harmonify.core.create_method(...)`

- Args:
    - `target_class` (`type`): The class where the method is being added. For example, if the user wants to create `Guy.apply_for_job(...)`, then `target_class = Guy`
    - `method_name` (`str`): The name of the method that is being created. In the previous example, `method_name = "apply_for_job"`
    - `body` (`Callable[..., Any]`): The code of the function (passed as a callable)

- Returns: a `bool`, indicating whether the method was created succesfully



### Function: `harmonify.core.create_function(...)`

- Args:
    - `target_module` (`types.ModuleType`): The module where the function is being added. For example, if the user wants to create `sys.change_stdout()`, then `target_module = sys`
    - `function_name` (`str`): The name of the function that is being created. In the previous example, `function_name = "change_stdout"`
    - `body` (`Callable[..., Any]`): The code of the function (passed as a callable)

- Returns: a `bool`, indicating whether the function was created succesfully

<br>
<br>

### Function: `harmonify.core.delete_method(...)`

- Args:
    - `target_class` (`type`): The class where the method is being removed. For example, if the user wants to delete `Guy.apply_for_job(...)`, then `target_class = Guy`
    - `method_name` (`str`): The name of the method that is being removed. In the previous example, `method_name = "apply_for_job"`

- Returns: a `bool`, indicating whether the method was removed succesfully

<br>
<br>

### Function: `harmonify.core.delete_function(...)`

- Args:
    - `target_module` (`types.ModuleType`): The module where the function is being removed. For example, if the user wants to delete `sys.get_info()`, then `target_module = sys` (don't do it though)
    - `function_name` (`str`): The name of the function that is being removed. In the previous example, `function_name = "get_info"`

- Returns: a `bool`, indicating whether the function was removed succesfully

<br>
<br>

### Function: `harmonify.core.unpatch_method(...)`

- Args:
    - `target_class` (`type`): The class where the patched method residex. For example, if the user wants to unpatch `Guy.ride_bike(...)`, then `target_class = Guy`
    - `method_name` (`str`): The name of the method that is being unpatched. In the previous example, `method_name = "ride_bike"`

- Returns: a `bool`, indicating whether the method was unpatched succesfully

```python
# ... after the Player patch example for `harmonify.core.patch_method` ...

harmonify.unpatch_method(
    target_class = Player,
    method_name = "__init__",
    index = pid1
)

harmonify.unpatch_method(
    target_class = Player,
    method_name = "is_adult",
    index = pid2
)
```

<br>
<br>

### Function: `harmonify.core.unpatch_function(...)`

- Args:
    - `target_class` (`type`): The class where the patched function residex. For example, if the user wants to unpatch `Guy.ride_bike(...)`, then `target_class = Guy`
    - `function_name` (`str`): The name of the function that is being unpatched. In the previous example, `function_name = "ride_bike"`

- Returns: a `bool`, indicating whether the function was unpatched succesfully

<br>
<br>

### Function: `harmonify.core.get_current_module()`

- Returns: the module object of the immediate caller (the module where this function was directly called).
    * If the module object cannot be retrieved, the function returns `None`.

```python
## In some_library.py
import harmonify

# ...

def find_and_apply_patches(mod = None):
    module = mod
    if not module:
        module = harmonify.get_current_module()
    # Find all patches and apply them ...
```

<br>
<br>

# Module: `harmonify.flow_control`

### Constant: `harmonify.flow_control.CONTINUE_EXEC`
Represents a constant used by the internal function patching mechanism. It is required to be returned by a prefix patch to indicate that the execution should continue.

<br>

### Constant: `harmonify.flow_control.CONTINUE_WITHOUT_POSTFIX`
Represents a constant used by the internal function patching mechanism. It is required to be returned by a prefix patch to indicate that the execution should continue but stop after the original method executed (if, say, the postfix patch has errors).

<br>

### Constant: `harmonify.flow_control.STOP_EXEC`
Represents a constant used by the internal function patching mechanism. It is required to be returned by a prefix patch to indicate that the execution should *not* continue, not even with the original method.

<br>
<br>

### Class: `harmonify.flow_control.FlowControlError(Exception)`
Represents an error regarding an invalid flow control state returned by a prefix patch. This error is raised whenever a prefix patch returns a value that is *not* a valid value for flow control.

```python
import harmonify

def foo(*args):
    print(len(args))

def foo_prefix(*args, *kwds):
    if len(args) < 2:
        # This will make Harmonify raise a FlowControlError on call
        return None, args, kwds, "kaboom"
    return None, args, kwds, harmonify.CONTINUE_EXEC

harmonify.patch_function(
    target_module = harmonify.get_current_module(),
    function_name = "foo",
    prefix = foo_prefix
)
```

<br>
<br>

# Module: `harmonify.func_types`

### Type: `harmonify.func_types.PrefixFnType`
Represents a prefix function. For a function to be classified as a valid prefix function it has to meet the following criteria:

- Arguments: 
    * A `self`-like argument (required for methods) 
    * `*args` and `**kwds` (non_postional & keyword args)
- Return value: a tuple/list containing:
    * A result (ignored if the flow control state is not equal to `harmonify.flow_control.STOP_EXEC`)
    * Modified non-postional args (can be equal to the orginal list)
    * Modified keyword args (can be equal to the original dictionary)
    * The flow control state. This has to be one of the constants present in `harmonify.flow_control`, oterwise a `harmonify.flow_control.FlowControlError` will be thrown

<br>

### Type: `harmonify.func_types.PostfixFnType`
Represents a postfix function. For a function to be classified as a valid prefix function it has to meet the following criteria:

- Arguments:
    * A `self`-like argument (required for methods)
    * A call result argument. This will contain the value returned by the original function
    * `*args` and `**kwds` (non_postional & keyword args)

- Return value: This can be anything, as it represents the final `return` in the "chain", and will be sent to the caller as the final result of the call.

<br>

### Type: `harmonify.func_types.ReplaceFnType`
Represents a replace function. This type is meant as a generic function type, and thus all functions theoretically count as `ReplaceFn`s.

<br>
<br>

# Module: `harmonify.hook`

### Function: `harmonify.hook.register_function_hook(...)`
Registers a hook callback for a function in a module.

- Args:
    * `target_module` (`types.ModuleType`): The module where the function is defined. For example, if a hook is registered for the function `my_lib.init()`, then `target_module = my_lib`
    * `function_name` (`str`): The name of the function for which the hook is registered. In the previous example, `function_name = "init"`
    * `hook_callback` (`Callable[..., Any]`): The callback that is used as the hook
    * `hook_id` (`str`): The ID of the registered hook. This is necessary and it is important to check the function source to see which hook ID is required!

- Returns: a `bool` indicating whether the hook was registered.

```python
import harmonify

def init():
    harmonify.call_hook('pre_init', [])   # This will call all hooks registered to 'pre_init'
    state = 'init'
    # ...
    harmonify.call_hook('post_init', [])


# ... #


def pre_init_hook():
    print('Pre-Init hook called!')

def post_init_hook():
    print('Post-Init hook called!')

harmonify.register_function_hook(
    target_module = harmonify.get_current_module(),
    function_name = "init",
    hook_callback = pre_init_hook,
    hook_id = "pre_init"
)

harmonify.register_function_hook(
    target_module = harmonify.get_current_module(),
    function_name = "init",
    hook_callback = post_init_hook,
    hook_id = "post_init"
```

<br>
<br>

### Function: `harmonify.hook.register_method_hook(...)`
Registers a hook callback for a method in a class.

- Args:
    * `target_class` (`type`): The class where the method is defined. For example, if a hook is registered for the method `Game.__init__`, then `target_class = Game`
    * `method_name` (`str`): The name of the method for which the hook is registered. In the previous example, `method_name = "__init__"`
    * `hook_callback` (`Callable[..., Any]`): The callback that is used as the hook
    * `hook_id` (`str`): The ID of the registered hook. This is necessary and it is important to check the method source to see which hook ID is required!

- Returns: a `bool` indicating whether the hook was registered.

```python
import harmonify

class Game:
    def __init__(self):
        harmonify.call_hook('pre_init', [self])   # This will call all hooks registered to 'pre_init' with args = [self]
        self.state = 'init'
        self.create_world()
        # ...
        harmonify.call_hook('post_init', [self])


# ... #


def pre_init_hook(obj_self):
    print('Pre-Init hook called!')

def post_init_hook(obj_self):
    print('Post-Init hook called!')

harmonify.register_method_hook(
    target_class = Game,
    method_name = "__init__",
    hook_callback = pre_init_hook,
    hook_id = "pre_init"
)

harmonify.register_method_hook(
    target_class = Game,
    method_name = "__init__",
    hook_callback = post_init_hook,
    hook_id = "post_init"
)
```

<br>
<br>

### Function: `harmonify.hook.remove_function_hook(...)`
Removes a hook for a function in a module.

- Args:
    * `target_module` (`types.ModuleType`): The module where the function is defined. For example, if the user wants to remove a hook for `my_lib.init()`, then `target_module = "my_lib"`
    * `function_name` (`str`): The name of the function that holds the hook. In the previous example, `function_name = "init"`
    * `hook_id` (`str`): The ID of the registered hook. This is necessary for Harmonify to be able to un-hook the function.

- Returns: a `bool` indicating whether the function was succesfully un-hooked.

```python
# ... insert code from `hook.register_function_hook` example ... #

harmonify.remove_function_hook(
    target_module = harmonify.get_current_module(),
    function_name = "init",
    hook_id = "pre_init"
)
```

<br>
<br>

### Function: `harmonify.hook.remove_method_hook(...)`
Removes a hook for a method in a class.

- Args:
    * `target_class` (`type`): The class where the method is defined. For example, if the user wants to remove a hook for `Game.__init__`, then `target_class = Game`
    * `method_name` (`str`): The name of the method that holds the hook. In the previous example, `method_name = "__init__"`
    * `hook_id` (`str`): The ID of the registered hook. This is necessary for Harmonify to be able to un-hook the method.

- Returns: a `bool` indicating whether the method was succesfully un-hooked.

```python
# ... insert code from `hook.register_method_hook` example ... #

harmonify.remove_method_hook(
    target_class = Game,
    method_name = "__init__",
    hook_id = "pre_init"
)
```

<br>
<br>

***The following functions have the purpose of being used in the target library.***

<br>

### Function: `harmonify.hook.call_function_hook(...)`
    Calls the function hook with the specified ID.

- Args:
    * `hook_id` (`str`): The ID of the function hook to call
    * `args` (`list`, default = `[]`): The arguments to pass to the hook
    * `kwds` (`dict`, default = `{}`): The keyword arguments to pass to the hook

- Returns: an `Any`, representing the result of the hook call.

<br>
<br>

### Function: `harmonify.hook.call_method_hook(...)`
    Calls the method hook with the specified ID.

- Args:
    * `hook_id` (`str`): The ID of the method hook to call
    * `args` (`list`, default = `[]`): The arguments to pass to the hook
    * `kwds` (`dict`, default = `{}`): The keyword arguments to pass to the hook

- Returns: an `Any`, representing the result of the hook call.

<br>
<br>

### Function: `harmonify.hook.call_hook(...)`
Calls the hook with the specified ID.
This function is a wrapper to call either a function or method hook based on the context of the caller.

- Args:
    * `hook_id` (`str`): The ID of the method hook to call
    * `args` (`list`, default = `[]`): The arguments to pass to the hook
    * `kwds` (`dict`, default = `{}`): The keyword arguments to pass to the hook

- Returns: an `Any`, representing the result of the hook call.

<br>

### Function: `harmonify.hook.get_active_function_hooks()`
Returns: a `dict[tuple, dict[str, typing.Callable]]` representing a dictionary of all currently registered function hooks.

<br>

### Function: `harmonify.hook.get_active_function_hooks()`
Returns: a `dict[tuple, dict[str, typing.Callable]]` representing a dictionary of all currently registered function hooks.

<br>
<br>

# Module: `harmonify.info_utils`

### Class: `harmonify.info_utils.PatchInfo`
This class holds information about a patch. Instances of this class are returned when `harmonify.core.get_function_patches()` or `harmonify.get_method_patches()` are called.

<br>
<br>

# Module: `harmonify.patch`

### Class: `harmonify.patch.Patch`
Represents the core of the class-based patching system. This abstract class allows patching only methods on classes.

*Static methods:*
* `Patch.target(target_class, method_name)`: A decorator meant for specifying the target of the patch. Returns: `Callable[[Patch], Patch]`
* `Patch.set_replace(replace_valid)`: Decorator to specify the whether the `replace` patch is valid. Returns: `Callable[[Patch], Patch]`

*Patch methods, default to no patching:*
* `Patch.prefix(self, obj_self, *args, **kwds) -> tuple[Any, list, dict, str]`
* `Patch.postfix(self, obj_self, call_result, *args, **kwds) -> Any`
* `Patch.replace(self, obj_self, *args, **kwds) -> Any`
* `Patch.inject(self) -> tuple[types.ModuleType | type, str, int, int, str]`: Returns a list containing:
    - the target object (or `None` if no injection is desired)
    - the name of the callable to inject into
    - the line after which the code will be injected
    - the type of injection (`harmonify.injector.InsertType.BEFORE_TARGET` / `AFTER_TARGET` / `REPLACE_TARGET`)
    - the code to inject at the specified loaction

<br>
<br>

### Function: `harmonify.patch.apply(...)`
Applies a `Patch` to a method of a class.

- Args:
    * `patch` (`harmonify.Patch`): The patch that is to be applied.

```python
import harmonify

def foo(x):
    print(x)

@harmonify.set_replace(False)
@harmonify.target(harmonify.get_current_module(), "foo")
class MyPatch(harmonify.Patch):
    def postfix(self, _, call_res, *args, **kwds):
        print(args)

harmonify.apply(MyPatch())
```

<br>
<br>

# Module: `harmonify.injector`

## Sub-Module: `harmonify.injector.core`

### Function: `harmonify.injector.core.inject_function(...)`
Inject the specified code snippet in the targeted function's source (at runtime).<br>
If the function is decorated with `harmonify.no_inject`,then this will not do anything.<br>
**Note**: This is very dangerous and allows programmmers to run *unsandboxed code*!
    
- Args:
    * `target_module` (`types.ModuleType`): The module in which the targeted function exists.
    * `function_name` (`str`): The name of the targeted function.
    * `insert_line` (`int`): The line number (relative to the function definition) where the code will be injected.
    * `insert_type` (`int`): The type of injection (before, after, or replace).
    * `target_code` (`str`): The code snippet that will be injected (Replace injection works only if the code to inject is a single statement).

- Returns: a `tuple[bool, int]` indicating whether the injection was successful and the ID of the injection.
<br>
<br>

### Function: `harmonify.injector.core.undo_func_inject(...)`
Revert the injected function back to its original code.

- Args:
    * `target_module` (`types.ModuleType`): The module where the targeted function exists.
    * `function_name` (`str`): The name of the targeted function.
    * `id` (`int`): The ID of the injection that is to be reverted.

- Returns: a `bool` indicating whether the injection was successful.
<br>
<br>

### Function: `harmonify.injector.core.inject_method(...)`
Inject the specified code snippet in the targeted method's source (at runtime).<br>
If the method is decorated with `harmonify.no_inject`,then this will not do anything.<br>
**Note**: This is very dangerous and allows programmmers to run *unsandboxed code*!
    
- Args:
    * `target_class` (`type`): The class in which the targeted method exists.
    * `method_name` (`str`): The name of the targeted method.
    * `insert_line` (`int`): The line number (relative to the method definition) where the code will be injected.
    * `insert_type` (`int`): The type of injection (before, after, or replace).
    * `target_code` (`str`): The code snippet that will be injected (Replace injection works only if the code to inject is a single statement).

- Returns: a `tuple[bool, int]` indicating whether the injection was successful and the ID of the injection.
<br>
<br>

### Function: `harmonify.injector.core.undo_method_inject(...)`
Revert the injected method back to its original code.

- Args:
    * `target_class` (`type`): The module where the targeted method exists.
    * `method_name` (`str`): The name of the targeted method.
    * `id` (`int`): The ID of the injection that is to be reverted.

- Returns: a `bool` indicating whether the injection was successful.

<br>
<br>

## Sub-Module: `harmonify.injector.security`

### Class: `harmonify.injector.security.no_inject`
Class-based decorator to mark a function as not allowing injection from Harmonify.

```python
import harmonify

@harmonify.no_inject
def login(uname: str, passwd: str):
    if get_passwd(uname) == passwd:
        return True
    return False
```

<br>
<br>

### Class: `harmonify.injector.security.allow_inject`
Class-based decorator to mark a function as explicitly allowing injection from Harmonify. This is useful only when the developer wants to *explicitly* mark a function/method as injectable, as Harmonify treats functions as injectable by default.

```python
import harmonify

@harmonify.allow_inject
def reload_page():
    # ... #
    pass
```

<br>
<br>

## Sub-Module: `harmonify.injector.utils`

### Enum: `harmonify.injector.utils.InsertType`
Holds values corresponding to different inection locations.

#### Values:
- `InsertType.BEFORE_TARGET`: Tells the injector to insert the specified code before the target line.
- `InsertType.AFTER_TARGET`: Tells the injector to insert the specified code after the target line.
- `InsertType.REPLACE_TARGET`: Instructs the injector to replace whatever is at the target line with the specified code.
    * *Note:* `REPLACE_TARGET` supports only single statements. If it's necessary to replace the code with multiple lines, *wrap the target code in an `if True: ...` block*.

<br>
<br>

### Class: `harmonify.injector.utils.InsertError(Exception)`
Represents an exception that occurs when the injector is preovided with an invalid insert type.

```python
import harmonify

def test(x):
    if x > 5:
        print("X > 5")
    # ^^^ Insert target here ^^^
    return x

harmonify.inject_function(
    target_module = harmonify.get_current_module(),
    function_name = "test",
    insert_line = 3,
    insert_type = 12312321,   # This will *definitely* raise an InsertError
    code_to_inject = "if x < 5:\n\tprint('X < 5')"
)
```

<br>
<br>

# Module: `harmonify.context`

### Function: `harmonify.context.apply_patch(...)`
This function returns a context manager for easily managing patches.

- Args:
    * `target` (`types.ModuleType | type`): The target object that holds the callable
    * `callable_name` (`str`): The name of the callable
    * `prefix` (`PrefixFnType | None`, default = `None`): The prefix patch
    * `postfix` (`PostfixFnType | None`, default = `None`): The postfix patch
    * `replace` (`ReplaceFnType | None`, default = `None`): The replacement function

- Returns: a `PatchManager` for creating the context.

<br>
<br>

### Function: `harmonify.context.apply_inject(...)`
Returns a context manager for easily managing injections.

- Args:
    * `target` (`types.ModuleType | type`): The target object that holds the callable
    * `callable_name` (`str`): The name of the callable
    * `insert_line` (`int`): The line at which the code will be inserted
    * `insert_type` (`int`): The type of insertion (`harmonify.injector.InsertType.BEFORE_TARGET` / `AFTER_TARGET` / `REPLACE_TARGET`)
    * `code_to_inject` (`str`): The code to inject

- Returns: an `InjectManager` for creating the context.

<br>
<br>

### Function: `harmonify.context.add_hook(...)`
Returns a context manager for easily managing hooks.

- Args:
    * `target` (`types.ModuleType | type`): The target object that holds the callable
    * `callable_name` (`str`): The name of the callable
    * `hook_callback` (`Callable[..., Any]`): The hook callback
    * `hook_id` (`str`): The ID of the hook to add

- Returns: a `HookManager` for managing the context.

<br>
<br>
    