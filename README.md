# Harmonify

Harmonify is a Python library that allows users to change the behavior of classes at runtime, with nothing more than a few function calls.
Inspired by Harmony (the *very* popular C# library that also allows runtime behavior modification), Harmonify is flexible and uses a simple system based on monkey-patching.
Like its C# equivalent, it can be used for:
* **Debugging:** Inject logging or checks into methods without changing them permanently.
* **Testing:** Isolate parts of your code by temporarily changing how certain methods behave.
* **Extending Libraries:** Add new features or modify behavior of classes from libraries you can't edit directly.
* **Experimentation:** Play around with how code runs in a non-destructive way.

## Features

* **Prefix Patching:** Run your custom code *before* the original method executes.
* **Postfix Patching:** Run your custom code *after* the original method executes, even allowing you to modify its return value.
* **Replace Patching:** Completely swap out the original method's logic with your own.
* **Create & Delete methods:** Add or remove methods from a class or a module, without changing the other ones.
* **Easy Unpatching:** Restore methods to their original state with a simple call.
* **Function patching:** Patch functions as easily as methods!
* **Code Injection & Injection undo-ing:** Add you own code inside any Python function or method and revert at any time.
  * *Note:* Be careful with code injection, and *do **not** inject code coming from a source you don't trust!* If you're a library developer and want to prevent your code from being injected into, decorate your code with the `harmonify.injector_security.no_inject` decorator.

## Installation

Installing Harmonify is as easy as using `pip`:

```shell
pip install harmonify-patcher
```
After that, Harmonify will be available globally!



## Example Programs

### Function Patching
#### my_library.py
```python
def sqrt(x: float) -> float:
	return x ** (1 / 2)

def pow(x: float, n: int) -> float:
	return x ** n

def get_version():
	return "1.0"
```

#### main.py
```python
import harmonify
import my_library

def new_get_ver():
	return "Latest release"

print(my_library.get_version())   # 1.0
harmonify.patch_function(
	target_module = my_library,
	function_name = "get_version",
	replace = new_get_ver
)
print(my_library.get_version())   # Latest release
```


### Code Injection
#### api_lib.py
```python
import harmonify

def open_api1():
	print("Doing API stuff...")

@harmonify.allow_inject
def open_api2():
	print("More API stuff...")

@harmonify.no_inject
def restricted_api(uname, passwd):
	print(f"Doing restricted API access with:\n\tUsername: {uname}\n\tPassword: {passwd}")
```

#### main.py
```python
import harmonify
if harmonify.inject_function(
    harmonify.get_current_module(),
    "open_api1", 1,
    "print('Done!')"
):
    print("Successfully injected open_api1")

    
if harmonify.inject_function(
    harmonify.get_current_module(),
    "open_api2", 1,
    "print('Done!')"
):
    print("Successfully injected open_api2")


if harmonify.inject_function(
    harmonify.get_current_module(),
    "restricted_api", 1,
    "print('Done!')"
):
    print("Successfully injected restricted_api")

open_api1()
open_api2()
restricted_api("secret service agent #42", "super secret password")
```



# Changelog

## 1.4.0
Added hooks. These can be registered to a callable via the `register_function_hook` and `register_method_hook` functions.
Hooks can be called by a library function with `call_function_hook` or `call_method_hook`. Multiple hooks can be added to the same callable. <br>
*Future plan (possibly in 1.4.1): add a generic `call_hook` function, which would dispatch to `call_function_hook` or `call_method_hook`, depending on the caller.*

## 1.3.2
Fixed an internal bug where an `UnboundLocalError` would appear when creating a new patch.

## 1.3.1
Added the `PatchInfo` utility class and two new fucntions, `get_function_patches` and `get_method_patches`.
These two functions return informations about every patch that has been applied up until the call.

## 1.3.0
Slightly improved safeguards to provide an easy API. This *does* mean that the library dev needs to have Harmonify installed, which is not ideal.

## 1.2.3
Added injection safeguards. These should be applied in the target library.

## 1.2.2
Fixed a problem where the code would be injected *before* the target line.
