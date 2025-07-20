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
  * *Note:* Be careful with code injection. If you're a library developer and want to prevent your code from being injected into, decorate your code with the `harmonify.injector_security.no_inject` decorator.

## Installation

Installing Harmonify is as easy as using `pip`:

```shell
pip install harmonify-patcher
```
After that, Harmonify will be available globally!

## Example Program

### my_library.py
```python
def sqrt(x: float) -> float:
  return x ** (1 / 2)

def pow(x: float, n: int) -> float:
  return x ** n

def get_version():
  return "1.0"
```

### main.py
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

# Changelog
## 1.3.0
Improve safeguards and provide an easy API. This *does* mean that the library dev needs to have Harmonify installed, which is not ideal.

## 1.2.3
* Added injection safeguards. These should be applied in the target library.

## 1.2.2
* Fixed a problem where the code would be injected *before* the target line.
